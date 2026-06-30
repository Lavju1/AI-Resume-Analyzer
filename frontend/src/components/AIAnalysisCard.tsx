import type { AIAnalysis } from "../types/resume";

type AIAnalysisCardProps = {
  aiAnalysis: AIAnalysis;
};

export function AIAnalysisCard({ aiAnalysis }: AIAnalysisCardProps) {
  return (
    <section className="panel analysis-card">
      <p className="eyebrow">AI Analysis</p>
      <h2>Professional Summary</h2>
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
