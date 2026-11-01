import { Link } from "react-router-dom";

function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="site-footer-inner">
        <div className="footer-brand">
          <Link className="brand" to="/" aria-label="NexAbility Home">
            <img
              className="brand-logo"
              src="/assets/nexability-logo.png"
              alt="NexAbility"
              width="180"
              height="90"
            />
          </Link>
          <p className="footer-tagline">
            Accessible employment platform connecting candidates with inclusive employers.
          </p>
        </div>

        <nav className="footer-nav" aria-label="Footer links">
          <div className="footer-nav-col">
            <span className="footer-heading">Platform</span>
            <Link to="/register?role=candidate">For Candidates</Link>
            <Link to="/register?role=employer">For Employers</Link>
            <a href="/#how-it-works">How It Works</a>
          </div>

          <div className="footer-nav-col">
            <span className="footer-heading">About & Access</span>
            <a href="/#about">About NexAbility</a>
            <a href="/#accessibility">Accessibility</a>
          </div>

          <div className="footer-nav-col">
            <span className="footer-heading">Account</span>
            <Link to="/login">Sign In</Link>
            <Link to="/register">Get Started</Link>
            <Link to="/candidate/settings">Candidate Settings</Link>
          </div>
        </nav>
      </div>

      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} NexAbility. Accessible employment for everyone.</p>
        <p>Built to WCAG 2.2 AA accessibility standards.</p>
      </div>
    </footer>
  );
}

export default SiteFooter;
