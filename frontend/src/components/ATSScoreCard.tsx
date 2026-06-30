import { Activity, AlertTriangle, CheckCircle2 } from "lucide-react";

import { Card } from "./ui/Card";
import { CircularScore } from "./ui/CircularScore";
import type { ATSScore } from "../types/resume";

type ATSScoreCardProps = {
  atsScore: ATSScore;
};

const CATEGORY_LABELS: Record<keyof ATSScore["section_scores"], string> = {
  action_verbs: "Action Verbs",
  contact_information: "Contact Information",
  education: "Education",
  experience: "Experience",
  formatting: "Formatting",
  keywords: "Keywords",
  professional_summary: "Professional Summary",
  projects: "Projects",
  quantified_achievements: "Quantified Achievements",
  skills: "Skills",
};

export function ATSScoreCard({ atsScore }: ATSScoreCardProps) {
  const categories = Object.entries(atsScore.section_scores) as Array<
    [keyof ATSScore["section_scores"], ATSScore["section_scores"][keyof ATSScore["section_scores"]]]
  >;

  return (
    <Card className="analysis-card ats-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">ATS Analysis</p>
          <h2>Resume Readiness</h2>
        </div>
        <Activity aria-hidden="true" size={20} />
      </div>

      <div className="ats-overview">
        <CircularScore label="ATS score" score={atsScore.overall_score} />
        <div className="ats-copy">
          <p>
            Weighted scoring checks resume completeness, keyword depth, action
            verbs, measurable impact, and ATS-friendly formatting.
          </p>
        </div>
      </div>

      <div className="category-grid">
        {categories.map(([key, category]) => {
          const percentage = Math.round(
            (category.score / category.max_score) * 100,
          );
          const tone =
            percentage >= 80 ? "good" : percentage >= 60 ? "medium" : "low";

          return (
            <article className="category-card" key={key}>
              <div className="category-header">
                <span>{CATEGORY_LABELS[key]}</span>
                <strong>
                  {category.score}/{category.max_score}
                </strong>
              </div>
              <div className="progress-track">
                <div
                  className={`progress-fill progress-fill-${tone}`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
              <p>{category.feedback}</p>
            </article>
          );
        })}
      </div>

      <div className="feedback-list compact-list">
        {atsScore.strengths.slice(0, 3).map((strength) => (
          <div className="inline-insight success-insight" key={strength}>
            <CheckCircle2 aria-hidden="true" size={16} />
            <span>{strength}</span>
          </div>
        ))}
        {atsScore.weaknesses.slice(0, 3).map((weakness) => (
          <div className="inline-insight warning-insight" key={weakness}>
            <AlertTriangle aria-hidden="true" size={16} />
            <span>{weakness}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
