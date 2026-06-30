import { Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <main className="auth-shell">
      <section className="auth-panel">
        <div className="brand-block">
          <span className="brand-mark">AR</span>
          <div>
            <h1>AI Resume Analyzer</h1>
            <p>Sign in to continue.</p>
          </div>
        </div>
        <Outlet />
      </section>
    </main>
  );
}
