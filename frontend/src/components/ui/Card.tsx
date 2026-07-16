import { type ReactNode } from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: ReactNode;
  className?: string;
  gradient?: string;
  hover?: boolean;
  padding?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
}

const paddingStyles = {
  sm: 'p-4',
  md: 'p-5 sm:p-6',
  lg: 'p-6 sm:p-8',
};

export function Card({
  children,
  className = '',
  gradient,
  hover = true,
  padding = 'md',
  onClick,
}: CardProps) {
  const Component = onClick ? motion.div : 'div';
  const motionProps = onClick
    ? {
        whileHover: { scale: 1.01 },
        whileTap: { scale: 0.99 },
        onClick,
      }
    : {};

  return (
    <Component
      className={`
        rounded-2xl bg-surface border border-border/60
        ${hover ? 'hover:border-border-glow/40 hover:bg-surface-light/20 transition-all duration-500' : ''}
        ${onClick ? 'cursor-pointer' : ''}
        ${paddingStyles[padding]}
        relative overflow-hidden group
        ${className}
      `}
      {...motionProps}
    >
      {/* Gradient hover background */}
      {gradient && (
        <div
          className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-[0.03] transition-opacity duration-500`}
        />
      )}
      {/* Shine effect */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
      </div>
      {/* Radial glow */}
      <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-3xl pointer-events-none" />
      <div className="relative z-10">{children}</div>
    </Component>
  );
}

export function CardHeader({
  icon: Icon,
  title,
  subtitle,
  action,
  gradient = 'from-primary to-accent',
}: {
  icon?: React.ComponentType<{ className?: string }>;
  title: string;
  subtitle?: string;
  action?: ReactNode;
  gradient?: string;
}) {
  return (
    <div className="flex items-center justify-between mb-4 sm:mb-5">
      <div className="flex items-center gap-2.5 sm:gap-3">
        {Icon && (
          <div
            className={`w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-gradient-to-br ${gradient} p-1.5 sm:p-2 flex items-center justify-center flex-shrink-0`}
          >
            <Icon className="w-full h-full text-white" />
          </div>
        )}
        <div>
          <h3 className="text-sm sm:text-base font-semibold text-text-heading">{title}</h3>
          {subtitle && (
            <p className="text-xs sm:text-sm text-text-muted mt-0.5">{subtitle}</p>
          )}
        </div>
      </div>
      {action && <div className="flex-shrink-0">{action}</div>}
    </div>
  );
}
