 
import { useState } from "react";
import "./App.css";

function App() {
  const [showKeyboardGuide, setShowKeyboardGuide] = useState(false);

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>

      <header className="site-header">
        <a className="brand" href="#home" aria-label="NexAbility home">
          NexAbility<span aria-hidden="true">.</span>
        </a>

        <nav aria-label="Main navigation">
          <a href="#how-it-works">How it works</a>
          <a href="#accessibility">Accessibility</a>
        </nav>
      </header>

      <main id="main-content" tabIndex="-1">
        <section className="hero" id="home" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">ACCESSIBILITY FIRST</p>

            <h1 id="hero-title">
              A digital world
              <br />
              open to everyone.
            </h1>

            <p className="hero-description">
              We're building NexAbility with keyboard navigation,
              readable content, and screen-reader support at its core.
              Every important action should be possible without a mouse.
            </p>

            <div className="hero-actions">
              <a className="primary-link" href="#how-it-works">
                Explore accessibility
              </a>

              <button
                type="button"
                className="secondary-button"
                aria-expanded={showKeyboardGuide}
                aria-controls="keyboard-guide"
                onClick={() =>
                  setShowKeyboardGuide((current) => !current)
                }
              >
                {showKeyboardGuide
                  ? "Hide keyboard guide"
                  : "Show keyboard guide"}
              </button>
            </div>

            <div
              id="keyboard-guide"
              className="keyboard-guide"
              hidden={!showKeyboardGuide}
            >
              <h2>Keyboard guide</h2>
              <ul>
                <li>
                  <kbd>Tab</kbd> — move to the next interactive element.
                </li>
                <li>
                  <kbd>Shift</kbd> + <kbd>Tab</kbd> — move backwards.
                </li>
                <li>
                  <kbd>Enter</kbd> — open a link or activate a button.
                </li>
                <li>
                  <kbd>Space</kbd> — activate a focused button.
                </li>
              </ul>
            </div>
          </div>

          <div
            className="visual-panel"
            aria-hidden="true"
          >
            <div className="visual-orbit orbit-one" />
            <div className="visual-orbit orbit-two" />

            <div className="visual-card back-card">
              <span>ACCESS FOR ALL</span>
            </div>

            <div className="visual-card front-card">
              <span className="visual-symbol">N</span>
              <span>Human-centred technology</span>
            </div>

            <div className="visual-dot" />
          </div>
        </section>

        <section
          className="content-section"
          id="how-it-works"
          aria-labelledby="how-title"
        >
          <p className="eyebrow">DESIGNED WITH PURPOSE</p>
          <h2 id="how-title">Accessibility is part of the experience.</h2>
          <p className="section-intro">
            The interface should be easy to understand, navigate,
            and operate using a keyboard and assistive technology.
          </p>

          <div className="feature-grid">
            <article className="feature-card">
              <span className="feature-number" aria-hidden="true">
                01
              </span>
              <h3>Keyboard navigation</h3>
              <p>
                Use links, buttons, and form controls without needing
                a mouse. Keep the focus order clear and predictable.
              </p>
            </article>

            <article className="feature-card">
              <span className="feature-number" aria-hidden="true">
                02
              </span>
              <h3>Screen-reader support</h3>
              <p>
                Use meaningful headings, labelled controls, and
                understandable feedback so content can be read aloud.
              </p>
            </article>

            <article className="feature-card">
              <span className="feature-number" aria-hidden="true">
                03
              </span>
              <h3>Clear and consistent design</h3>
              <p>
                Use readable text, visible focus indicators, strong
                contrast, and alternatives to decorative movement.
              </p>
            </article>
          </div>
        </section>

        <section
          className="content-section accessibility-section"
          id="accessibility"
          aria-labelledby="accessibility-title"
        >
          <p className="eyebrow">OUR APPROACH</p>
          <h2 id="accessibility-title">
            Every action should have a keyboard alternative.
          </h2>
          <p className="section-intro">
            Interactive 3D elements will be supplementary. Essential
            information and actions must remain available as accessible
            text and standard controls.
          </p>
          <a className="text-link" href="#home">
            Return to the top
          </a>
        </section>
      </main>

      <footer className="site-footer">
        <p>NexAbility</p>
        <p>Built with accessibility in mind.</p>
      </footer>
    </div>
  );
}

export default App;
              