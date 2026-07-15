import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Briefcase,
  Send,
  BarChart3,
  TrendingUp,
  Loader2,
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
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  const statCards = [
    { label: 'Total Jobs', value: data.stats?.total_jobs ?? 0, icon: Briefcase, color: 'from-blue-500 to-cyan-500' },
    { label: 'Applications', value: data.stats?.total_applications ?? 0, icon: Send, color: 'from-purple-500 to-pink-500' },
    { label: 'Active', value: data.stats?.active_applications ?? 0, icon: TrendingUp, color: 'from-emerald-500 to-teal-500' },
    { label: 'Interviews', value: data.stats?.interviews ?? 0, icon: BarChart3, color: 'from-orange-500 to-red-500' },
  ];

  const statusColors: Record<string, string> = {
    saved: 'bg-blue-500/20 text-blue-400',
    applied: 'bg-purple-500/20 text-purple-400',
    interview: 'bg-amber-500/20 text-amber-400',
    offer: 'bg-emerald-500/20 text-emerald-400',
    rejected: 'bg-red-500/20 text-red-400',
    accepted: 'bg-green-500/20 text-green-400',
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-text-heading">Dashboard</h1>
        <p className="text-text mt-1">Overview of your career journey</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="relative p-4 rounded-xl bg-surface border border-border overflow-hidden group hover:border-primary/30 transition-all duration-300"
          >
            <div className={`absolute top-0 right-0 w-24 h-24 -mr-8 -mt-8 rounded-full bg-gradient-to-br ${stat.color} opacity-5 group-hover:opacity-10 transition-opacity`} />
            <div className="relative">
              <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${stat.color} p-2 mb-3`}>
                <stat.icon className="w-full h-full text-white" />
              </div>
              <div className="text-2xl font-bold text-text-heading">{stat.value}</div>
              <div className="text-sm text-text mt-1">{stat.label}</div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Recent Jobs */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="p-4 rounded-xl bg-surface border border-border"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-text-heading flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-primary" />
              Recent Jobs
            </h2>
            {(!data.recent_jobs || data.recent_jobs.length === 0) && (
              <span className="text-xs text-text">No jobs yet</span>
            )}
          </div>
          <div className="space-y-3">
            {data.recent_jobs?.slice(0, 5).map((job) => (
              <div key={job.id} className="flex items-center justify-between p-3 rounded-lg bg-surface-light/50 hover:bg-surface-light transition-colors">
                <div>
                  <p className="text-sm font-medium text-text-heading">{job.title}</p>
                  <p className="text-xs text-text">{job.company}</p>
                </div>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColors[job.status] || 'bg-gray-500/20 text-gray-400'}`}>
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
          className="p-4 rounded-xl bg-surface border border-border"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-text-heading flex items-center gap-2">
              <Send className="w-4 h-5 text-accent" />
              Recent Applications
            </h2>
            {(!data.recent_applications || data.recent_applications.length === 0) && (
              <span className="text-xs text-text">No applications yet</span>
            )}
          </div>
          <div className="space-y-3">
            {data.recent_applications?.slice(0, 5).map((app) => (
              <div key={app.id} className="flex items-center justify-between p-3 rounded-lg bg-surface-light/50 hover:bg-surface-light transition-colors">
                <div>
                  <p className="text-sm font-medium text-text-heading">{app.job_title}</p>
                  <p className="text-xs text-text">{app.company}</p>
                </div>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColors[app.status] || 'bg-gray-500/20 text-gray-400'}`}>
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
