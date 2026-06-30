import type { CSSProperties } from "react";

type CircularScoreProps = {
  label: string;
  score: number;
  suffix?: string;
};

export function CircularScore({ label, score, suffix = "" }: CircularScoreProps) {
  const normalizedScore = Math.max(0, Math.min(100, Math.round(score)));
  const tone =
    normalizedScore >= 80 ? "good" : normalizedScore >= 60 ? "medium" : "low";

  return (
    <div
      className={`circular-score circular-score-${tone}`}
      style={{ "--score": normalizedScore } as CSSProperties}
    >
      <div className="circular-score-inner">
        <strong>
          {normalizedScore}
          {suffix}
        </strong>
        <span>{label}</span>
      </div>
    </div>
  );
}
