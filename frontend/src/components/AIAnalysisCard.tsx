import { Lightbulb, Sparkles, Target, TriangleAlert } from "lucide-react";
import type { ReactNode } from "react";

import { Card } from "./ui/Card";
import { CollapsibleSection } from "./ui/CollapsibleSection";
import type { AIAnalysis } from "../types/resume";

type AIAnalysisCardProps = {
  aiAnalysis: AIAnalysis;
  eyebrow?: string;
  title?: string;
};

export function AIAnalysisCard({
  aiAnalysis,
  eyebrow = "AI Analysis",
  title = "Professional Summary",
}: AIAnalysisCardProps) {
  return (
    <Card className="analysis-card ai-analysis-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">{eyebrow}</p>
          <h2>{title}</h2>
        </div>
        <Sparkles aria-hidden="true" size={20} />
      </div>

      <CollapsibleSection title="Summary">
        <p className="analysis-summary">{aiAnalysis.summary}</p>
      </CollapsibleSection>

      <div className="insight-card-grid">
        <AnalysisList
          icon={<Target aria-hidden="true" size={18} />}
          items={aiAnalysis.strengths}
          title="Strengths"
          tone="success"
        />
        <AnalysisList
          icon={<TriangleAlert aria-hidden="true" size={18} />}
          items={aiAnalysis.weaknesses}
          title="Weaknesses"
          tone="warning"
        />
        <AnalysisList
          icon={<Lightbulb aria-hidden="true" size={18} />}
          items={aiAnalysis.recommendations}
          title="Recommendations"
          tone="neutral"
        />
      </div>
    </Card>
  );
}

type AnalysisListProps = {
  icon: ReactNode;
  title: string;
  items: string[];
  tone: "neutral" | "success" | "warning";
};

function AnalysisList({ icon, title, items, tone }: AnalysisListProps) {
  return (
    <div className={`insight-card insight-card-${tone}`}>
      <div className="insight-card-heading">
        {icon}
        <h3>{title}</h3>
      </div>
      <CollapsibleSection defaultOpen={items.length <= 4} title="Details">
        {items.length > 0 ? (
          <ul>
            {items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted-text">No items returned.</p>
        )}
      </CollapsibleSection>
    </div>
  );
}
