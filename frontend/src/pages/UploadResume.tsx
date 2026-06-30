import { AxiosError } from "axios";
import { type ChangeEvent, type FormEvent, useState } from "react";

import { AIAnalysisCard } from "../components/AIAnalysisCard";
import { ATSScoreCard } from "../components/ATSScoreCard";
import { ResumeFeedbackCard } from "../components/ResumeFeedbackCard";
import { resumeService } from "../services/resumeService";
import type { ResumeUploadResponse } from "../types/resume";

type BackendError = {
  detail?: string;
};

export function UploadResume() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");
  const [uploadResult, setUploadResult] =
    useState<ResumeUploadResponse | null>(null);

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    setSelectedFile(file);
    setUploadProgress(0);
    setError("");
    setUploadResult(null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setError("Select a PDF or DOCX resume before uploading.");
      return;
    }

    setIsUploading(true);
    setError("");
    setUploadResult(null);
    setUploadProgress(0);

    try {
      const result = await resumeService.uploadResume(selectedFile, {
        onUploadProgress: (progressEvent) => {
          if (!progressEvent.total) {
            return;
          }

          setUploadProgress(
            Math.round((progressEvent.loaded * 100) / progressEvent.total),
          );
        },
      });
      setUploadResult(result);
      setUploadProgress(100);
    } catch (caughtError) {
      setError(getUploadErrorMessage(caughtError));
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section className="upload-page">
      <div className="panel upload-panel">
        <p className="eyebrow">Resume</p>
        <h2>Upload Resume</h2>
        <form className="upload-form" onSubmit={handleSubmit}>
          <label className="file-picker">
            <span>Select PDF or DOCX file</span>
            <input
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              disabled={isUploading}
              onChange={handleFileChange}
              type="file"
            />
          </label>

          <div className="selected-file">
            {selectedFile ? selectedFile.name : "No file selected"}
          </div>

          {isUploading ? (
            <div className="progress-group">
              <div className="progress-track">
                <div
                  className="progress-fill"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <span>{uploadProgress}%</span>
            </div>
          ) : null}

          {error ? <p className="form-error">{error}</p> : null}

          {uploadResult ? (
            <p className="form-success">
              {uploadResult.resume.original_filename} uploaded successfully.
            </p>
          ) : null}

          <button
            className="button button-primary"
            disabled={isUploading || !selectedFile}
          >
            {isUploading ? "Uploading..." : "Upload resume"}
          </button>
        </form>
      </div>

      {isUploading ? (
        <div className="panel analysis-card">
          <p className="eyebrow">Analysis</p>
          <h2>Analyzing resume...</h2>
          <p className="analysis-summary">
            Your resume is being parsed and analyzed.
          </p>
        </div>
      ) : null}

      {uploadResult ? (
        <div className="analysis-grid">
          <ATSScoreCard atsScore={uploadResult.ats_score} />
          <ResumeFeedbackCard feedback={uploadResult.feedback} />
          <AIAnalysisCard aiAnalysis={uploadResult.ai_analysis} />
        </div>
      ) : null}
    </section>
  );
}

function getUploadErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    const data = error.response?.data as BackendError | BackendError[] | undefined;

    if (Array.isArray(data)) {
      return data
        .map((item) => item.detail)
        .filter(Boolean)
        .join(" ");
    }

    if (typeof data?.detail === "string") {
      return data.detail;
    }
  }

  return "Could not upload resume.";
}
