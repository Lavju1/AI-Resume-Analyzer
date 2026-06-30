type JobMatchListCardProps = {
  title: string;
  items: string[];
};

export function JobMatchListCard({ title, items }: JobMatchListCardProps) {
  return (
    <section className="panel analysis-card">
      <p className="eyebrow">Job Match</p>
      <h2>{title}</h2>
      {items.length > 0 ? (
        <ul className="match-list">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="muted-text">No items returned.</p>
      )}
    </section>
  );
}
