import { useEffect, useState } from "react";
import { authService, tokenStore } from "../api/index.js";
import { AuthContext } from "./authContextInstance.js";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [authError, setAuthError] = useState(null);

  // Check current session on mount if tokenStore has a token
  useEffect(() => {
    async function initAuth() {
      const token = tokenStore.getAccessToken();
      if (!token) {
        return;
      }
      try {
        setIsLoading(true);
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      } catch {
        tokenStore.clearTokens();
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }

    initAuth();
  }, []);

  async function login(email, password) {
    setIsLoading(true);
    setAuthError(null);
    try {
      const tokenData = await authService.login(email, password);
      // Fetch user profile using access token
      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      } catch {
        // Fallback to basic session if /auth/me returns unpopulated object
        setUser({ email, role: "user" });
      }
      return tokenData;
    } catch (err) {
      setAuthError(err.message || "Failed to sign in");
      throw err;
    } finally {
      setIsLoading(false);
    }
  }

  async function logout() {
    setIsLoading(true);
    try {
      await authService.logout();
    } catch {
      // Continue clearing local state regardless of server logout status
    } finally {
      tokenStore.clearTokens();
      setUser(null);
      setIsLoading(false);
    }
  }

  const value = {
    user,
    isAuthenticated: Boolean(user && tokenStore.getAccessToken()),
    isLoading,
    authError,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthProvider;
