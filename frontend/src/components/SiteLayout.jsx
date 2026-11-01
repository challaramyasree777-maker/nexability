import { useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import SiteFooter from "./SiteFooter.jsx";
import SiteHeader from "./SiteHeader.jsx";

function SiteLayout() {
  const location = useLocation();

  useEffect(() => {
    if (location.hash) {
      const target = document.getElementById(location.hash.slice(1));
      target?.focus?.();
      target?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    const main = document.getElementById("main-content");
    main?.focus();
    window.scrollTo(0, 0);
  }, [location.pathname, location.hash]);

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <SiteHeader />
      <Outlet />
      <SiteFooter />
    </div>
  );
}

export default SiteLayout;
