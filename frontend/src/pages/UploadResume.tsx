import { AxiosError } from "axios";
import {
  type ChangeEvent,
  type DragEvent,
  type FormEvent,
  useRef,
  useState,
} from "react";
import { CheckCircle2, FileText, UploadCloud, XCircle } from "lucide-react";

import { AIAnalysisCard } from "../components/AIAnalysisCard";
import { ATSScoreCard } from "../components/ATSScoreCard";
import { ResumeFeedbackCard } from "../components/ResumeFeedbackCard";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { LoadingState } from "../components/ui/LoadingState";
import { resumeService } from "../services/resumeService";
import type { ResumeUploadResponse } from "../types/resume";

type ValidationIssue = {
  msg?: string;
};

type BackendError = {
  detail?: string | ValidationIssue[];
};

export function UploadResume() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState("");
  const [uploadResult, setUploadResult] =
    useState<ResumeUploadResponse | null>(null);

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    selectFile(file);
  }

  function selectFile(file: File | null) {
    setSelectedFile(file);
    setUploadProgress(0);
    setError("");
    setUploadResult(null);
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    setIsDragging(false);
    selectFile(event.dataTransfer.files?.[0] ?? null);
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
      <Card className="upload-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Resume</p>
            <h2>Upload Resume</h2>
          </div>
          <UploadCloud aria-hidden="true" size={22} />
        </div>
        <p className="analysis-summary">
          Drop in a PDF or DOCX resume and get ATS feedback plus AI analysis in
          one pass.
        </p>

        <form className="upload-form" onSubmit={handleSubmit}>
          <label
            className={isDragging ? "file-picker file-picker-active" : "file-picker"}
            onDragLeave={() => setIsDragging(false)}
            onDragOver={(event) => {
              event.preventDefault();
              setIsDragging(true);
            }}
            onDrop={handleDrop}
          >
            <span className="file-picker-icon">
              <UploadCloud aria-hidden="true" size={26} />
            </span>
            <strong>Drag and drop your resume</strong>
            <span>PDF or DOCX, up to the backend upload limit.</span>
            <input
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              disabled={isUploading}
              ref={fileInputRef}
              onChange={handleFileChange}
              type="file"
            />
          </label>

          <div className="selected-file">
            <FileText aria-hidden="true" size={18} />
            <span>{selectedFile ? selectedFile.name : "No file selected"}</span>
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

          {error ? (
            <p className="form-error">
              <XCircle aria-hidden="true" size={16} />
              <span>{error}</span>
            </p>
          ) : null}

          {uploadResult ? (
            <p className="form-success">
              <CheckCircle2 aria-hidden="true" size={16} />
              <span>
                {uploadResult.resume.original_filename} uploaded successfully.
              </span>
            </p>
          ) : null}

          <Button
            disabled={isUploading || !selectedFile}
            icon={<UploadCloud aria-hidden="true" size={16} />}
            isLoading={isUploading}
          >
            Upload resume
          </Button>
        </form>
      </Card>

      {isUploading ? (
        <Card className="analysis-card">
          <LoadingState
            description="Parsing the document, calculating ATS readiness, and preparing AI insights."
            title="Analyzing resume"
          />
        </Card>
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

  return "Could not upload resume.";
}
