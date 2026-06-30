import { AxiosError } from "axios";
import { type FormEvent, useEffect, useState } from "react";
import { BriefcaseBusiness, FileSearch, Play, XCircle } from "lucide-react";

import { AIAnalysisCard } from "../components/AIAnalysisCard";
import { JobMatchListCard } from "../components/JobMatchListCard";
import { JobMatchScoreCard } from "../components/JobMatchScoreCard";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { EmptyState } from "../components/ui/EmptyState";
import { LoadingState } from "../components/ui/LoadingState";
import { jobMatchingService } from "../services/jobMatchingService";
import { resumeService } from "../services/resumeService";
import type { JobMatchResponse } from "../types/jobMatching";
import type { ResumeRead } from "../types/resume";

type ValidationIssue = {
  msg?: string;
};

type BackendError = {
  detail?: string | ValidationIssue[];
};

export function JobMatching() {
  const [resumes, setResumes] = useState<ResumeRead[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [jobMatchResult, setJobMatchResult] = useState<JobMatchResponse | null>(
    null,
  );
  const [isLoadingResumes, setIsLoadingResumes] = useState(true);
  const [isMatching, setIsMatching] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    resumeService
      .listResumes()
      .then((userResumes) => {
        if (!isMounted) {
          return;
        }

        setResumes(userResumes);
        setSelectedResumeId(userResumes[0]?.id ?? "");
      })
      .catch((caughtError) => {
        if (isMounted) {
          setError(getBackendErrorMessage(caughtError));
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoadingResumes(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedResumeId) {
      setError("Select a resume before running job matching.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Paste a job description before running job matching.");
      return;
    }

    setIsMatching(true);
    setError("");
    setJobMatchResult(null);

    try {
      const result = await jobMatchingService.matchResumeToJob({
        resume_id: selectedResumeId,
        job_description_text: jobDescription,
      });
      setJobMatchResult(result);
    } catch (caughtError) {
      setError(getBackendErrorMessage(caughtError));
    } finally {
      setIsMatching(false);
    }
  }

  return (
    <section className="upload-page">
      <Card className="upload-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Job Matching</p>
            <h2>Match Resume to Job</h2>
          </div>
          <BriefcaseBusiness aria-hidden="true" size={22} />
        </div>
        <p className="analysis-summary">
          Select a saved resume, paste the job description, and compare skill
          coverage with AI-assisted role-fit guidance.
        </p>

        {isLoadingResumes ? (
          <LoadingState title="Loading resumes" />
        ) : null}

        {error && (isLoadingResumes || resumes.length === 0) ? (
          <p className="form-error">
            <XCircle aria-hidden="true" size={16} />
            <span>{error}</span>
          </p>
        ) : null}

        {!isLoadingResumes && resumes.length === 0 ? (
          <EmptyState
            description="Upload a resume first so the matcher has a profile to compare."
            title="No resumes available"
          />
        ) : null}

        {!isLoadingResumes && resumes.length > 0 ? (
          <form className="job-match-form" onSubmit={handleSubmit}>
            <label>
              Resume
              <select
                disabled={isMatching}
                onChange={(event) => setSelectedResumeId(event.target.value)}
                value={selectedResumeId}
              >
                {resumes.map((resume) => (
                  <option key={resume.id} value={resume.id}>
                    {resume.original_filename}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Job description
              <textarea
                disabled={isMatching}
                onChange={(event) => setJobDescription(event.target.value)}
                placeholder="Paste the job description here..."
                rows={10}
                value={jobDescription}
              />
            </label>

            {error ? (
              <p className="form-error">
                <XCircle aria-hidden="true" size={16} />
                <span>{error}</span>
              </p>
            ) : null}

            <Button
              disabled={isMatching}
              icon={<Play aria-hidden="true" size={16} />}
              isLoading={isMatching}
            >
              Run job match
            </Button>
          </form>
        ) : null}
      </Card>

      {isMatching ? (
        <Card className="analysis-card">
          <LoadingState
            description="Comparing resume skills, keywords, and AI role-fit signals."
            title="Matching resume"
          />
        </Card>
      ) : null}

      {jobMatchResult ? (
        <div className="analysis-grid">
          <JobMatchScoreCard overallMatch={jobMatchResult.overall_match} />
          <JobMatchListCard
            items={jobMatchResult.matched_skills}
            title="Matched Skills"
            tone="success"
          />
          <JobMatchListCard
            items={jobMatchResult.missing_skills}
            title="Missing Skills"
            tone="warning"
          />
          <JobMatchListCard
            items={jobMatchResult.matched_keywords}
            title="Matched Keywords"
            tone="success"
          />
          <JobMatchListCard
            items={jobMatchResult.missing_keywords}
            title="Missing Keywords"
            tone="warning"
          />
          <AIAnalysisCard
            aiAnalysis={jobMatchResult.ai_analysis}
            eyebrow="AI Job Match"
            title="Role Fit Summary"
          />
        </div>
      ) : !isMatching && !isLoadingResumes && resumes.length > 0 ? (
        <Card className="analysis-card empty-analysis-card">
          <FileSearch aria-hidden="true" size={28} />
          <h2>Paste a job description to begin.</h2>
          <p className="analysis-summary">
            Results will appear here with match percentage, skill chips,
            keyword coverage, and AI recommendations.
          </p>
        </Card>
      ) : null}
    </section>
  );
}

function getBackendErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    const data = error.response?.data as BackendError | undefined;

    if (typeof data?.detail === "string") {
      return data.detail;
    }

    if (Array.isArray(data?.detail)) {
      return data.detail
        .map((issue) => issue.msg)
        .filter(Boolean)
        .join(" ");
    }
  }

  return "Could not complete job matching.";
}
