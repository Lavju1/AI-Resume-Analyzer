import { BarChart3, BriefcaseBusiness, FileUp } from "lucide-react";
import { NavLink } from "react-router-dom";

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="brand-mark">AR</span>
        <div>
          <strong>AI Resume</strong>
          <span>Analyzer</span>
        </div>
      </div>
      <nav className="sidebar-nav">
        <NavLink to="/dashboard">
          <BarChart3 aria-hidden="true" size={18} />
          Dashboard
        </NavLink>
        <NavLink to="/resumes/upload">
          <FileUp aria-hidden="true" size={18} />
          Upload Resume
        </NavLink>
        <NavLink to="/job-matching">
          <BriefcaseBusiness aria-hidden="true" size={18} />
          Job Matching
        </NavLink>
      </nav>
    </aside>
  );
}
