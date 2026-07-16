import { motion } from 'framer-motion';
import { SkeletonBlock, SkeletonCard, SkeletonStatCard } from './Skeleton';

function SkeletonHeader({ hasBadge = false }: { hasBadge?: boolean }) {
  return (
    <div className="flex items-center justify-between">
      <div className="space-y-2">
        <div className="flex items-center gap-3">
          <SkeletonBlock height={32} width={180} rounded="rounded-lg" />
          {hasBadge && <SkeletonBlock height={22} width={48} rounded="rounded-full" />}
        </div>
        <SkeletonBlock height={14} width={260} rounded="rounded-md" />
      </div>
      <SkeletonBlock width={120} height={40} rounded="rounded-xl" />
    </div>
  );
}

function SkeletonSearchBar() {
  return (
    <div className="relative">
      <SkeletonBlock height={48} width="100%" rounded="rounded-2xl" />
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-between"
      >
        <div>
          <div className="flex items-center gap-3 mb-2">
            <SkeletonBlock height={32} width={160} rounded="rounded-lg" />
            <SkeletonBlock height={22} width={44} rounded="rounded-full" />
          </div>
          <SkeletonBlock height={14} width={240} rounded="rounded-md" />
        </div>
        <SkeletonBlock width={72} height={28} rounded="rounded-full" />
      </motion.div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {[1, 2, 3, 4].map((i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
          >
            <SkeletonStatCard />
          </motion.div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-5">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="p-5 sm:p-6 rounded-2xl bg-surface border border-border/60"
        >
          <div className="flex items-center gap-2.5 mb-5">
            <SkeletonBlock width={28} height={28} rounded="rounded-lg" />
            <SkeletonBlock height={18} width={100} rounded="rounded-md" />
          </div>
          <div className="space-y-2.5">
            {[1, 2, 3, 4, 5].map((i) => (
              <SkeletonCard key={i} />
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.25 }}
          className="p-5 sm:p-6 rounded-2xl bg-surface border border-border/60"
        >
          <div className="flex items-center gap-2.5 mb-5">
            <SkeletonBlock width={28} height={28} rounded="rounded-lg" />
            <SkeletonBlock height={18} width={130} rounded="rounded-md" />
          </div>
          <div className="space-y-2.5">
            {[1, 2, 3, 4, 5].map((i) => (
              <SkeletonCard key={i} />
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

function ListPageSkeleton() {
  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <SkeletonHeader />
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
      >
        <SkeletonSearchBar />
      </motion.div>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="grid gap-3.5"
      >
        {[1, 2, 3, 4].map((i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
          >
            <SkeletonCard />
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}

function ResumesSkeleton() {
  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <SkeletonHeader />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
      >
        <div className="p-10 sm:p-14 rounded-2xl border-2 border-dashed border-border/40 bg-surface">
          <div className="flex flex-col items-center gap-4">
            <SkeletonBlock width={64} height={64} rounded="rounded-2xl" />
            <SkeletonBlock height={18} width={140} rounded="rounded-md" />
            <SkeletonBlock height={14} width={260} rounded="rounded-md" />
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="grid gap-3.5"
      >
        {[1, 2, 3].map((i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
            className="p-5 rounded-2xl bg-surface border border-border/60"
          >
            <div className="flex items-center gap-4">
              <SkeletonBlock width={48} height={48} rounded="rounded-xl" />
              <div className="flex-1 space-y-2.5">
                <SkeletonBlock height={16} width="40%" rounded="rounded-md" />
                <div className="flex gap-2.5">
                  <SkeletonBlock height={22} width={80} rounded="rounded-lg" />
                  <SkeletonBlock height={22} width={60} rounded="rounded-lg" />
                  <SkeletonBlock height={22} width={100} rounded="rounded-lg" />
                </div>
              </div>
              <div className="flex gap-1.5">
                <SkeletonBlock width={36} height={36} rounded="rounded-xl" />
                <SkeletonBlock width={36} height={36} rounded="rounded-xl" />
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}

function AIPageSkeleton() {
  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="flex items-center gap-3 mb-2">
          <SkeletonBlock width={40} height={40} rounded="rounded-xl" />
          <div>
            <SkeletonBlock height={32} width={120} rounded="rounded-lg" />
            <SkeletonBlock height={14} width={300} rounded="rounded-md" className="mt-1" />
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
      >
        <div className="flex gap-3 p-1.5 rounded-2xl bg-surface border border-border/40 w-fit">
          <SkeletonBlock width={180} height={44} rounded="rounded-xl" />
          <SkeletonBlock width={180} height={44} rounded="rounded-xl" />
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid lg:grid-cols-2 gap-5"
      >
        <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
          <div className="flex items-center gap-2.5 mb-5">
            <SkeletonBlock width={32} height={32} rounded="rounded-lg" />
            <SkeletonBlock height={18} width={160} rounded="rounded-md" />
          </div>
          <div className="space-y-4">
            <SkeletonBlock height={140} width="100%" rounded="rounded-xl" />
            <SkeletonBlock height={140} width="100%" rounded="rounded-xl" />
            <SkeletonBlock height={48} width="100%" rounded="rounded-xl" />
          </div>
        </div>
        <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
          <div className="flex items-center gap-2.5 mb-5">
            <SkeletonBlock width={32} height={32} rounded="rounded-lg" />
            <SkeletonBlock height={18} width={130} rounded="rounded-md" />
          </div>
          <div className="flex flex-col items-center justify-center h-[380px]">
            <SkeletonBlock width={64} height={64} rounded="rounded-2xl" />
            <SkeletonBlock height={14} width={200} rounded="rounded-md" className="mt-4" />
            <SkeletonBlock height={12} width={150} rounded="rounded-md" className="mt-1" />
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export function PageSkeleton({ route }: { route: string }) {
  if (route.startsWith('/dashboard')) return <DashboardSkeleton />;
  if (route.startsWith('/resumes')) return <ResumesSkeleton />;
  if (route.startsWith('/ai')) return <AIPageSkeleton />;
  // Jobs, Applications, and any other list pages
  return <ListPageSkeleton />;
}
