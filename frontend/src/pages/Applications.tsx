import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send, Plus, Loader2, Trash2, X,
  Calendar, FileText,
} from 'lucide-react';
import { applicationsApi } from '../api/client';

interface Application {
  id: number;
  job_id?: number;
  job_title?: string;
  company?: string;
  status: string;
  notes?: string;
  applied_date?: string;
  created_at?: string;
}

const statusFlow = ['saved', 'applied', 'interview', 'offer', 'rejected', 'accepted'];

const statusBadge: Record<string, string> = {
  saved: 'badge-saved',
  new: 'badge-new',
  applied: 'badge-applied',
  interview: 'badge-interview',
  offer: 'badge-offer',
  rejected: 'badge-rejected',
  accepted: 'badge-accepted',
};

export function Applications() {
  const [apps, setApps] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newApp, setNewApp] = useState({ job_id: '', status: 'applied', notes: '' });
  const [deleting, setDeleting] = useState<number | null>(null);

  const fetchApps = () => {
    setLoading(true);
    applicationsApi.list()
      .then((res) => setApps(Array.isArray(res.data.data) ? res.data.data : []))
      .catch(() => setApps([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchApps(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await applicationsApi.create({
        job_id: parseInt(newApp.job_id),
        status: newApp.status,
        notes: newApp.notes,
        applied_date: new Date().toISOString().split('T')[0],
      });
      setShowCreate(false);
      setNewApp({ job_id: '', status: 'applied', notes: '' });
      fetchApps();
    } catch (err) {
      console.error('Failed to create application', err);
    }
  };

  const handleDelete = async (id: number) => {
    setDeleting(id);
    try {
      await applicationsApi.delete(id);
      fetchApps();
    } catch (err) {
      console.error('Failed to delete', err);
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Applications</h1>
          <p className="text-text-muted mt-1">Track every stage of your job applications</p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="group relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
        >
          <Plus className="w-4 h-4" />
          <span>Add Application</span>
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
        </button>
      </motion.div>

      {/* Create Modal */}
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
                <h2 className="text-xl font-semibold text-text-heading">Add Application</h2>
                <button onClick={() => setShowCreate(false)}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <form onSubmit={handleCreate} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Job ID *</label>
                  <input type="number" value={newApp.job_id} onChange={(e) => setNewApp({ ...newApp, job_id: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                    required />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Status</label>
                  <select value={newApp.status} onChange={(e) => setNewApp({ ...newApp, status: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all">
                    {statusFlow.map(s => (
                      <option key={s} value={s} className="capitalize">{s}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Notes</label>
                  <textarea value={newApp.notes} onChange={(e) => setNewApp({ ...newApp, notes: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[80px] resize-y" />
                </div>
                <div className="flex justify-end gap-3 pt-2">
                  <button type="button" onClick={() => setShowCreate(false)}
                    className="px-5 py-2.5 rounded-xl text-sm text-text-muted hover:text-text-heading transition-colors">Cancel</button>
                  <button type="submit"
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">Create</button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* App List */}
      {loading ? (
        <div className="flex justify-center py-16">
          <div className="flex flex-col items-center gap-3">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
            <p className="text-text-muted text-sm">Loading applications...</p>
          </div>
        </div>
      ) : apps.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-20 glass-panel rounded-2xl"
        >
          <div className="w-16 h-16 rounded-2xl bg-primary-light flex items-center justify-center mb-4">
            <Send className="w-8 h-8 text-primary" />
          </div>
          <p className="text-text-heading font-medium mb-1">No applications yet</p>
          <p className="text-text-muted text-sm mb-6">Start tracking your job applications!</p>
          <button onClick={() => setShowCreate(true)}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">
            <Plus className="w-4 h-4" />
            Add Application
          </button>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid gap-3.5"
        >
          {apps.map((app, i) => (
            <motion.div
              key={app.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
              className="group relative p-5 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden"
            >
              {/* Hover shine */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
              </div>

              <div className="relative flex items-start justify-between gap-4">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <h3 className="text-base font-semibold text-text-heading">
                      {app.job_title || `Application #${app.id}`}
                    </h3>
                    <span className={`px-2.5 py-1 rounded-lg text-[11px] font-medium ${statusBadge[app.status] || 'badge-saved'}`}>
                      {app.status}
                    </span>
                  </div>
                  {app.company && (
                    <p className="text-sm text-text-muted">{app.company}</p>
                  )}
                  <div className="flex items-center gap-3 mt-2 text-xs text-text-muted/60">
                    {app.applied_date && (
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {app.applied_date}
                      </span>
                    )}
                    <span className="flex items-center gap-1">
                      <FileText className="w-3 h-3" />
                      ID: {app.id}
                    </span>
                  </div>
                  {app.notes && (
                    <p className="text-xs text-text-muted/50 mt-2 line-clamp-1 italic">{app.notes}</p>
                  )}
                </div>
                <button
                  onClick={() => handleDelete(app.id)}
                  disabled={deleting === app.id}
                  className="p-2.5 rounded-xl text-text-muted hover:text-danger hover:bg-danger-light transition-all disabled:opacity-50"
                >
                  {deleting === app.id ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Trash2 className="w-4 h-4" />
                  )}
                </button>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
