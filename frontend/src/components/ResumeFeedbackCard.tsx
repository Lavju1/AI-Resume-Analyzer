import { CheckCircle2, Info, TriangleAlert } from "lucide-react";

import { Card } from "./ui/Card";
import type { ResumeFeedback } from "../types/resume";

type ResumeFeedbackCardProps = {
  feedback: ResumeFeedback;
};

export function ResumeFeedbackCard({ feedback }: ResumeFeedbackCardProps) {
  return (
    <Card className="analysis-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Feedback</p>
          <h2>Resume Feedback</h2>
        </div>
        <Info aria-hidden="true" size={20} />
      </div>
      <p className="analysis-summary">{feedback.overall_summary}</p>
      <div className="feedback-list">
        {feedback.feedback.map((item) => (
          <article className="feedback-item" key={`${item.category}-${item.title}`}>
            <span className={`severity-pill severity-${item.severity}`}>
              {item.severity === "success" ? (
                <CheckCircle2 aria-hidden="true" size={13} />
              ) : item.severity === "warning" ? (
                <TriangleAlert aria-hidden="true" size={13} />
              ) : (
                <Info aria-hidden="true" size={13} />
              )}
              <span>{item.severity}</span>
            </span>
            <div>
              <h3>{item.title}</h3>
              <p>{item.message}</p>
            </div>
          </article>
        ))}
      </div>
    </Card>
  );
}
