type TagListProps = {
  emptyLabel?: string;
  items: string[];
  tone?: "neutral" | "success" | "warning";
};

export function TagList({
  emptyLabel = "No items returned.",
  items,
  tone = "neutral",
}: TagListProps) {
  if (items.length === 0) {
    return <p className="muted-text">{emptyLabel}</p>;
  }

  return (
    <div className="tag-list">
      {items.map((item) => (
        <span className={`tag tag-${tone}`} key={item}>
          {item}
        </span>
      ))}
    </div>
  );
}
