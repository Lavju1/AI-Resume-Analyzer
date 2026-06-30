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
    <section className="panel analysis-card">
      <p className="eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      <p className="analysis-summary">{aiAnalysis.summary}</p>
      <AnalysisList title="Strengths" items={aiAnalysis.strengths} />
      <AnalysisList title="Weaknesses" items={aiAnalysis.weaknesses} />
      <AnalysisList title="Recommendations" items={aiAnalysis.recommendations} />
    </section>
  );
}

type AnalysisListProps = {
  title: string;
  items: string[];
};

function AnalysisList({ title, items }: AnalysisListProps) {
  return (
    <div className="analysis-list">
      <h3>{title}</h3>
      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="muted-text">No items returned.</p>
      )}
    </div>
  );
}
