import type { ResumeFeedback } from "../types/resume";

type ResumeFeedbackCardProps = {
  feedback: ResumeFeedback;
};

export function ResumeFeedbackCard({ feedback }: ResumeFeedbackCardProps) {
  return (
    <section className="panel analysis-card">
      <p className="eyebrow">Feedback</p>
      <h2>Resume Feedback</h2>
      <p className="analysis-summary">{feedback.overall_summary}</p>
      <div className="feedback-list">
        {feedback.feedback.map((item) => (
          <article className="feedback-item" key={`${item.category}-${item.title}`}>
            <span className={`severity-pill severity-${item.severity}`}>
              {item.severity}
            </span>
            <div>
              <h3>{item.title}</h3>
              <p>{item.message}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
