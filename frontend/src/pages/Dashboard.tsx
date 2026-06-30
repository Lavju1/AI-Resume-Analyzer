import { BarChart3, BriefcaseBusiness, FileText, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { resumeService } from "../services/resumeService";
import type { ResumeRead } from "../types/resume";
import { Card } from "../components/ui/Card";
import { LoadingState } from "../components/ui/LoadingState";
import { StatCard } from "../components/ui/StatCard";

export function Dashboard() {
  const { user } = useAuth();
  const [resumes, setResumes] = useState<ResumeRead[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    resumeService
      .listResumes()
      .then((userResumes) => {
        if (isMounted) {
          setResumes(userResumes);
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <section className="dashboard-page">
      <Card className="hero-panel">
        <div>
          <p className="eyebrow">Welcome back</p>
          <h2>Build sharper resumes with AI-assisted feedback.</h2>
          <p>
            Upload resumes, review ATS readiness, and compare your profile to
            specific job descriptions from one focused workspace.
          </p>
        </div>
        <div className="hero-actions">
          <Link className="button button-primary" to="/resumes/upload">
            <FileText aria-hidden="true" size={16} />
            <span>Upload resume</span>
          </Link>
          <Link className="button button-secondary" to="/job-matching">
            <BriefcaseBusiness aria-hidden="true" size={16} />
            <span>Match a job</span>
          </Link>
        </div>
      </Card>

      <div className="stat-grid">
        <StatCard
          icon={<FileText aria-hidden="true" size={20} />}
          label="Uploaded resumes"
          value={isLoading ? "..." : String(resumes.length)}
        />
        <StatCard
          icon={<BarChart3 aria-hidden="true" size={20} />}
          label="ATS analyses"
          value={isLoading ? "..." : String(resumes.length)}
        />
        <StatCard
          icon={<Sparkles aria-hidden="true" size={20} />}
          label="AI insights"
          value="Ready"
        />
      </div>

      <Card className="activity-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Recent activity</p>
            <h2>Resume workspace</h2>
          </div>
          <span className="user-email">{user?.email}</span>
        </div>

        {isLoading ? (
          <LoadingState title="Loading workspace" />
        ) : resumes.length > 0 ? (
          <div className="resume-table">
            {resumes.slice(0, 5).map((resume) => (
              <div className="resume-row" key={resume.id}>
                <div>
                  <strong>{resume.original_filename}</strong>
                  <span>{resume.content_type}</span>
                </div>
                <span className="tag tag-neutral">{resume.upload_status}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="muted-text">
            No resumes yet. Upload your first resume to unlock ATS and AI
            insights.
          </p>
        )}
      </Card>
    </section>
  );
}
