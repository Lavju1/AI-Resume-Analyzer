import { NavLink } from "react-router-dom";

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="brand-mark">AR</span>
        <span>AI Resume Analyzer</span>
      </div>
      <nav className="sidebar-nav">
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/resumes/upload">Upload Resume</NavLink>
        <NavLink to="/job-matching">Job Matching</NavLink>
      </nav>
    </aside>
  );
}
