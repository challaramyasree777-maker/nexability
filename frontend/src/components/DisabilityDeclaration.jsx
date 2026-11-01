import { useId, useState } from "react";
import { candidateService } from "../api/index.js";

/**
 * DisabilityDeclaration Component
 * Optional candidate self-declaration step adhering to NexAbility accessibility standards.
 *
 * @param {Object} props
 * @param {Function} props.onComplete Callback when user completes or skips (passes { declared, skipped })
 * @param {boolean} [props.isStandalone] Whether rendered standalone or in onboarding flow
 */
export function DisabilityDeclaration({ onComplete, isStandalone = false }) {
  const [isDeclared, setIsDeclared] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  const checkboxId = useId();
  const noteId = useId();
  const titleId = useId();
  const descId = useId();

  async function handleContinue(event) {
    event.preventDefault();
    setError("");
    setStatusMessage("");

    // If candidate did NOT check the box, proceed without sending any declaration request
    if (!isDeclared) {
      if (onComplete) {
        onComplete({ declared: false, skipped: false });
      }
      return;
    }

    // Candidate voluntarily selected the checkbox - save declaration
    setIsLoading(true);
    try {
      await candidateService.saveDeclaration({
        accepted: true,
        declaration_version: "v1",
      });
      setStatusMessage("Your voluntary declaration has been recorded.");
      if (onComplete) {
        onComplete({ declared: true, skipped: false });
      }
    } catch (err) {
      // The backend endpoint /candidates/me/declaration may not be deployed yet
      if (err.status === 404 || err.status === 0) {
        const pendingMsg =
          "Note: The candidate declaration backend endpoint (/candidates/me/declaration) is pending server deployment. Your voluntary preference has been noted.";
        setStatusMessage(pendingMsg);
        // Do not block onboarding progression even if backend is pending
        if (onComplete) {
          onComplete({ declared: true, skipped: false, backendPending: true });
        }
      } else {
        setError(
          err.message ||
            "Unable to save your declaration at this time. You can manage this anytime in profile settings."
        );
      }
    } finally {
      setIsLoading(false);
    }
  }

  function handleSkip() {
    setError("");
    setStatusMessage("");
    // Do NOT send any API request when skipping
    if (onComplete) {
      onComplete({ declared: false, skipped: true });
    }
  }

  return (
    <section
      className="declaration-card"
      aria-labelledby={titleId}
      aria-describedby={descId}
    >
      <header className="declaration-header">
        <p className="eyebrow">CANDIDATE ONBOARDING &bull; OPTIONAL</p>
        <h2 id={titleId} className="declaration-title">
          Help us create a more inclusive experience.
        </h2>
        <p id={descId} className="declaration-subtitle">
          We believe everyone deserves equal opportunities. You can optionally share
          this information to help us improve your experience.
        </p>
      </header>

      {/* Pale-blue information panel */}
      <div className="declaration-info-panel" role="region" aria-label="Voluntary declaration details">
        <div className="declaration-checkbox-row">
          <input
            type="checkbox"
            id={checkboxId}
            className="declaration-checkbox"
            checked={isDeclared}
            onChange={(e) => {
              setIsDeclared(e.target.checked);
              setError("");
            }}
            aria-describedby={noteId}
            disabled={isLoading}
          />
          <label htmlFor={checkboxId} className="declaration-checkbox-label">
            <strong>I voluntarily identify as a person with a disability.</strong>
          </label>
        </div>

        <p id={noteId} className="declaration-note">
          Your declaration is completely optional. You do not need to provide a medical
          diagnosis or upload medical documents. You can skip this step and manage your
          declaration later through your profile settings.
        </p>

        {/* Privacy & Safeguard Pillars */}
        <ul className="declaration-safeguards" aria-label="Privacy and inclusion guarantees">
          <li>
            <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
            <span><strong>Completely Voluntary:</strong> Proceed with or without declaring.</span>
          </li>
          <li>
            <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
            <span><strong>No Medical Documents:</strong> Zero diagnosis paperwork needed.</span>
          </li>
          <li>
            <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
            <span><strong>Privacy Protected:</strong> Never automatically shared with employers.</span>
          </li>
          <li>
            <span className="safeguard-icon" aria-hidden="true">&#10003;</span>
            <span><strong>Fully Withdrawable:</strong> Manage or delete anytime in profile settings.</span>
          </li>
        </ul>
      </div>

      {/* Screen Reader Live Announcements */}
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

      {/* Action Buttons */}
      <div className="declaration-actions">
        <button
          type="button"
          className="btn btn-primary"
          onClick={handleContinue}
          disabled={isLoading}
        >
          {isLoading ? "Saving..." : "Continue"}
        </button>

        {!isStandalone && (
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleSkip}
            disabled={isLoading}
          >
            Skip for now
          </button>
        )}
      </div>
    </section>
  );
}

export default DisabilityDeclaration;
