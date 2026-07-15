import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Plus, Loader2, Trash2 } from 'lucide-react';
import { applicationsApi } from '../api/client';

interface Application {
  id: number;
  job_title?: string;
  company?: string;
  status: string;
  notes?: string;
  created_at?: string;
}

const statusColors: Record<string, string> = {
  saved: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
  applied: 'bg-purple-500/20 text-purple-400 border-purple-500/20',
  interview: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
  offer: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
  rejected: 'bg-red-500/20 text-red-400 border-red-500/20',
  accepted: 'bg-green-500/20 text-green-400 border-green-500/20',
};

export function Applications() {
  const [apps, setApps] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newApp, setNewApp] = useState({ job_id: '', status: 'applied', notes: '' });

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
      });
      setShowCreate(false);
      setNewApp({ job_id: '', status: 'applied', notes: '' });
      fetchApps();
    } catch (err) {
      console.error('Failed to create application', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this application?')) return;
    try {
      await applicationsApi.delete(id);
      fetchApps();
    } catch (err) {
      console.error('Failed to delete application', err);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-heading">Applications</h1>
          <p className="text-text mt-1">Track your job applications</p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-hover transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Application
        </button>
      </div>

      {showCreate && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setShowCreate(false)}>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-lg bg-surface border border-border rounded-xl p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-lg font-semibold text-text-heading mb-4">Add Application</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Job ID *</label>
                <input type="number" value={newApp.job_id} onChange={(e) => setNewApp({ ...newApp, job_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                  required />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Status</label>
                <select value={newApp.status} onChange={(e) => setNewApp({ ...newApp, status: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary">
                  <option value="saved">Saved</option>
                  <option value="applied">Applied</option>
                  <option value="interview">Interview</option>
                  <option value="offer">Offer</option>
                  <option value="rejected">Rejected</option>
                  <option value="accepted">Accepted</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Notes</label>
                <textarea value={newApp.notes} onChange={(e) => setNewApp({ ...newApp, notes: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary min-h-[80px]" />
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button type="button" onClick={() => setShowCreate(false)}
                  className="px-4 py-2 rounded-lg text-sm text-text hover:text-text-heading transition-colors">Cancel</button>
                <button type="submit"
                  className="px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-hover transition-colors">Create</button>
              </div>
            </form>
          </motion.div>
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-12"><Loader2 className="w-8 h-8 text-primary animate-spin" /></div>
      ) : apps.length === 0 ? (
        <div className="text-center py-12">
          <Send className="w-12 h-12 text-text/40 mx-auto mb-3" />
          <p className="text-text">No applications yet. Start tracking your applications!</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {apps.map((app, i) => (
            <motion.div
              key={app.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="p-4 rounded-xl bg-surface border border-border hover:border-primary/20 transition-all duration-200"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-base font-semibold text-text-heading">
                      {app.job_title || `Application #${app.id}`}
                    </h3>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium border ${statusColors[app.status] || 'bg-gray-500/20 text-gray-400'}`}>
                      {app.status}
                    </span>
                  </div>
                  {app.company && <p className="text-sm text-text">{app.company}</p>}
                  {app.notes && <p className="text-xs text-text/60 mt-1">{app.notes}</p>}
                </div>
                <button onClick={() => handleDelete(app.id)}
                  className="p-2 rounded-lg text-text hover:text-danger hover:bg-danger/10 transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
