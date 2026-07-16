import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Building2, Plus, Users, Loader2, UserPlus,
  Shield, ShieldCheck, ShieldAlert, X, Check,
  ChevronRight, Clock,
} from 'lucide-react';
import apiClient from '../api/client';

interface Organization {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  max_members: number;
  is_active: boolean;
}

interface Member {
  id: number;
  user_id: number;
  role: string;
  joined_at: string;
}

export function Organizations() {
  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState<number | null>(null);
  const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null);
  const [members, setMembers] = useState<Member[]>([]);
  const [form, setForm] = useState({ name: '', slug: '', description: '' });
  const [inviteUserId, setInviteUserId] = useState('');
  const [inviteRole, setInviteRole] = useState('member');

  useEffect(() => {
    apiClient.get('/organizations/')
      .then(r => setOrgs(r.data.data || []))
      .catch(() => setOrgs([]))
      .finally(() => setLoading(false));
  }, []);

  const fetchMembers = async (orgId: number) => {
    try {
      const r = await apiClient.get(`/organizations/${orgId}/members`);
      setMembers(r.data.data || []);
    } catch {
      setMembers([]);
    }
  };

  const createOrg = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post(`/organizations/?name=${encodeURIComponent(form.name)}&slug=${encodeURIComponent(form.slug)}${form.description ? `&description=${encodeURIComponent(form.description)}` : ''}`);
      const r = await apiClient.get('/organizations/');
      setOrgs(r.data.data || []);
      setShowCreateModal(false);
      setForm({ name: '', slug: '', description: '' });
    } catch {}
  };

  const inviteMember = async () => {
    if (!inviteUserId || showInviteModal === null) return;
    try {
      await apiClient.post(`/organizations/${showInviteModal}/invite?user_id=${parseInt(inviteUserId)}&role=${inviteRole}`);
      setInviteUserId('');
      fetchMembers(showInviteModal);
    } catch {}
  };

  const openOrg = async (org: Organization) => {
    setSelectedOrg(org);
    setShowInviteModal(null);
    fetchMembers(org.id);
  };

  const roleIcon = (role: string) => {
    switch (role) {
      case 'owner': return <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />;
      case 'admin': return <Shield className="w-3.5 h-3.5 text-primary" />;
      default: return <ShieldAlert className="w-3.5 h-3.5 text-text-muted" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 text-primary animate-spin" />
          <p className="text-text-muted text-sm">Loading organizations...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-7 max-w-6xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between flex-wrap gap-4"
      >
        <div>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 shadow-lg">
              <Building2 className="w-full h-full text-white" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Organizations</h1>
          </div>
          <p className="text-text-muted mt-1">Create teams, invite members, and manage shared workspaces</p>
        </div>
        <button onClick={() => setShowCreateModal(true)}
          className="group relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
        >
          <Plus className="w-4 h-4" />
          <span>New Organization</span>
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
        </button>
      </motion.div>

      {/* Stats Bar */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className="flex items-center gap-6 p-4 rounded-2xl bg-surface border border-border/60"
      >
        <div className="flex items-center gap-2">
          <Building2 className="w-4 h-4 text-primary" />
          <span className="text-sm text-text-heading font-medium">{orgs.length}</span>
          <span className="text-xs text-text-muted">Organizations</span>
        </div>
        <div className="w-px h-6 bg-border/60" />
        <div className="flex items-center gap-2">
          <Users className="w-4 h-4 text-accent" />
          <span className="text-sm text-text-heading font-medium">{orgs.reduce((sum, o) => sum + (o.max_members || 0), 0)}</span>
          <span className="text-xs text-text-muted">Total Capacity</span>
        </div>
        <div className="w-px h-6 bg-border/60" />
        <div className="flex items-center gap-2 text-xs text-text-muted">
          <Check className="w-3.5 h-3.5 text-success" />
          {orgs.filter(o => o.is_active).length} Active
        </div>
      </motion.div>

      {/* Org Grid */}
      {orgs.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-20 glass-panel rounded-2xl"
        >
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center mb-5 border border-indigo-500/10">
            <Building2 className="w-10 h-10 text-primary" />
          </div>
          <p className="text-lg font-semibold text-text-heading mb-1">No organizations yet</p>
          <p className="text-sm text-text-muted mb-8 max-w-md text-center">
            Create your first team workspace to collaborate with others on shared job boards and applications.
          </p>
          <button onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury"
          >
            <Plus className="w-4 h-4" />
            Create Your First Organization
          </button>
        </motion.div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {orgs.map((org, i) => (
            <motion.div
              key={org.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              onClick={() => openOrg(org)}
            >
              <div className={`group relative p-5 rounded-2xl bg-surface border transition-all duration-500 cursor-pointer overflow-hidden
                ${selectedOrg?.id === org.id
                  ? 'border-primary/40 bg-primary/5 shadow-lg shadow-primary-glow/10'
                  : 'border-border/60 hover:border-border-glow/40 hover:bg-surface-light/20'
                }`}
              >
                {/* Shine */}
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                  <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
                </div>
                <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-3xl" />

                <div className="relative">
                  {/* Icon */}
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${
                    selectedOrg?.id === org.id
                      ? 'from-primary to-accent'
                      : 'from-indigo-500 to-purple-600'
                  } p-3 mb-4 shadow-lg flex items-center justify-center`}>
                    <Building2 className="w-full h-full text-white" />
                  </div>

                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="font-semibold text-text-heading text-base">{org.name}</h3>
                      <p className="text-xs text-text-muted mt-0.5">/{org.slug}</p>
                    </div>
                    <div className={`px-2.5 py-1 rounded-lg text-[10px] font-medium border ${
                      org.is_active
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                        : 'bg-red-500/10 text-red-400 border-red-500/20'
                    }`}>
                      {org.is_active ? 'Active' : 'Inactive'}
                    </div>
                  </div>

                  {org.description && (
                    <p className="text-xs text-text-muted mb-4 line-clamp-2">{org.description}</p>
                  )}

                  <div className="flex items-center justify-between pt-3 border-t border-border/30">
                    <div className="flex items-center gap-1.5 text-xs text-text-muted">
                      <Users className="w-3.5 h-3.5" />
                      <span>Up to {org.max_members} members</span>
                    </div>
                    <ChevronRight className={`w-4 h-4 text-text-muted transition-all duration-300 ${
                      selectedOrg?.id === org.id ? 'translate-x-1 text-primary' : 'group-hover:translate-x-0.5'
                    }`} />
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Selected Org Detail */}
      <AnimatePresence>
        {selectedOrg && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="glass-panel-strong rounded-2xl overflow-hidden"
          >
            <div className="flex items-center justify-between px-6 py-4 border-b border-border/40 bg-surface/30">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 p-2 flex items-center justify-center">
                  <Building2 className="w-full h-full text-white" />
                </div>
                <div>
                  <h2 className="text-base font-semibold text-text-heading">{selectedOrg.name}</h2>
                  <p className="text-xs text-text-muted">{members.length} members · /{selectedOrg.slug}</p>
                </div>
              </div>
              <button
                onClick={() => setShowInviteModal(selectedOrg.id)}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-xs font-semibold btn-luxury"
              >
                <UserPlus className="w-3.5 h-3.5" />
                Invite Member
              </button>
            </div>

            {/* Members List */}
            <div className="p-6">
              <div className="flex items-center gap-2 mb-4">
                <Users className="w-4 h-4 text-text-muted" />
                <h3 className="text-sm font-medium text-text-heading">Members</h3>
                <span className="text-xs text-text-muted">({members.length})</span>
              </div>
              {members.length === 0 ? (
                <p className="text-sm text-text-muted py-8 text-center">No members yet. Invite someone!</p>
              ) : (
                <div className="space-y-2">
                  {members.map(m => (
                    <div key={m.id}
                      className="flex items-center justify-between p-3 rounded-xl bg-surface-light/30 border border-border/30 hover:bg-surface-light/50 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                          <span className="text-xs font-bold text-white">U{m.user_id}</span>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-text-heading">User #{m.user_id}</p>
                          <p className="text-[11px] text-text-muted flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            Joined {new Date(m.joined_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-1.5 text-xs font-medium">
                        {roleIcon(m.role)}
                        <span className="capitalize text-text-muted">{m.role}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Create Modal */}
      <AnimatePresence>
        {showCreateModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowCreateModal(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="w-full max-w-md glass-panel-strong rounded-2xl p-6 sm:p-8"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 p-2 flex items-center justify-center">
                    <Plus className="w-full h-full text-white" />
                  </div>
                  <h2 className="text-lg font-semibold text-text-heading">New Organization</h2>
                </div>
                <button onClick={() => setShowCreateModal(false)}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <form onSubmit={createOrg} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Organization Name *</label>
                  <input value={form.name} onChange={e => setForm({ ...form, name: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                    placeholder="e.g., Acme Corp" required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Slug *</label>
                  <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted text-sm">/</span>
                    <input value={form.slug} onChange={e => setForm({ ...form, slug: e.target.value.replace(/[^a-z0-9-]/g, '') })}
                      className="w-full pl-8 pr-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                      placeholder="my-organization" required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Description</label>
                  <textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[80px] resize-y"
                    placeholder="What's this organization for?"
                  />
                </div>
                <div className="flex justify-end gap-3 pt-2">
                  <button type="button" onClick={() => setShowCreateModal(false)}
                    className="px-5 py-2.5 rounded-xl text-sm text-text-muted hover:text-text-heading transition-colors">Cancel</button>
                  <button type="submit"
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury">
                    Create Organization
                  </button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Invite Modal */}
      <AnimatePresence>
        {showInviteModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowInviteModal(null)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="w-full max-w-sm glass-panel-strong rounded-2xl p-6"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-5">
                <h2 className="text-lg font-semibold text-text-heading flex items-center gap-2.5">
                  <UserPlus className="w-5 h-5 text-primary" />
                  Invite Member
                </h2>
                <button onClick={() => setShowInviteModal(null)}
                  className="p-2 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">User ID *</label>
                  <input type="number" value={inviteUserId} onChange={e => setInviteUserId(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                    placeholder="Enter user ID to invite" required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-heading mb-1.5">Role</label>
                  <div className="flex gap-2">
                    {(['member', 'admin'] as const).map(r => (
                      <button key={r} onClick={() => setInviteRole(r)}
                        className={`flex-1 py-2.5 rounded-xl text-sm font-medium transition-all border capitalize ${
                          inviteRole === r
                            ? 'bg-primary/15 text-primary border-primary/30'
                            : 'bg-background text-text-muted border-border-light hover:text-text-heading'
                        }`}
                      >
                        {r === 'member' ? '👤 Member' : '🛡️ Admin'}
                      </button>
                    ))}
                  </div>
                </div>
                <button onClick={inviteMember} disabled={!inviteUserId}
                  className="w-full py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-luxury disabled:opacity-50"
                >
                  Send Invitation
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
