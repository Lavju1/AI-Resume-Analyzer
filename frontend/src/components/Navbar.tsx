import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

export function Navbar() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <header className="navbar">
      <div>
        <p className="eyebrow">Workspace</p>
        <h1>Dashboard</h1>
      </div>
      <div className="navbar-actions">
        {user ? <span className="user-email">{user.email}</span> : null}
        <button className="button button-secondary" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}
