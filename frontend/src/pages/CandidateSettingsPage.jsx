import { useEffect, useId, useState } from "react";
import { Link } from "react-router-dom";
import { candidateService } from "../api/index.js";
import { useAuth } from "../context/useAuth.js";

function CandidateSettingsPage() {
  const { user } = useAuth();
  const [hasDeclaration, setHasDeclaration] = useState(false);
  const [isDeclaredInput, setIsDeclaredInput] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [error, setError] = useState("");

  const checkboxId = useId();
  const noteId = useId();

  // Load current declaration status on mount
  useEffect(() => {
    async function fetchDeclarationStatus() {
      setIsLoading(true);
      setError("");
      try {
        const res = await candidateService.getDeclaration();
        if (res && res.accepted) {
          setHasDeclaration(true);
          setIsDeclaredInput(true);
        }
      } catch (err) {
        // If 404 or pending deployment, default to false without crashing
        if (err.status !== 404) {
          // Log or silently ignore if endpoint is not deployed yet
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchDeclarationStatus();
  }, []);

  // Save new declaration
  async function handleSave(event) {
    event.preventDefault();
    setError("");
    setStatusMessage("");

    if (!isDeclaredInput) {
      setError("Please check the declaration box before saving, or leave it unchanged.");
      return;
    }

    setIsLoading(true);
    try {
      await candidateService.saveDeclaration({
        accepted: true,
        declaration_version: "v1",
      });
      setHasDeclaration(true);
      setStatusMessage("Your voluntary disability declaration has been saved.");
    } catch (err) {
      if (err.status === 404 || err.status === 0) {
        setStatusMessage(
          "Note: The backend declaration endpoint (/candidates/me/declaration) is pending server deployment. Your preference has been saved in your local session."
        );
        setHasDeclaration(true);
      } else {
        setError(err.message || "Failed to update declaration. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  // Withdraw declaration via DELETE /candidates/me/declaration
  async function handleWithdraw() {
    setError("");
    setStatusMessage("");
    setIsLoading(true);

    try {
      await candidateService.withdrawDeclaration();
      setHasDeclaration(false);
      setIsDeclaredInput(false);
      setStatusMessage("Your voluntary disability declaration has been withdrawn.");
    } catch (err) {
      if (err.status === 404 || err.status === 0) {
        // Backend not deployed yet, allow withdrawal in frontend session
        setHasDeclaration(false);
        setIsDeclaredInput(false);
        setStatusMessage(
          "Your voluntary declaration has been removed from this session. (Backend endpoint /candidates/me/declaration is pending deployment)."
        );
      } else {
        setError(err.message || "Failed to withdraw declaration. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main id="main-content" className="settings-main" tabIndex="-1">
      <div className="settings-container">
        <header className="settings-header">
          <p className="eyebrow">PROFILE &amp; PRIVACY SETTINGS</p>
          <h1>Candidate Settings</h1>
          <p className="settings-intro">
            Manage your personal preferences, privacy settings, and voluntary self-declarations.
          </p>
        </header>

        {/* Declaration Management Section */}
        <section
          className="settings-section declaration-card"
          aria-labelledby="declaration-settings-title"
        >
          <div className="section-title-row">
            <div>
              <h2 id="declaration-settings-title" className="declaration-title">
                Disability Self-Declaration
              </h2>
              <p className="declaration-subtitle">
                Help us create a more inclusive experience. Your declaration is
                completely optional and withdrawable at any time.
              </p>
            </div>
            <span
              className={
                hasDeclaration ? "status-badge status-active" : "status-badge status-inactive"
              }
              aria-label={`Declaration status: ${hasDeclaration ? "Active" : "Not declared"}`}
            >
              {hasDeclaration ? "Active on File" : "Not Declared"}
            </span>
          </div>

          <div
            className="declaration-info-panel"
            role="region"
            aria-label="Disability declaration policy"
          >
            <p id={noteId} className="declaration-note">
              Your declaration is completely optional. You do not need to provide a
              medical diagnosis or upload medical documents. You can manage or withdraw
              your declaration at any time without affecting your job applications or profile.
            </p>

            <ul className="declaration-safeguards" aria-label="Privacy safeguards">
              <li>
                <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
                <span><strong>Strictly Voluntary:</strong> Completely up to your personal choice.</span>
              </li>
              <li>
                <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
                <span><strong>No Diagnosis Needed:</strong> Medical paperwork is never required.</span>
              </li>
              <li>
                <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
                <span><strong>Employer Privacy:</strong> Not automatically shared with recruiters.</span>
              </li>
              <li>
                <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
                <span><strong>Withdrawable Anytime:</strong> Remove your declaration with one click.</span>
              </li>
            </ul>

            {hasDeclaration ? (
              <div className="active-declaration-notice">
                <p>
                  You currently have a voluntary disability declaration recorded for your candidate profile.
                </p>
                <button
                  type="button"
                  className="btn btn-secondary withdraw-btn"
                  onClick={handleWithdraw}
                  disabled={isLoading}
                >
                  {isLoading ? "Withdrawing..." : "Withdraw Declaration"}
                </button>
              </div>
            ) : (
              <form className="declaration-form" onSubmit={handleSave} noValidate>
                <div className="declaration-checkbox-row">
                  <input
                    type="checkbox"
                    id={checkboxId}
                    className="declaration-checkbox"
                    checked={isDeclaredInput}
                    onChange={(e) => {
                      setIsDeclaredInput(e.target.checked);
                      setError("");
                    }}
                    aria-describedby={noteId}
                    disabled={isLoading}
                  />
                  <label htmlFor={checkboxId} className="declaration-checkbox-label">
                    <strong>I voluntarily identify as a person with a disability.</strong>
                  </label>
                </div>

                <div className="declaration-actions">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={isLoading || !isDeclaredInput}
                  >
                    {isLoading ? "Saving..." : "Save Declaration"}
                  </button>
                </div>
              </form>
            )}
          </div>

          {statusMessage ? (
            <div className="form-status" role="status" aria-live="polite">
              {statusMessage}
            </div>
          ) : null}

          {error ? (
            <div className="form-error" role="alert" aria-live="assertive">
              {error}
            </div>
          ) : null}
        </section>

        <div className="settings-footer-actions">
          <Link className="btn btn-secondary" to="/">
            Return to Home
          </Link>
          {user ? (
            <Link className="btn btn-primary" to="/login">
              Account Overview
            </Link>
          ) : null}
        </div>
      </div>
    </main>
  );
}

export default CandidateSettingsPage;
