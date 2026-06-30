import { ChevronDown } from "lucide-react";
import type { ReactNode } from "react";
import { useState } from "react";

type CollapsibleSectionProps = {
  children: ReactNode;
  defaultOpen?: boolean;
  title: string;
};

export function CollapsibleSection({
  children,
  defaultOpen = true,
  title,
}: CollapsibleSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="collapsible">
      <button
        className="collapsible-trigger"
        onClick={() => setIsOpen((current) => !current)}
        type="button"
      >
        <span>{title}</span>
        <ChevronDown
          aria-hidden="true"
          className={isOpen ? "chevron chevron-open" : "chevron"}
          size={18}
        />
      </button>
      {isOpen ? <div className="collapsible-body">{children}</div> : null}
    </div>
  );
}
