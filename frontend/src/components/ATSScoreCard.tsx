import type { ATSScore } from "../types/resume";

type ATSScoreCardProps = {
  atsScore: ATSScore;
};

export function ATSScoreCard({ atsScore }: ATSScoreCardProps) {
  return (
    <section className="panel analysis-card">
      <p className="eyebrow">ATS Score</p>
      <div className="score-row">
        <span className="score-value">{atsScore.overall_score}</span>
        <span className="score-label">/ 100</span>
      </div>
    </section>
  );
}
