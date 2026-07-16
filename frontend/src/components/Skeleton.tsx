import { motion } from 'framer-motion';

interface SkeletonBlockProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  rounded?: string;
}

export function SkeletonBlock({
  className = '',
  width,
  height,
  rounded = 'rounded-xl',
}: SkeletonBlockProps) {
  return (
    <div
      className={`relative overflow-hidden bg-surface-light/60 ${rounded} ${className}`}
      style={{ width, height }}
    >
      <motion.div
        className="absolute inset-0 -translate-x-full"
        animate={{ x: ['0%', '100%', '100%'] }}
        transition={{
          duration: 1.8,
          repeat: Infinity,
          ease: [0.25, 0.46, 0.45, 0.94],
          repeatDelay: 0.6,
        }}
      >
        <div className="h-full w-1/2 bg-gradient-to-r from-transparent via-white/[0.06] to-transparent skew-x-12" />
      </motion.div>
    </div>
  );
}

export function SkeletonCircle({ size = 40 }: { size?: number }) {
  return (
    <SkeletonBlock
      width={size}
      height={size}
      rounded="rounded-full"
    />
  );
}

export function SkeletonText({
  lines = 3,
  lastWidth = '60%',
  className = '',
}: {
  lines?: number;
  lastWidth?: string;
  className?: string;
}) {
  return (
    <div className={`space-y-2.5 ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <SkeletonBlock
          key={i}
          height={14}
          width={i === lines - 1 ? lastWidth : '100%'}
          rounded="rounded-md"
        />
      ))}
    </div>
  );
}

export function SkeletonCard({ className = '' }: { className?: string }) {
  return (
    <div className={`p-5 rounded-2xl bg-surface border border-border/40 ${className}`}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0 space-y-3">
          <div className="flex items-center gap-2.5">
            <SkeletonBlock height={16} width="45%" rounded="rounded-md" />
            <SkeletonBlock height={22} width={60} rounded="rounded-lg" />
          </div>
          <SkeletonText lines={2} lastWidth="40%" />
        </div>
        <div className="flex gap-1.5 flex-shrink-0">
          <SkeletonBlock width={36} height={36} rounded="rounded-xl" />
          <SkeletonBlock width={36} height={36} rounded="rounded-xl" />
        </div>
      </div>
    </div>
  );
}

export function SkeletonStatCard({ className = '' }: { className?: string }) {
  return (
    <div className={`p-5 rounded-2xl bg-surface border border-border/40 ${className}`}>
      <div className="space-y-3.5">
        <SkeletonBlock width={40} height={40} rounded="rounded-xl" />
        <SkeletonBlock height={32} width="50%" rounded="rounded-md" />
        <SkeletonBlock height={14} width="35%" rounded="rounded-md" />
      </div>
    </div>
  );
}
