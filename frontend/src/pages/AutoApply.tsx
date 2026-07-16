import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Zap, Plus, Loader2, Trash2, X, Search,
  Globe, Building2, Sparkles, Send,
  Calendar, Clock, ChevronRight, RefreshCw,
  Mail,
} from 'lucide-react';
import { autoApplyApi } from '../api/client';

interface AutoApp {
  id: number;
  user_id: number;
  source: string;
  source_url?: string;
  company: string;
  job_title: string;
  job_description?: string;
  company_email?: string;
  status: string;
  ats_score?: number;
  tailored_resume_text?: string;
  email_sent_to?: string;
  email_sent_at?: string;
  interview_date?: string;
  interview_type?: string;
  followup_count: number;
  next_followup_at?: string;
  notes?: string;
  created_at: string;
}

interface DashboardStats {
  total_sourced: number;
  total_ai_optimized: number;
  total_emailed: number;
  total_interviews: number;
  total_rejected: number;
  total_accepted: number;
  pending_followups: number;
  upcoming_interviews: Array<{
    id: number;
    company: string;
    job_title: string;
    interview_date: string;
    interview_type: string;
  }>;
}

const statusConfig: Record<string, { label: string; color: string; icon: string }> = {
  sourced: { label: 'Sourced', color: 'text-blue-400 bg-blue-400/10 border-blue-400/20', icon: '🔍' },
  ai_optimized: { label: 'AI Optimized', color: 'text-purple-400 bg-purple-400/10 border-purple-400/20', icon: '🤖' },
  emailed: { label: 'Emailed', color: 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20', icon: '📧' },
  interview_scheduled: { label: 'Interview', color: 'text-green-400 bg-green-400/10 border-green-400/20', icon: '🎯' },
  followup_sent: { label: 'Follow-up', color: 'text-amber-400 bg-amber-400/10 border-amber-400/20', icon: '🔄' },
  rejected: { label: 'Rejected', color: 'text-red-400 bg-red-400/10 border-red-400/20', icon: '❌' },
  accepted: { label: 'Accepted', color: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20', icon: '✅' },
};

const sourceIcons: Record<string, typeof Globe> = {
  linkedin: Globe,
  indeed: Globe,
  company_career: Building2,
  manual: Plus,
};

export function AutoApply() {
  const [apps, setApps] = useState<AutoApp[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [showScrapeModal, setShowScrapeModal] = useState(false);
  const [showManualModal, setShowManualModal] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [scrapedJobs, setScrapedJobs] = useState<any[]>([]);
  const [pipelineRunning, setPipelineRunning] = useState(false);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'applications'>('dashboard');

  const [scrapeForm, setScrapeForm] = useState({
    source: 'linkedin',
    query: '',
    location: '',
  });

  const [manualForm, setManualForm] = useState({
    company: '',
    job_title: '',
    job_description: '',
    company_email: '',
    source: 'manual',
  });

  const [expandedApp, setExpandedApp] = useState<number | null>(null);
  const [actionLoading, setActionLoading] = useState<Record<string, boolean>>({});

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [appsRes, statsRes] = await Promise.all([
        autoApplyApi.list(),
        autoApplyApi.dashboard(),
      ]);
      setApps(Array.isArray(appsRes.data.data) ? appsRes.data.data : []);
      setStats(statsRes.data.data || {});
    } catch (err) {
      console.error('Failed to fetch auto-apply data', err);
      setApps([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleScrape = async () => {
    if (!scrapeForm.query) return;
    setScraping(true);
    try {
      const res = await autoApplyApi.scrape({
        source: scrapeForm.source,
        query: scrapeForm.query,
        location: scrapeForm.location || undefined,
      });
      setScrapedJobs(res.data.jobs || []);
    } catch (err) {
      console.error('Scrape failed', err);
    } finally {
      setScraping(false);
    }
  };

  const handleImportJobs = async () => {
    if (scrapedJobs.length === 0) return;
    setPipelineRunning(true);
    try {
      for (const job of scrapedJobs) {
        await autoApplyApi.create({
          source: scrapeForm.source,
          source_url: job.url,
          company: job.company,
          job_title: job.title,
          job_description: job.description,
        });
      }
      setScrapedJobs([]);
      setShowScrapeModal(false);
      await fetchData();
    } catch (err) {
      console.error('Import failed', err);
    } finally {
      setPipelineRunning(false);
    }
  };

  const handleManualCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await autoApplyApi.create(manualForm);
      setShowManualModal(false);
      setManualForm({ company: '', job_title: '', job_description: '', company_email: '', source: 'manual' });
      await fetchData();
    } catch (err) {
      console.error('Create failed', err);
    }
  };

  const handleAutoOptimize = async (id: number) => {
    setActionLoading(prev => ({ ...prev, [`optimize-${id}`]: true }));
    try {
      await autoApplyApi.optimize(id);
      await fetchData();
    } catch (err) {
      console.error('Optimize failed', err);
    } finally {
      setActionLoading(prev => ({ ...prev, [`optimize-${id}`]: false }));
    }
  };

  const handleSendEmail = async (id: number, email?: string) => {
    setActionLoading(prev => ({ ...prev, [`send-${id}`]: true }));
    try {
      await autoApplyApi.sendEmail(id, email);
      await fetchData();
    } catch (err) {
      console.error('Send failed', err);
    } finally {
      setActionLoading(prev => ({ ...prev, [`send-${id}`]: false }));
    }
  };

  const handleFollowup = async (id: number) => {
    setActionLoading(prev => ({ ...prev, [`followup-${id}`]: true }));
    try {
      await autoApplyApi.followup(id);
      await fetchData();
    } catch (err) {
      console.error('Follow-up failed', err);
    } finally {
      setActionLoading(prev => ({ ...prev, [`followup-${id}`]: false }));
    }
  };

  const handleFullPipeline = async () => {
    if (!scrapeForm.query) return;
    setPipelineRunning(true);
    try {
      await autoApplyApi.fullPipeline(
        scrapeForm.source,
        scrapeForm.query,
        scrapeForm.location || undefined,
        3,
      );
      setShowScrapeModal(false);
      await fetchData();
    } catch (err) {
      console.error('Pipeline failed', err);
    } finally {
      setPipelineRunning(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await autoApplyApi.delete(id);
      await fetchData();
    } catch (err) {
      console.error('Delete failed', err);
    }
  };

  const getStatusBadge = (status: string) => {
    const config = statusConfig[status] || { label: status, color: 'text-text-muted bg-surface-light border-border', icon: '📋' };
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium border ${config.color}`}>
        <span>{config.icon}</span>
        {config.label}
      </span>
    );
  };

  const formatDate = (d: string | undefined) => {
    if (!d) return '';
    return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between flex-wrap gap-4"
      >
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Auto-Apply Engine</h1>
          <p className="text-text-muted mt-1">AI-powered job sourcing, resume tailoring & automated applications</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => { setShowScrapeModal(true); setActiveTab('applications'); }}
            className="group relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
          >
            <Search className="w-4 h-4" />
            <span>Scrape Jobs</span>
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
          </button>
          <button
            onClick={() => setShowManualModal(true)}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-surface border border-border/60 text-text-heading text-sm font-medium hover:border-primary/30 hover:bg-surface-light transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>Manual Entry</span>
          </button>
        </div>
      </motion.div>

      {/* Tabs */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-surface border border-border/60 w-fit">
        {(['dashboard', 'applications'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === tab
                ? 'bg-primary/10 text-primary shadow-sm'
                : 'text-text-muted hover:text-text-heading'
            }`}
          >
            {tab === 'dashboard' ? '📊 Dashboard' : '📋 Applications'}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center py-16">
          <Loader2 className="w-8 h-8 text-primary animate-spin" />
        </div>
      ) : activeTab === 'dashboard' ? (
        /* ═══════════════════════════════════════ DASHBOARD VIEW ═══════════════════════════════════════ */
        <div className="space-y-7">
          {/* Stat Cards */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4"
          >
            {[
              { label: 'Sourced', value: stats?.total_sourced || 0, icon: Search, color: 'from-blue-500/20 to-blue-600/10', textColor: 'text-blue-400' },
              { label: 'AI Optimized', value: stats?.total_ai_optimized || 0, icon: Sparkles, color: 'from-purple-500/20 to-purple-600/10', textColor: 'text-purple-400' },
              { label: 'Emailed', value: stats?.total_emailed || 0, icon: Send, color: 'from-cyan-500/20 to-cyan-600/10', textColor: 'text-cyan-400' },
              { label: 'Interviews', value: stats?.total_interviews || 0, icon: Calendar, color: 'from-green-500/20 to-green-600/10', textColor: 'text-green-400' },
              { label: 'Follow-ups Due', value: stats?.pending_followups || 0, icon: RefreshCw, color: 'from-amber-500/20 to-amber-600/10', textColor: 'text-amber-400' },
            ].map((card, i) => (
              <motion.div
                key={card.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="relative p-5 rounded-2xl bg-surface border border-border/60 overflow-hidden group hover:border-border-glow/40 transition-all duration-500"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${card.color} opacity-50`} />
                <div className="relative z-10">
                  <div className="flex items-center justify-between mb-3">
                    <card.icon className={`w-5 h-5 ${card.textColor}`} />
                    <span className={`text-2xl font-bold ${card.textColor}`}>{card.value}</span>
                  </div>
                  <p className="text-xs text-text-muted font-medium">{card.label}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>

          {/* Pipeline Status */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-6 rounded-2xl bg-surface border border-border/60"
          >
            <h2 className="text-lg font-semibold text-text-heading mb-4">Pipeline Progress</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { key: 'total_sourced', label: 'Step 1: Sourced', desc: 'Jobs found from portals', icon: Search, color: 'bg-blue-500' },
                { key: 'total_ai_optimized', label: 'Step 2: AI Optimized', desc: 'Resumes tailored', icon: Sparkles, color: 'bg-purple-500' },
                { key: 'total_emailed', label: 'Step 3: Emailed', desc: 'Applications sent', icon: Send, color: 'bg-cyan-500' },
                { key: 'total_interviews', label: 'Step 4: Interviews', desc: 'Responses received', icon: Calendar, color: 'bg-green-500' },
              ].map((step) => {
                const val = (stats as any)?.[step.key] || 0;
                const total = (stats?.total_sourced || 1);
                const pct = Math.round((val / total) * 100);
                return (
                  <div key={step.key} className="text-center">
                    <div className="relative w-20 h-20 mx-auto mb-3">
                      <svg className="w-20 h-20 -rotate-90" viewBox="0 0 36 36">
                        <circle cx="18" cy="18" r="15.5" fill="none" stroke="currentColor" strokeWidth="3" className="text-border" />
                        <circle cx="18" cy="18" r="15.5" fill="none" stroke="currentColor" strokeWidth="3"
                          strokeDasharray={`${pct * 0.97} 100`}
                          className={`${step.color.replace('bg-', 'text-')}`}
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <step.icon className="w-6 h-6 text-text-muted" />
                      </div>
                    </div>
                    <p className="text-sm font-medium text-text-heading">{step.label}</p>
                    <p className="text-xs text-text-muted mt-1">{val} {step.desc}</p>
                  </div>
                );
              })}
            </div>
          </motion.div>

          {/* Upcoming Interviews */}
          {stats?.upcoming_interviews && stats.upcoming_interviews.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="p-6 rounded-2xl bg-surface border border-border/60"
            >
              <h2 className="text-lg font-semibold text-text-heading mb-4">📅 Upcoming Interviews</h2>
              <div className="space-y-3">
                {stats.upcoming_interviews.map((iv) => (
                  <div key={iv.id} className="flex items-center justify-between p-4 rounded-xl bg-surface-light/50 border border-border/40">
                    <div>
                      <p className="font-medium text-text-heading">{iv.company} — {iv.job_title}</p>
                      <p className="text-sm text-text-muted mt-1">
                        <Calendar className="w-3.5 h-3.5 inline mr-1" />
                        {formatDate(iv.interview_date)} · {iv.interview_type}
                      </p>
                    </div>
                    <span className="px-3 py-1.5 rounded-lg bg-green-400/10 border border-green-400/20 text-green-400 text-xs font-medium">
                      🎯 Scheduled
                    </span>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </div>
      ) : (
        /* ═══════════════════════════════════════ APPLICATIONS LIST ═══════════════════════════════════════ */
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-3.5"
        >
          {apps.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col items-center justify-center py-20 glass-panel rounded-2xl"
            >
              <div className="w-16 h-16 rounded-2xl bg-primary-light flex items-center justify-center mb-4">
                <Zap className="w-8 h-8 text-primary" />
              </div>
              <p className="text-text-heading font-medium mb-1">No auto-applications yet</p>
              <p className="text-text-muted text-sm mb-6">Scrape jobs or enter them manually to get started!</p>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowScrapeModal(true)}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury"
                >
                  <Search className="w-4 h-4" />
                  Scrape Jobs
                </button>
                <button
                  onClick={() => setShowManualModal(true)}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-surface border border-border/60 text-text-heading text-sm font-medium"
                >
                  <Plus className="w-4 h-4" />
                  Manual Entry
                </button>
              </div>
            </motion.div>
          ) : (
            <AnimatePresence>
              {apps.map((app, i) => (
                <motion.div
                  key={app.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ delay: i * 0.03 }}
                >
                  <div
                    className="group relative p-5 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 cursor-pointer overflow-hidden"
                    onClick={() => setExpandedApp(expandedApp === app.id ? null : app.id)}
                  >
                    {/* Hover shine */}
                    <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none">
                      <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
                    </div>

                    <div className="relative">
                      {/* Header row */}
                      <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-2.5 mb-1.5 flex-wrap">
                            {/* Source icon */}
                            <div className="w-8 h-8 rounded-xl bg-primary-light/30 flex items-center justify-center">
                              {sourceIcons[app.source] ? (
                                (() => {
                                  const IconComp = sourceIcons[app.source];
                                  return <IconComp className="w-4 h-4 text-primary" />;
                                })()
                              ) : (
                                <Globe className="w-4 h-4 text-primary" />
                              )}
                            </div>
                            <h3 className="text-base font-semibold text-text-heading">{app.job_title}</h3>
                            {getStatusBadge(app.status)}
                          </div>
                          <p className="text-sm font-medium text-text-muted ml-[42px]">{app.company}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          {app.ats_score && (
                            <div className={`px-2.5 py-1 rounded-lg text-xs font-bold ${
                              app.ats_score >= 80 ? 'text-green-400 bg-green-400/10' :
                              app.ats_score >= 60 ? 'text-amber-400 bg-amber-400/10' :
                              'text-red-400 bg-red-400/10'
                            }`}>
                              {app.ats_score}%
                            </div>
                          )}
                          <button
                            onClick={(e) => { e.stopPropagation(); handleDelete(app.id); }}
                            className="p-2 rounded-lg text-text-muted hover:text-danger hover:bg-danger-light transition-all opacity-0 group-hover:opacity-100"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>

                      {/* Meta row */}
                      <div className="flex items-center gap-4 mt-2.5 ml-[42px] text-xs text-text-muted/60">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {formatDate(app.created_at)}
                        </span>
                        {app.email_sent_at && (
                          <span className="flex items-center gap-1">
                            <Mail className="w-3 h-3" />
                            Emailed {formatDate(app.email_sent_at)}
                          </span>
                        )}
                        {app.followup_count > 0 && (
                          <span className="flex items-center gap-1">
                            <RefreshCw className="w-3 h-3" />
                            {app.followup_count} follow-up(s)
                          </span>
                        )}
                        <ChevronRight className={`w-4 h-4 ml-auto transition-transform ${expandedApp === app.id ? 'rotate-90' : ''}`} />
                      </div>

                      {/* Expanded Details */}
                      <AnimatePresence>
                        {expandedApp === app.id && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.2 }}
                            className="overflow-hidden"
                          >
                            <div className="pt-4 mt-4 border-t border-border/40 space-y-4">
                              {/* Action Buttons */}
                              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                                {/* Optimize */}
                                <button
                                  onClick={(e) => { e.stopPropagation(); handleAutoOptimize(app.id); }}
                                  disabled={actionLoading[`optimize-${app.id}`] || app.status === 'ai_optimized'}
                                  className="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-medium hover:bg-purple-500/20 transition-all disabled:opacity-40"
                                >
                                  {actionLoading[`optimize-${app.id}`] ? (
                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                  ) : (
                                    <Sparkles className="w-3.5 h-3.5" />
                                  )}
                                  AI Optimize
                                </button>

                                {/* Send Email */}
                                <button
                                  onClick={(e) => { e.stopPropagation(); handleSendEmail(app.id, app.company_email); }}
                                  disabled={actionLoading[`send-${app.id}`] || app.status === 'emailed'}
                                  className="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-medium hover:bg-cyan-500/20 transition-all disabled:opacity-40"
                                >
                                  {actionLoading[`send-${app.id}`] ? (
                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                  ) : (
                                    <Send className="w-3.5 h-3.5" />
                                  )}
                                  Send Email
                                </button>

                                {/* Follow-up */}
                                <button
                                  onClick={(e) => { e.stopPropagation(); handleFollowup(app.id); }}
                                  disabled={actionLoading[`followup-${app.id}`]}
                                  className="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-medium hover:bg-amber-500/20 transition-all disabled:opacity-40"
                                >
                                  {actionLoading[`followup-${app.id}`] ? (
                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                  ) : (
                                    <RefreshCw className="w-3.5 h-3.5" />
                                  )}
                                  Follow-up
                                </button>

                                {/* Record Interview */}
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    const date = prompt('Interview date (YYYY-MM-DD):');
                                    if (date) {
                                      const type = prompt('Type (phone/video/onsite):') || 'video';
                                      autoApplyApi.interview(app.id, date, type).then(() => fetchData());
                                    }
                                  }}
                                  className="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-xs font-medium hover:bg-green-500/20 transition-all"
                                >
                                  <Calendar className="w-3.5 h-3.5" />
                                  Interview
                                </button>
                              </div>

                              {/* Details Grid */}
                              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                                <div className="space-y-2">
                                  {app.company_email && (
                                    <div className="flex items-center gap-2 text-text-muted">
                                      <Mail className="w-3.5 h-3.5" />
                                      <span>{app.company_email}</span>
                                    </div>
                                  )}
                                  {app.source_url && (
                                    <div className="flex items-center gap-2 text-text-muted">
                                      <Globe className="w-3.5 h-3.5" />
                                      <a href={app.source_url} target="_blank" rel="noopener noreferrer"
                                        className="text-primary hover:underline truncate max-w-[300px]"
                                        onClick={e => e.stopPropagation()}
                                      >
                                        {app.source_url}
                                      </a>
                                    </div>
                                  )}
                                  {app.next_followup_at && (
                                    <div className="flex items-center gap-2 text-text-muted">
                                      <Clock className="w-3.5 h-3.5" />
                                      <span>Next follow-up: {formatDate(app.next_followup_at)}</span>
                                    </div>
                                  )}
                                </div>
                                <div className="space-y-2">
                                  {app.interview_date && (
                                    <div className="flex items-center gap-2 text-green-400">
                                      <Calendar className="w-3.5 h-3.5" />
                                      <span>Interview: {formatDate(app.interview_date)} ({app.interview_type})</span>
                                    </div>
                                  )}
                                  {app.email_sent_to && (
                                    <div className="flex items-center gap-2 text-text-muted">
                                      <Send className="w-3.5 h-3.5" />
                                      <span>Sent to: {app.email_sent_to}</span>
                                    </div>
                                  )}
                                </div>
                              </div>

                              {/* AI Tailored Resume Preview */}
                              {app.tailored_resume_text && (
                                <div>
                                  <p className="text-xs font-medium text-text-muted mb-2">📄 AI-Tailored Resume Preview</p>
                                  <div className="p-3 rounded-xl bg-background border border-border/40 max-h-32 overflow-y-auto text-xs text-text-muted font-mono leading-relaxed">
                                    <pre className="whitespace-pre-wrap">{app.tailored_resume_text.substring(0, 1000)}...</pre>
                                  </div>
                                </div>
                              )}

                              {/* Notes */}
                              {app.notes && (
                                <p className="text-xs text-text-muted italic">{app.notes}</p>
                              )}
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          )}
        </motion.div>
      )}

      {/* ═══════════════════════════════════════ SCRAPE MODAL ═══════════════════════════════════════ */}
      <AnimatePresence>
        {showScrapeModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowScrapeModal(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="w-full max-w-2xl glass-panel-strong rounded-2xl p-6 sm:p-8 max-h-[85vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-semibold text-text-heading">🔍 Scrape Jobs</h2>
                  <p className="text-sm text-text-muted mt-1">Find job listings from various sources</p>
                </div>
                <button onClick={() => { setShowScrapeModal(false); setScrapedJobs([]); }}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-4">
                {/* Source */}
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Source</label>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { value: 'linkedin', label: 'LinkedIn', icon: Globe },
                      { value: 'indeed', label: 'Indeed', icon: Globe },
                      { value: 'company_career', label: 'Career Pages', icon: Building2 },
                    ].map(src => (
                      <button
                        key={src.value}
                        onClick={() => setScrapeForm({ ...scrapeForm, source: src.value })}
                        className={`flex items-center justify-center gap-2 px-4 py-3 rounded-xl border text-sm font-medium transition-all ${
                          scrapeForm.source === src.value
                            ? 'border-primary/50 bg-primary/10 text-primary'
                            : 'border-border/60 text-text-muted hover:border-border-glow/40 hover:text-text-heading'
                        }`}
                      >
                        <src.icon className="w-4 h-4" />
                        {src.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Query */}
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Job Search Query</label>
                  <input
                    type="text"
                    value={scrapeForm.query}
                    onChange={(e) => setScrapeForm({ ...scrapeForm, query: e.target.value })}
                    placeholder="e.g. Senior Software Engineer, Python Developer..."
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                  />
                </div>

                {/* Location */}
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Location (optional)</label>
                  <input
                    type="text"
                    value={scrapeForm.location}
                    onChange={(e) => setScrapeForm({ ...scrapeForm, location: e.target.value })}
                    placeholder="e.g. Remote, San Francisco, New York..."
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                  />
                </div>

                {/* Buttons */}
                <div className="flex items-center gap-3 pt-2">
                  <button
                    onClick={handleScrape}
                    disabled={scraping || !scrapeForm.query}
                    className="flex-1 flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury disabled:opacity-50"
                  >
                    {scraping ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Search className="w-4 h-4" />
                    )}
                    Find Jobs
                  </button>
                  <button
                    onClick={handleFullPipeline}
                    disabled={pipelineRunning || !scrapeForm.query}
                    className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-green-500/20 border border-green-500/30 text-green-400 text-sm font-medium hover:bg-green-500/30 transition-all disabled:opacity-50"
                  >
                    {pipelineRunning ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Zap className="w-4 h-4" />
                    )}
                    Full Pipeline
                  </button>
                </div>

                {/* Scraped Results */}
                {scrapedJobs.length > 0 && (
                  <div className="pt-4 border-t border-border/40">
                    <div className="flex items-center justify-between mb-3">
                      <p className="text-sm font-medium text-text-heading">Found {scrapedJobs.length} jobs</p>
                      <button
                        onClick={handleImportJobs}
                        disabled={pipelineRunning}
                        className="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary/10 border border-primary/20 text-primary text-xs font-medium hover:bg-primary/20 transition-all"
                      >
                        {pipelineRunning ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        ) : (
                          <Plus className="w-3.5 h-3.5" />
                        )}
                        Import All
                      </button>
                    </div>
                    <div className="space-y-2 max-h-60 overflow-y-auto">
                      {scrapedJobs.map((job, idx) => (
                        <div key={idx} className="p-3 rounded-xl bg-background border border-border/40">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm font-medium text-text-heading">{job.title}</p>
                              <p className="text-xs text-text-muted mt-0.5">{job.company} · {job.location || 'Remote'}</p>
                            </div>
                            <span className="text-[10px] text-text-muted uppercase px-2 py-0.5 rounded bg-surface-light">
                              {scrapeForm.source}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ═══════════════════════════════════════ MANUAL ENTRY MODAL ═══════════════════════════════════════ */}
      <AnimatePresence>
        {showManualModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowManualModal(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="w-full max-w-lg glass-panel-strong rounded-2xl p-6 sm:p-8"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-text-heading">Add Job Manually</h2>
                <button onClick={() => setShowManualModal(false)}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <form onSubmit={handleManualCreate} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-heading mb-1.5">Company *</label>
                    <input type="text" value={manualForm.company}
                      onChange={(e) => setManualForm({ ...manualForm, company: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                      required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-heading mb-1.5">Job Title *</label>
                    <input type="text" value={manualForm.job_title}
                      onChange={(e) => setManualForm({ ...manualForm, job_title: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                      required />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">HR Email</label>
                  <input type="email" value={manualForm.company_email}
                    onChange={(e) => setManualForm({ ...manualForm, company_email: e.target.value })}
                    placeholder="hr@company.com"
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Job Description</label>
                  <textarea value={manualForm.job_description}
                    onChange={(e) => setManualForm({ ...manualForm, job_description: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[100px] resize-y"
                    rows={4} />
                </div>
                <div className="flex justify-end gap-3 pt-2">
                  <button type="button" onClick={() => setShowManualModal(false)}
                    className="px-5 py-2.5 rounded-xl text-sm text-text-muted hover:text-text-heading transition-colors">Cancel</button>
                  <button type="submit"
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">Add Job</button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
