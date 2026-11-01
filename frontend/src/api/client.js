/**
 * NexAbility Core API Client
 * Centralized HTTP client supporting GET, POST, PATCH, PUT, DELETE
 * with standard response/error envelope handling, Bearer token injection,
 * 204 No-Content handling, and in-memory token security.
 */

export class ApiError extends Error {
  constructor(message, status, data = null, validationErrors = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
    this.validationErrors = validationErrors;
  }
}

// In-memory token storage (NEVER stored in localStorage or sessionStorage for security)
let inMemoryAccessToken = null;
let inMemoryRefreshToken = null;

export const tokenStore = {
  getAccessToken: () => inMemoryAccessToken,
  setAccessToken: (token) => {
    inMemoryAccessToken = token;
  },
  getRefreshToken: () => inMemoryRefreshToken,
  setRefreshToken: (token) => {
    inMemoryRefreshToken = token;
  },
  clearTokens: () => {
    inMemoryAccessToken = null;
    inMemoryRefreshToken = null;
  },
};

/**
 * Normalizes and formats FastAPI / Pydantic validation error arrays
 */
function formatValidationErrors(detail) {
  if (Array.isArray(detail)) {
    return detail.map((err) => {
      const field = Array.isArray(err.loc) ? err.loc.slice(1).join(".") : "field";
      return {
        field: field || "input",
        message: err.msg || "Invalid value",
        type: err.type,
      };
    });
  }
  return null;
}

/**
 * Returns a user-friendly message for common HTTP status codes
 */
function getDefaultErrorMessage(status) {
  switch (status) {
    case 400:
      return "Invalid request. Please check the information provided.";
    case 401:
      return "Authentication required. Please sign in with valid credentials.";
    case 403:
      return "Access denied. You do not have permission to perform this action.";
    case 404:
      return "The requested resource could not be found.";
    case 409:
      return "A conflict occurred. This record or email may already exist.";
    case 422:
      return "Validation failed. Please correct the highlighted errors.";
    case 429:
      return "Too many requests. Please wait a moment before trying again.";
    case 500:
    case 502:
    case 503:
    case 504:
      return "The server encountered an error. Please try again later.";
    default:
      return `Request failed with status ${status}.`;
  }
}

/**
 * Resolves the API base URL from import.meta.env.VITE_API_BASE_URL
 * Defaults to '/api/v1' if not defined or if using the local Vite proxy.
 */
export function getApiBaseUrl() {
  const envUrl = import.meta.env.VITE_API_BASE_URL;
  if (envUrl && typeof envUrl === "string") {
    // Strip trailing slash if present
    return envUrl.replace(/\/+$/, "");
  }
  return "/api/v1";
}

/**
 * Central request dispatcher
 */
async function request(endpoint, options = {}) {
  const {
    method = "GET",
    body = null,
    headers = {},
    requiresAuth = false,
    useProxyFallback = true,
    ...customOptions
  } = options;

  const baseUrl = getApiBaseUrl();
  const normalizedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${baseUrl}${normalizedEndpoint}`;

  const requestHeaders = {
    Accept: "application/json",
    // Ngrok free tunnels show an interstitial page unless this header is present
    "ngrok-skip-browser-warning": "1",
    ...headers,
  };

  if (body !== null && !(body instanceof FormData)) {
    requestHeaders["Content-Type"] = "application/json";
  }

  // Attach Bearer token to authenticated requests
  if (requiresAuth) {
    const token = tokenStore.getAccessToken();
    if (token) {
      requestHeaders.Authorization = `Bearer ${token}`;
    }
  }

  const fetchOptions = {
    method,
    headers: requestHeaders,
    // Support the backend's confirmed refresh-cookie policy
    credentials: "include",
    ...customOptions,
  };

  if (body !== null) {
    fetchOptions.body = body instanceof FormData ? body : JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(url, fetchOptions);
  } catch (networkError) {
    // Handle CORS or network failure by attempting dev proxy fallback if configured
    if (
      useProxyFallback &&
      baseUrl.startsWith("http") &&
      typeof window !== "undefined" &&
      window.location.hostname === "localhost"
    ) {
      const fallbackUrl = `/api/v1${normalizedEndpoint}`;
      try {
        response = await fetch(fallbackUrl, fetchOptions);
      } catch {
        throw new ApiError(
          "Unable to connect to the NexAbility backend. Please check network connectivity or CORS configuration.",
          0,
          { originalError: networkError.message }
        );
      }
    } else {
      throw new ApiError(
        "Unable to connect to the NexAbility backend. Please check network connectivity or CORS configuration.",
        0,
        { originalError: networkError.message }
      );
    }
  }

  // Handle HTTP 204 No Content
  if (response.status === 204) {
    return null;
  }

  // Parse JSON response or fallback to empty object
  let responseData = null;
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    try {
      responseData = await response.json();
    } catch {
      // Keep responseData as null
    }
  } else {
    try {
      const text = await response.text();
      if (text) {
        responseData = { raw: text };
      }
    } catch {
      // Keep responseData as null
    }
  }

  // Handle error responses
  if (!response.ok) {
    let errorMessage = getDefaultErrorMessage(response.status);
    let validationErrors = null;

    if (responseData) {
      if (typeof responseData.detail === "string") {
        errorMessage = responseData.detail;
      } else if (Array.isArray(responseData.detail)) {
        validationErrors = formatValidationErrors(responseData.detail);
        if (validationErrors && validationErrors.length > 0) {
          errorMessage = validationErrors.map((v) => `${v.field}: ${v.message}`).join(", ");
        }
      } else if (typeof responseData.message === "string") {
        errorMessage = responseData.message;
      }
    }

    throw new ApiError(errorMessage, response.status, responseData, validationErrors);
  }

  return responseData;
}

export const apiClient = {
  get: (endpoint, options = {}) => request(endpoint, { ...options, method: "GET" }),
  post: (endpoint, body, options = {}) => request(endpoint, { ...options, method: "POST", body }),
  patch: (endpoint, body, options = {}) => request(endpoint, { ...options, method: "PATCH", body }),
  put: (endpoint, body, options = {}) => request(endpoint, { ...options, method: "PUT", body }),
  delete: (endpoint, options = {}) => request(endpoint, { ...options, method: "DELETE" }),
  tokenStore,
};

export default apiClient;
