import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  icon?: ReactNode;
  isLoading?: boolean;
  variant?: "primary" | "secondary" | "ghost";
};

export function Button({
  children,
  className = "",
  disabled,
  icon,
  isLoading = false,
  variant = "primary",
  ...props
}: ButtonProps) {
  return (
    <button
      className={`button button-${variant} ${className}`.trim()}
      {...props}
      disabled={isLoading || disabled}
    >
      {icon ? <span className="button-icon">{icon}</span> : null}
      <span>{isLoading ? "Working..." : children}</span>
    </button>
  );
}
