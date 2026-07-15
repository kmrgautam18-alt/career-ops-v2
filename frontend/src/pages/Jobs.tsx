import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Briefcase, Plus, Search, ExternalLink, Trash2, Loader2 } from 'lucide-react';
import { jobsApi } from '../api/client';

interface Job {
  id: number;
  title: string;
  company: string;
  location?: string;
  status: string;
  url?: string;
  created_at?: string;
}

const statusColors: Record<string, string> = {
  saved: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
  applied: 'bg-purple-500/20 text-purple-400 border-purple-500/20',
  interviewing: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
  offer: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
  rejected: 'bg-red-500/20 text-red-400 border-red-500/20',
  accepted: 'bg-green-500/20 text-green-400 border-green-500/20',
};

export function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showCreate, setShowCreate] = useState(false);
  const [newJob, setNewJob] = useState({ title: '', company: '', location: '', description: '', url: '', status: 'saved' });

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
    if (!confirm('Delete this job?')) return;
    try {
      await jobsApi.delete(id);
      fetchJobs();
    } catch (err) {
      console.error('Failed to delete job', err);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-heading">Jobs</h1>
          <p className="text-text mt-1">Track and manage your job opportunities</p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-hover transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Job
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text" />
        <input
          type="text"
          placeholder="Search jobs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && fetchJobs()}
          className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-surface border border-border text-text-heading placeholder:text-text focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors"
        />
      </div>

      {/* Create Modal */}
      {showCreate && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setShowCreate(false)}>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-lg bg-surface border border-border rounded-xl p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-lg font-semibold text-text-heading mb-4">Add New Job</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Title *</label>
                <input type="text" value={newJob.title} onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                  required />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Company *</label>
                <input type="text" value={newJob.company} onChange={(e) => setNewJob({ ...newJob, company: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                  required />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Location</label>
                <input type="text" value={newJob.location} onChange={(e) => setNewJob({ ...newJob, location: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">URL</label>
                <input type="url" value={newJob.url} onChange={(e) => setNewJob({ ...newJob, url: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Description</label>
                <textarea value={newJob.description} onChange={(e) => setNewJob({ ...newJob, description: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary min-h-[80px]" />
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button type="button" onClick={() => setShowCreate(false)}
                  className="px-4 py-2 rounded-lg text-sm text-text hover:text-text-heading transition-colors">Cancel</button>
                <button type="submit"
                  className="px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-hover transition-colors">Create Job</button>
              </div>
            </form>
          </motion.div>
        </div>
      )}

      {/* Jobs List */}
      {loading ? (
        <div className="flex justify-center py-12"><Loader2 className="w-8 h-8 text-primary animate-spin" /></div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-12">
          <Briefcase className="w-12 h-12 text-text/40 mx-auto mb-3" />
          <p className="text-text">No jobs yet. Start by adding your first job opportunity!</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {jobs.map((job, i) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="p-4 rounded-xl bg-surface border border-border hover:border-primary/20 transition-all duration-200 group"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-base font-semibold text-text-heading truncate">{job.title}</h3>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium border ${statusColors[job.status] || 'bg-gray-500/20 text-gray-400 border-gray-500/20'}`}>
                      {job.status}
                    </span>
                  </div>
                  <p className="text-sm text-text">{job.company}{job.location ? ` · ${job.location}` : ''}</p>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  {job.url && (
                    <a href={job.url} target="_blank" rel="noopener noreferrer"
                      className="p-2 rounded-lg text-text hover:text-text-heading hover:bg-surface-light transition-colors">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  )}
                  <button onClick={() => handleDelete(job.id)}
                    className="p-2 rounded-lg text-text hover:text-danger hover:bg-danger/10 transition-colors">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
