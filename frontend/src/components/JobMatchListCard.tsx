import { Card } from "./ui/Card";
import { TagList } from "./ui/TagList";

type JobMatchListCardProps = {
  title: string;
  items: string[];
  tone?: "neutral" | "success" | "warning";
};

export function JobMatchListCard({
  title,
  items,
  tone = "neutral",
}: JobMatchListCardProps) {
  return (
    <Card className="analysis-card">
      <p className="eyebrow">Job Match</p>
      <h2>{title}</h2>
      <TagList items={items} tone={tone} />
    </Card>
  );
}
