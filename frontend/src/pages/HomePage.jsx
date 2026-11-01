import { Link } from "react-router-dom";

function HomePage() {
  return (
    <main id="main-content" tabIndex="-1">
      {/* 1. HERO SECTION */}
      <section className="hero" id="home" aria-labelledby="hero-title">
        <div className="hero-copy">
          <p className="eyebrow">ACCESSIBLE EMPLOYMENT FOR EVERYONE</p>
          <h1 id="hero-title">Your ability deserves to be seen.</h1>
          <p className="hero-description">
            Discover opportunities, showcase your strengths, and connect with
            employers who value inclusive talent.
          </p>
          <div className="hero-actions">
            <Link className="btn btn-primary" to="/register?role=candidate">
              Find Opportunities
            </Link>
            <Link className="btn btn-secondary" to="/register?role=employer">
              Hire Inclusively
            </Link>
          </div>
          <div className="hero-highlights" aria-label="Key platform qualities">
            <span className="hero-pill">✓ Accessible Profiles</span>
            <span className="hero-pill">✓ Inclusive Employers</span>
            <span className="hero-pill">✓ Barrier-Free Matching</span>
          </div>
        </div>

        <div className="hero-visual" aria-hidden="true">
          <div className="visual-panel">
            <div className="visual-orbit orbit-one" />
            <div className="visual-orbit orbit-two" />

            <div className="visual-card candidate-badge-card">
              <div className="visual-badge-header">
                <span className="visual-avatar">JD</span>
                <div>
                  <span className="visual-name">Candidate Profile</span>
                  <span className="visual-role">Software Engineer</span>
                </div>
              </div>
              <div className="visual-tags">
                <span className="visual-tag">Screen-Reader Ready</span>
                <span className="visual-tag">Remote Work</span>
              </div>
              <span className="visual-status">✓ Skills Verified</span>
            </div>

            <div className="visual-card employer-badge-card">
              <div className="visual-badge-header">
                <span className="visual-avatar avatar-navy">AC</span>
                <div>
                  <span className="visual-name">Inclusive Employer</span>
                  <span className="visual-role">Hiring Active</span>
                </div>
              </div>
              <span className="visual-match">Matched on Ability</span>
              <span className="visual-status status-cyan">★ Equal Opportunity</span>
            </div>

            <div className="visual-dot" />
          </div>
        </div>
      </section>

      {/* 3. ABOUT SECTION */}
      <section
        className="content-section about-section"
        id="about"
        tabIndex="-1"
        aria-labelledby="about-title"
      >
        <div className="section-header">
          <p className="eyebrow">ABOUT NEXABILITY</p>
          <h2 id="about-title">A better way to connect talent and opportunity.</h2>
          <p className="section-intro">
            NexAbility connects job seekers with inclusive employers through
            accessible digital experiences.
          </p>
        </div>

        <div className="about-pillars">
          <div className="pillar-card">
            <div className="pillar-icon" aria-hidden="true">♿</div>
            <h3>Universal Accessibility</h3>
            <p>
              Designed from the ground up to exceed accessibility standards,
              ensuring every candidate can navigate and apply with dignity.
            </p>
          </div>
          <div className="pillar-card">
            <div className="pillar-icon" aria-hidden="true">🎯</div>
            <h3>Strengths-Based Matching</h3>
            <p>
              Focusing on your real abilities, unique perspectives, and practical
              skills to match you with teams that empower your growth.
            </p>
          </div>
          <div className="pillar-card">
            <div className="pillar-icon" aria-hidden="true">🤝</div>
            <h3>Committed Employers</h3>
            <p>
              Partnering only with organizations genuinely dedicated to inclusive
              workplace culture, accommodations, and equal career advancement.
            </p>
          </div>
        </div>
      </section>

      {/* 4. HOW NEXABILITY WORKS */}
      <section
        className="content-section how-section"
        id="how-it-works"
        tabIndex="-1"
        aria-labelledby="how-title"
      >
        <div className="section-header">
          <p className="eyebrow">HOW IT WORKS</p>
          <h2 id="how-title">How NexAbility works</h2>
          <p className="section-intro">
            A simple path from profile to placement.
          </p>
        </div>

        <ol className="step-grid">
          <li className="step-card">
            <div className="step-badge">
              <span className="step-number" aria-hidden="true">1</span>
              <span className="step-label">Step One</span>
            </div>
            <h3>Create Your Profile</h3>
            <p>Build an accessible profile and showcase your strengths.</p>
          </li>

          <li className="step-card">
            <div className="step-badge">
              <span className="step-number" aria-hidden="true">2</span>
              <span className="step-label">Step Two</span>
            </div>
            <h3>Discover Opportunities</h3>
            <p>Explore opportunities that match your abilities.</p>
          </li>

          <li className="step-card">
            <div className="step-badge">
              <span className="step-number" aria-hidden="true">3</span>
              <span className="step-label">Step Three</span>
            </div>
            <h3>Get Hired</h3>
            <p>Connect with employers who value inclusive talent.</p>
          </li>
        </ol>
      </section>

      {/* 5. CANDIDATE AND EMPLOYER SECTIONS */}
      <section
        className="content-section audience-section"
        id="audiences"
        aria-labelledby="audience-title"
      >
        <div className="section-header">
          <p className="eyebrow">BUILT FOR BOTH SIDES OF EMPLOYMENT</p>
          <h2 id="audience-title">Opportunities for Candidates. Solutions for Employers.</h2>
        </div>

        <div className="audience-grid">
          {/* Candidate Card */}
          <article className="audience-card candidate-card" aria-labelledby="candidates-title">
            <div className="audience-badge">FOR JOB SEEKERS</div>
            <h3 id="candidates-title">For Candidates</h3>
            <p className="audience-description">
              Find opportunities, build your profile and explore inclusive
              careers.
            </p>
            <ul className="audience-features" aria-label="Candidate advantages">
              <li>Showcase your unique strengths without technical hurdles</li>
              <li>Filter opportunities by workplace accommodations and accessibility</li>
              <li>Connect directly with verified equal-opportunity employers</li>
            </ul>
            <div className="audience-cta">
              <Link className="btn btn-primary" to="/register?role=candidate">
                Find Opportunities
              </Link>
            </div>
          </article>

          {/* Employer Card */}
          <article className="audience-card employer-card" aria-labelledby="employers-title">
            <div className="audience-badge employer-badge">FOR INCLUSIVE EMPLOYERS</div>
            <h3 id="employers-title">For Employers</h3>
            <p className="audience-description">
              Discover diverse talent and create accessible hiring experiences.
            </p>
            <ul className="audience-features" aria-label="Employer advantages">
              <li>Access an under-leveraged pool of high-performing candidates</li>
              <li>Eliminate digital barriers in your recruitment and interview process</li>
              <li>Foster an authentic culture of inclusion and workplace belonging</li>
            </ul>
            <div className="audience-cta">
              <Link className="btn btn-accent" to="/register?role=employer">
                Hire Inclusively
              </Link>
            </div>
          </article>
        </div>
      </section>

      {/* 8. ACCESSIBILITY SECTION */}
      <section
        className="content-section accessibility-section"
        id="accessibility"
        tabIndex="-1"
        aria-labelledby="accessibility-title"
      >
        <div className="section-header">
          <p className="eyebrow">ACCESSIBILITY</p>
          <h2 id="accessibility-title">Built to be used by everyone.</h2>
          <p className="section-intro">
            Keyboard access, clear language, and screen-reader support are part
            of every NexAbility flow.
          </p>
        </div>

        <div className="accessibility-grid">
          <div className="accessibility-card">
            <h3>Full Keyboard Navigation</h3>
            <p>
              Navigate the entire platform using logical tab order, skip links,
              and high-contrast focus indicators on every control.
            </p>
          </div>
          <div className="accessibility-card">
            <h3>Assistive Tech Compatible</h3>
            <p>
              Built with semantic HTML landmarks, live ARIA regions, and clear
              descriptive labels for screen-reader users.
            </p>
          </div>
          <div className="accessibility-card">
            <h3>WCAG 2.2 AA Contrast</h3>
            <p>
              Every text element and control meets or exceeds standard color contrast
              ratios with support for system reduced-motion preferences.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export default HomePage;
