import { useAuth } from "../hooks/useAuth";

export function Dashboard() {
  const { user } = useAuth();

  return (
    <section className="dashboard-grid">
      <div className="panel">
        <p className="eyebrow">Signed in</p>
        <h2>{user?.email}</h2>
        <p>Your workspace is ready.</p>
      </div>
    </section>
  );
}
