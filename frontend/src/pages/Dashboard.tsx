import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Briefcase,
  Send,
  Loader2,
  Eye,
  Zap,
  Activity,
} from 'lucide-react';
import { dashboardApi } from '../api/client';

interface DashboardData {
  stats?: {
    total_jobs?: number;
    total_applications?: number;
    active_applications?: number;
    interviews?: number;
  };
  status_summary?: Record<string, number>;
  recent_jobs?: Array<{ id: number; title: string; company: string; status: string }>;
  recent_applications?: Array<{ id: number; job_title: string; company: string; status: string }>;
}

const statCards = [
  { label: 'Total Jobs', key: 'total_jobs' as const, icon: Briefcase, gradient: 'from-indigo-500 to-purple-600' },
  { label: 'Applications', key: 'total_applications' as const, icon: Send, gradient: 'from-cyan-500 to-blue-600' },
  { label: 'Active', key: 'active_applications' as const, icon: Activity, gradient: 'from-emerald-500 to-teal-600' },
  { label: 'Interviews', key: 'interviews' as const, icon: Eye, gradient: 'from-amber-500 to-orange-600' },
];

const statusBadge: Record<string, string> = {
  saved: 'badge-saved',
  new: 'badge-new',
  applied: 'badge-applied',
  interview: 'badge-interview',
  offer: 'badge-offer',
  rejected: 'badge-rejected',
  accepted: 'badge-accepted',
};

export function Dashboard() {
  const [data, setData] = useState<DashboardData>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      dashboardApi.get().catch(() => ({ data: { data: {} } })),
      dashboardApi.statusSummary().catch(() => ({ data: { data: {} } })),
      dashboardApi.recentJobs().catch(() => ({ data: { data: [] } })),
      dashboardApi.recentApplications().catch(() => ({ data: { data: [] } })),
    ])
      .then(([dash, status, jobs, apps]) => {
        setData({
          stats: dash.data.data,
          status_summary: status.data.data,
          recent_jobs: jobs.data.data,
          recent_applications: apps.data.data,
        });
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 text-primary animate-spin" />
          <p className="text-text-muted text-sm">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const getBadge = (status: string) => statusBadge[status.toLowerCase()] || 'bg-gray-500/20 text-gray-400 border-gray-500/20';

  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-heading flex items-center gap-3">
            Dashboard
            <span className="text-xs font-normal px-2.5 py-0.5 rounded-full bg-primary-light text-primary border border-primary/20">
              v2.0
            </span>
          </h1>
          <p className="text-text-muted mt-1">Overview of your career journey</p>
        </div>
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface border border-border/60 text-xs text-text-muted">
          <Zap className="w-3 h-3 text-primary" />
          Live
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {statCards.map((stat, i) => {
          const value = data.stats?.[stat.key] ?? 0;
          return (
            <motion.div
              key={stat.key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className="group relative p-5 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden"
            >
              {/* Gradient Hover Background */}
              <div className={`absolute inset-0 bg-gradient-to-br ${stat.gradient} opacity-0 group-hover:opacity-[0.03] transition-opacity duration-500`} />
              {/* Shine effect */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />
              </div>

              <div className="relative">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${stat.gradient} p-2.5 mb-3.5 shadow-lg`}>
                  <stat.icon className="w-full h-full text-white" />
                </div>
                <div className="text-2xl sm:text-3xl font-bold text-text-heading mb-0.5">
                  {value}
                </div>
                <div className="text-xs sm:text-sm text-text-muted">{stat.label}</div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Bottom Grid */}
      <div className="grid lg:grid-cols-2 gap-5">
        {/* Recent Jobs */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="p-5 sm:p-6 rounded-2xl bg-surface border border-border/60"
        >
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-base font-semibold text-text-heading flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 p-1.5">
                <Briefcase className="w-full h-full text-white" />
              </div>
              Recent Jobs
            </h2>
            {(!data.recent_jobs || data.recent_jobs.length === 0) && (
              <span className="text-xs text-text-muted">Empty</span>
            )}
          </div>
          <div className="space-y-2.5">
            {data.recent_jobs?.slice(0, 5).map((job) => (
              <div
                key={job.id}
                className="flex items-center justify-between p-3.5 rounded-xl bg-surface-light/30 hover:bg-surface-light/60 border border-border/30 hover:border-border-glow/20 transition-all duration-300"
              >
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-text-heading truncate">{job.title}</p>
                  <p className="text-xs text-text-muted truncate">{job.company}</p>
                </div>
                <span className={`px-2.5 py-1 rounded-lg text-xs font-medium ${getBadge(job.status)}`}>
                  {job.status}
                </span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Recent Applications */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.25 }}
          className="p-5 sm:p-6 rounded-2xl bg-surface border border-border/60"
        >
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-base font-semibold text-text-heading flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 p-1.5">
                <Send className="w-full h-full text-white" />
              </div>
              Recent Applications
            </h2>
            {(!data.recent_applications || data.recent_applications.length === 0) && (
              <span className="text-xs text-text-muted">Empty</span>
            )}
          </div>
          <div className="space-y-2.5">
            {data.recent_applications?.slice(0, 5).map((app) => (
              <div
                key={app.id}
                className="flex items-center justify-between p-3.5 rounded-xl bg-surface-light/30 hover:bg-surface-light/60 border border-border/30 hover:border-border-glow/20 transition-all duration-300"
              >
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-text-heading truncate">
                    {app.job_title || `Application #${app.id}`}
                  </p>
                  <p className="text-xs text-text-muted truncate">{app.company}</p>
                </div>
                <span className={`px-2.5 py-1 rounded-lg text-xs font-medium ${getBadge(app.status)}`}>
                  {app.status}
                </span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
