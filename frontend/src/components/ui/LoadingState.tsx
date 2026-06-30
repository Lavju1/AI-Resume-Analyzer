type LoadingStateProps = {
  description?: string;
  title: string;
};

export function LoadingState({ description, title }: LoadingStateProps) {
  return (
    <div className="loading-state">
      <span className="loading-spinner" />
      <div>
        <h3>{title}</h3>
        {description ? <p>{description}</p> : null}
      </div>
    </div>
  );
}
