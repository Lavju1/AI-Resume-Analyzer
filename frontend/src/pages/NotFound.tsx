import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <main className="centered-page">
      <section className="not-found">
        <p className="eyebrow">404</p>
        <h1>Page not found</h1>
        <Link className="button button-primary" to="/dashboard">
          Back to dashboard
        </Link>
      </section>
    </main>
  );
}
