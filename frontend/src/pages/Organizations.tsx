import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Building2, Plus, Users, Loader2, UserPlus } from 'lucide-react';
import apiClient from '../api/client';

interface Organization {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  max_members: number;
  is_active: boolean;
}

export function Organizations() {
  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState('');
  const [slug, setSlug] = useState('');

  useEffect(() => {
    apiClient.get('/organizations/')
      .then(r => setOrgs(r.data.data || []))
      .finally(() => setLoading(false));
  }, []);

  const createOrg = async () => {
    if (!name || !slug) return;
    try {
      await apiClient.post(`/organizations/?name=${encodeURIComponent(name)}&slug=${encodeURIComponent(slug)}`);
      const r = await apiClient.get('/organizations/');
      setOrgs(r.data.data || []);
      setShowCreate(false);
      setName('');
      setSlug('');
    } catch {}
  };

  if (loading) return <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 text-primary animate-spin" /></div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-text-heading flex items-center gap-3">
            <Building2 className="w-6 h-6 text-primary" />
            Organizations
          </h1>
          <p className="text-text-muted mt-1">Manage your teams and shared workspaces</p>
        </div>
        <button onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury"
        >
          <Plus className="w-4 h-4" />
          New Org
        </button>
      </motion.div>

      {showCreate && (
        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
          className="p-5 rounded-2xl bg-surface border border-border/60 space-y-4"
        >
          <input value={name} onChange={e => setName(e.target.value)}
            className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading"
            placeholder="Organization Name" />
          <input value={slug} onChange={e => setSlug(e.target.value.replace(/[^a-z0-9-]/g, ''))}
            className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading"
            placeholder="slug (e.g., my-team)" />
          <button onClick={createOrg}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-luxury"
          >
            Create Organization
          </button>
        </motion.div>
      )}

      <div className="grid sm:grid-cols-2 gap-4">
        {orgs.map(org => (
          <motion.div key={org.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="p-5 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all group"
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent p-2 flex items-center justify-center">
                <Users className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-text-heading">{org.name}</h3>
                <p className="text-xs text-text-muted">/{org.slug}</p>
              </div>
            </div>
            {org.description && <p className="text-sm text-text-muted mb-3">{org.description}</p>}
            <div className="flex items-center gap-2 text-xs text-text-muted">
              <UserPlus className="w-3 h-3" />
              <span>Up to {org.max_members} members</span>
            </div>
          </motion.div>
        ))}
        {orgs.length === 0 && (
          <div className="col-span-2 text-center py-12 text-text-muted">
            <Building2 className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p>No organizations yet. Create your first team!</p>
          </div>
        )}
      </div>
    </div>
  );
}
