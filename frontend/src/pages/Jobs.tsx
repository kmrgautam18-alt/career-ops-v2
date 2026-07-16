import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Briefcase, Plus, Search, ExternalLink, Trash2, Loader2,
  MapPin, X, Filter,
} from 'lucide-react';
import { jobsApi } from '../api/client';

interface Job {
  id: number;
  title: string;
  company: string;
  location?: string;
  status: string;
  url?: string;
  description?: string;
  created_at?: string;
}

const statusBadge: Record<string, string> = {
  saved: 'badge-saved',
  new: 'badge-new',
  applied: 'badge-applied',
  interviewing: 'badge-interview',
  offer: 'badge-offer',
  rejected: 'badge-rejected',
  accepted: 'badge-accepted',
};

export function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showCreate, setShowCreate] = useState(false);
  const [newJob, setNewJob] = useState({
    title: '', company: '', location: '', description: '', url: '', status: 'saved',
  });

  const fetchJobs = () => {
    setLoading(true);
    jobsApi.list({ search })
      .then((res) => setJobs(res.data.data || []))
      .catch(() => setJobs([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchJobs(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await jobsApi.create(newJob);
      setShowCreate(false);
      setNewJob({ title: '', company: '', location: '', description: '', url: '', status: 'saved' });
      fetchJobs();
    } catch (err) {
      console.error('Failed to create job', err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await jobsApi.delete(id);
      fetchJobs();
    } catch (err) {
      console.error('Failed to delete job', err);
    }
  };

  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Jobs</h1>
          <p className="text-text-muted mt-1">Track and manage your opportunities</p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="group relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
        >
          <Plus className="w-4 h-4" />
          <span>Add Job</span>
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
        </button>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className="relative group"
      >
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted group-focus-within:text-primary transition-colors" />
        <input
          type="text"
          placeholder="Search jobs by title or company..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && fetchJobs()}
          className="w-full pl-11 pr-14 py-3 rounded-2xl bg-surface border border-border/60 text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all duration-200"
        />
        <button
          onClick={fetchJobs}
          className="absolute right-3 top-1/2 -translate-y-1/2 px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-medium hover:bg-primary-hover transition-colors"
        >
          <Filter className="w-3.5 h-3.5" />
        </button>
      </motion.div>

      <AnimatePresence>
        {showCreate && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowCreate(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="w-full max-w-lg glass-panel-strong rounded-2xl p-6 sm:p-8"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-text-heading">Add New Job</h2>
                <button onClick={() => setShowCreate(false)}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <form onSubmit={handleCreate} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-heading mb-1.5">Title *</label>
                    <input type="text" value={newJob.title} onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-heading mb-1.5">Company *</label>
                    <input type="text" value={newJob.company} onChange={(e) => setNewJob({ ...newJob, company: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all" required />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Location</label>
                  <input type="text" value={newJob.location} onChange={(e) => setNewJob({ ...newJob, location: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">URL</label>
                  <input type="url" value={newJob.url} onChange={(e) => setNewJob({ ...newJob, url: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Description</label>
                  <textarea value={newJob.description} onChange={(e) => setNewJob({ ...newJob, description: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[80px] resize-y" />
                </div>
                <div className="flex justify-end gap-3 pt-2">
                  <button type="button" onClick={() => setShowCreate(false)}
                    className="px-5 py-2.5 rounded-xl text-sm text-text-muted hover:text-text-heading transition-colors">Cancel</button>
                  <button type="submit"
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">Create Job</button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {loading ? (
        <div className="flex justify-center py-16">
          <div className="flex flex-col items-center gap-3">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
            <p className="text-text-muted text-sm">Loading jobs...</p>
          </div>
        </div>
      ) : jobs.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-20 glass-panel rounded-2xl"
        >
          <div className="w-16 h-16 rounded-2xl bg-primary-light flex items-center justify-center mb-4">
            <Briefcase className="w-8 h-8 text-primary" />
          </div>
          <p className="text-text-heading font-medium mb-1">No jobs yet</p>
          <p className="text-text-muted text-sm mb-6">Start by adding your first job opportunity!</p>
          <button onClick={() => setShowCreate(true)}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">
            <Plus className="w-4 h-4" />
            Add Your First Job
          </button>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid gap-3.5"
        >
          {jobs.map((job, i) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
              className="group relative p-5 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden"
            >
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
              </div>
              <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-3xl pointer-events-none" />

              <div className="relative flex items-start justify-between gap-4">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <h3 className="text-base font-semibold text-text-heading truncate">{job.title}</h3>
                    <span className={`px-2.5 py-1 rounded-lg text-[11px] font-medium ${statusBadge[job.status] || 'badge-saved'}`}>
                      {job.status}
                    </span>
                  </div>
                  <p className="text-sm text-text-muted flex items-center gap-2">
                    <span className="font-medium text-text">{job.company}</span>
                    {job.location && (
                      <>
                        <span className="text-border-light">·</span>
                        <MapPin className="w-3 h-3 inline" />
                        {job.location}
                      </>
                    )}
                  </p>
                  {job.description && (
                    <p className="text-xs text-text-muted/60 mt-2 line-clamp-1">{job.description}</p>
                  )}
                </div>
                <div className="flex items-center gap-1.5 flex-shrink-0">
                  {job.url && (
                    <a href={job.url} target="_blank" rel="noopener noreferrer"
                      className="p-2.5 rounded-xl text-text-muted hover:text-text-heading hover:bg-surface-lighter transition-all">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  )}
                  <button onClick={() => handleDelete(job.id)}
                    className="p-2.5 rounded-xl text-text-muted hover:text-danger hover:bg-danger-light transition-all">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
