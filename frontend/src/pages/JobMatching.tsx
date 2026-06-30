import { AxiosError } from "axios";
import { type FormEvent, useEffect, useState } from "react";

import { AIAnalysisCard } from "../components/AIAnalysisCard";
import { JobMatchListCard } from "../components/JobMatchListCard";
import { JobMatchScoreCard } from "../components/JobMatchScoreCard";
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
      <div className="panel upload-panel">
        <p className="eyebrow">Job Matching</p>
        <h2>Match Resume to Job</h2>

        {isLoadingResumes ? (
          <p className="analysis-summary">Loading resumes...</p>
        ) : null}

        {!isLoadingResumes && resumes.length === 0 ? (
          <p className="empty-state">
            Upload a resume before running job matching.
          </p>
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

            {error ? <p className="form-error">{error}</p> : null}

            <button className="button button-primary" disabled={isMatching}>
              {isMatching ? "Matching..." : "Run job match"}
            </button>
          </form>
        ) : null}
      </div>

      {isMatching ? (
        <div className="panel analysis-card">
          <p className="eyebrow">Analysis</p>
          <h2>Matching resume...</h2>
          <p className="analysis-summary">
            Comparing your resume against the job description.
          </p>
        </div>
      ) : null}

      {jobMatchResult ? (
        <div className="analysis-grid">
          <JobMatchScoreCard overallMatch={jobMatchResult.overall_match} />
          <JobMatchListCard
            items={jobMatchResult.matched_skills}
            title="Matched Skills"
          />
          <JobMatchListCard
            items={jobMatchResult.missing_skills}
            title="Missing Skills"
          />
          <JobMatchListCard
            items={jobMatchResult.matched_keywords}
            title="Matched Keywords"
          />
          <JobMatchListCard
            items={jobMatchResult.missing_keywords}
            title="Missing Keywords"
          />
          <AIAnalysisCard
            aiAnalysis={jobMatchResult.ai_analysis}
            eyebrow="AI Job Match"
            title="AI Job Match Summary"
          />
        </div>
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
