/**
 * NexAbility Authentication API Service
 * Integrates strictly with confirmed live endpoints from OpenAPI schema.
 */

import { apiClient, tokenStore } from "./client.js";

export const authService = {
  /**
   * Screen employer email domain for corporate eligibility
   * Endpoint: POST /auth/employer/email/check
   * Body: { email: string }
   * Returns: { eligible: boolean, reason: string, domain: string | null }
   */
  async checkEmployerEmail(email) {
    return apiClient.post("/auth/employer/email/check", { email });
  },

  /**
   * Send one-time passcode for registration or password reset
   * Endpoint: POST /auth/otp/send
   * Body: { email: string, purpose: "CANDIDATE_REGISTRATION" | "EMPLOYER_REGISTRATION" | "PASSWORD_RESET" }
   * Returns: { message: string, expires_in: number | null }
   */
  async sendOtp(email, purpose) {
    return apiClient.post("/auth/otp/send", { email, purpose });
  },

  /**
   * Verify one-time passcode to receive a temporary verification ticket
   * Note: The verification_ticket is a proof token for registration/reset, NOT an access token.
   * Endpoint: POST /auth/otp/verify
   * Body: { email: string, purpose: "CANDIDATE_REGISTRATION" | "EMPLOYER_REGISTRATION" | "PASSWORD_RESET", otp: string }
   * Returns: { verified: boolean, message: string, verification_ticket: string, expires_in: number }
   */
  async verifyOtp(email, purpose, otp) {
    return apiClient.post("/auth/otp/verify", { email, purpose, otp });
  },

  /**
   * Register a new candidate using the verified ticket
   * Endpoint: POST /auth/candidate/register
   * Body: { full_name, email, password, phone, verification_ticket }
   * Returns: { id: string, email: string, full_name: string, role: string, message: string }
   */
  async registerCandidate({ full_name, email, password, phone = null, verification_ticket }) {
    return apiClient.post("/auth/candidate/register", {
      full_name,
      email,
      password,
      phone: phone || null,
      verification_ticket,
    });
  },

  /**
   * Register a new employer using the verified ticket
   * Endpoint: POST /auth/employer/register
   * Body: { full_name, company_name, email, password, phone, website, verification_ticket }
   * Returns: { id, email, full_name, company_name, role, verification_status, message }
   */
  async registerEmployer({
    full_name,
    company_name,
    email,
    password,
    phone = null,
    website = null,
    verification_ticket,
  }) {
    return apiClient.post("/auth/employer/register", {
      full_name,
      company_name,
      email,
      password,
      phone: phone || null,
      website: website || null,
      verification_ticket,
    });
  },

  /**
   * Sign in with email and password
   * Endpoint: POST /auth/login
   * Body: { email: string, password: string }
   * Returns: { access_token: string, refresh_token: string, token_type: string, expires_in: number }
   */
  async login(email, password) {
    const data = await apiClient.post("/auth/login", { email, password });
    if (data?.access_token) {
      tokenStore.setAccessToken(data.access_token);
    }
    if (data?.refresh_token) {
      // In-memory only, never persisted to localStorage
      tokenStore.setRefreshToken(data.refresh_token);
    }
    return data;
  },

  /**
   * Refresh session using refresh token or session cookie
   * Endpoint: POST /auth/refresh
   * Body: { refresh_token: string }
   * Returns: { access_token: string, refresh_token: string, token_type: string, expires_in: number }
   */
  async refreshSession() {
    const refreshToken = tokenStore.getRefreshToken();
    if (!refreshToken) {
      throw new Error("No refresh token available in current session.");
    }

    const data = await apiClient.post("/auth/refresh", { refresh_token: refreshToken });
    if (data?.access_token) {
      tokenStore.setAccessToken(data.access_token);
    }
    if (data?.refresh_token) {
      tokenStore.setRefreshToken(data.refresh_token);
    }
    return data;
  },

  /**
   * Logout current session
   * Endpoint: POST /auth/logout
   * Body: { refresh_token: string }
   * Returns: { message: string }
   */
  async logout() {
    const refreshToken = tokenStore.getRefreshToken() || "";
    try {
      if (refreshToken) {
        await apiClient.post("/auth/logout", { refresh_token: refreshToken });
      }
    } finally {
      tokenStore.clearTokens();
    }
  },

  /**
   * Get current authenticated user profile
   * Endpoint: GET /auth/me
   * Requires: Bearer access token
   */
  async getCurrentUser() {
    return apiClient.get("/auth/me", { requiresAuth: true });
  },

  /**
   * Request password reset OTP
   * Endpoint: POST /auth/password/forgot
   */
  async forgotPassword(email) {
    return apiClient.post("/auth/password/forgot", { email });
  },

  /**
   * Reset password with verification ticket
   * Endpoint: POST /auth/password/reset
   */
  async resetPassword({ email, verification_ticket, new_password }) {
    return apiClient.post("/auth/password/reset", {
      email,
      verification_ticket,
      new_password,
    });
  },

  /**
   * Google Authentication Status
   * Note: The live backend OpenAPI schema does not define `/api/v1/auth/google`.
   */
  isGoogleAuthAvailable: false,
};

export default authService;
