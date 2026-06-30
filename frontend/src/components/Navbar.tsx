import { LogOut, Search } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { Button } from "./ui/Button";

export function Navbar() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <header className="navbar">
      <div className="navbar-title">
        <p className="eyebrow">Workspace</p>
        <h1>AI Resume Analyzer</h1>
      </div>
      <div className="navbar-search">
        <Search aria-hidden="true" size={16} />
        <span>Search resumes, roles, and insights</span>
      </div>
      <div className="navbar-actions">
        {user ? <span className="user-email">{user.email}</span> : null}
        <Button
          icon={<LogOut aria-hidden="true" size={16} />}
          onClick={handleLogout}
          variant="secondary"
        >
          Logout
        </Button>
      </div>
    </header>
  );
}
