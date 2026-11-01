import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/useAuth.js";

function LoginPage() {
  const { user, login, logout, isLoading } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setStatus("");

    if (!email.trim() || !password) {
      setError("Please enter both email and password.");
      return;
    }

    try {
      await login(email.trim(), password);
      setStatus("Successfully signed in.");
    } catch (err) {
      setError(err.message || "Sign-in failed. Please check your credentials.");
    }
  }

  return (
    <main id="main-content" className="auth-main" tabIndex="-1">
      <section className="auth-panel" aria-labelledby="login-title">
        <p className="eyebrow">Sign in</p>
        <h1 id="login-title">Welcome back to your next opportunity.</h1>
        <p>Use your NexAbility account to continue.</p>

        {user ? (
          <div className="auth-authenticated" role="status">
            <p className="form-status">
              Signed in as <strong>{user.email || user.full_name || "Authenticated User"}</strong>
              {user.role ? ` (${user.role})` : ""}
            </p>
            <div className="auth-actions">
              <button
                className="btn btn-secondary"
                type="button"
                onClick={logout}
                disabled={isLoading}
              >
                Sign Out
              </button>
              <Link className="btn btn-primary" to="/">
                Return to Home
              </Link>
            </div>
          </div>
        ) : (
          <form className="auth-form" onSubmit={handleSubmit} noValidate>
            <div>
              <label className="field-label" htmlFor="login-email">
                Email address
              </label>
              <input
                className="field-control"
                id="login-email"
                name="email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <div>
              <label className="field-label" htmlFor="login-password">
                Password
              </label>
              <input
                className="field-control"
                id="login-password"
                name="password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <button className="btn btn-primary" type="submit" disabled={isLoading}>
              {isLoading ? "Signing In..." : "Sign In"}
            </button>
          </form>
        )}

        {error ? (
          <p className="form-error" role="alert">
            {error}
          </p>
        ) : null}

        {status && !user ? (
          <p className="form-status" role="status">
            {status}
          </p>
        ) : null}

        {!user && (
          <p>
            New to NexAbility? <Link to="/register">Create an account</Link>
          </p>
        )}
      </section>
    </main>
  );
}

export default LoginPage;
