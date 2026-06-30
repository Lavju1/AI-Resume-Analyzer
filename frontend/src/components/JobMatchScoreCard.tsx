import { Target } from "lucide-react";

import { Card } from "./ui/Card";
import { CircularScore } from "./ui/CircularScore";

type JobMatchScoreCardProps = {
  overallMatch: number;
};

export function JobMatchScoreCard({ overallMatch }: JobMatchScoreCardProps) {
  return (
    <Card className="analysis-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Overall Match</p>
          <h2>Role Fit</h2>
        </div>
        <Target aria-hidden="true" size={20} />
      </div>
      <CircularScore label="Match" score={overallMatch} suffix="%" />
    </Card>
  );
}
