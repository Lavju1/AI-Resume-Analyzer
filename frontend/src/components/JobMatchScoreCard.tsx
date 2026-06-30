type JobMatchScoreCardProps = {
  overallMatch: number;
};

export function JobMatchScoreCard({ overallMatch }: JobMatchScoreCardProps) {
  return (
    <section className="panel analysis-card">
      <p className="eyebrow">Overall Match</p>
      <div className="score-row">
        <span className="score-value">{overallMatch}</span>
        <span className="score-label">%</span>
      </div>
    </section>
  );
}
