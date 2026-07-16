import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Bell, Mail, MessageCircle, Smartphone, Loader2,
  CheckCircle2, XCircle, Settings2,
} from 'lucide-react';
import apiClient from '../api/client';

interface PrefsMap {
  [eventType: string]: {
    [channel: string]: boolean;
  };
}

const EVENT_CATEGORIES: Record<string, { label: string; events: string[] }> = {
  applications: {
    label: '📋 Applications',
    events: ['application.created', 'application.updated', 'application.deleted'],
  },
  interviews: {
    label: '🎯 Interviews',
    events: ['interview.scheduled', 'interview.reminder'],
  },
  automation: {
    label: '🤖 Automation',
    events: ['followup.sent', 'ai.complete', 'job.found'],
  },
  digests: {
    label: '📊 Digests',
    events: ['digest.daily', 'digest.weekly'],
  },
  system: {
    label: '🔔 System',
    events: ['system.alert'],
  },
};

const CHANNELS = [
  { id: 'email', label: 'Email', icon: Mail, gradient: 'from-blue-500 to-indigo-600' },
  { id: 'telegram', label: 'Telegram', icon: MessageCircle, gradient: 'from-sky-500 to-blue-600' },
  { id: 'push', label: 'Push', icon: Smartphone, gradient: 'from-purple-500 to-pink-600' },
  { id: 'in_app', label: 'In-App', icon: Bell, gradient: 'from-emerald-500 to-teal-600' },
];

function lookupLabel(eventType: string): string {
  const labels: Record<string, string> = {
    'application.created': 'Application Submitted',
    'application.updated': 'Status Changed',
    'application.deleted': 'Application Deleted',
    'interview.scheduled': 'Interview Scheduled',
    'interview.reminder': 'Interview Reminder',
    'followup.sent': 'Follow-up Sent',
    'ai.complete': 'AI Task Complete',
    'job.found': 'New Jobs Found',
    'digest.daily': 'Daily Digest',
    'digest.weekly': 'Weekly Digest',
    'system.alert': 'System Alert',
  };
  return labels[eventType] || eventType;
}

export function NotificationPrefs() {
  const [prefs, setPrefs] = useState<PrefsMap>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<{[key: string]: 'saving' | 'saved' | 'error'}>({});
  useEffect(() => {
    apiClient.get('/notifications/preferences/')
      .then(r => setPrefs(r.data.data || {}))
      .catch(() => setPrefs({}))
      .finally(() => setLoading(false));
  }, []);

  const toggle = async (event: string, channel: string) => {
    const key = `${event}:${channel}`;
    const current = prefs[event]?.[channel] ?? true;
    const newVal = !current;

    setSaving(prev => ({ ...prev, [key]: 'saving' }));
    setPrefs(p => ({
      ...p,
      [event]: { ...(p[event] || {}), [channel]: newVal },
    }));

    try {
      await apiClient.put(`/notifications/preferences/${event}/${channel}?enabled=${newVal}`);
      setSaving(prev => ({ ...prev, [key]: 'saved' }));
      setTimeout(() => setSaving(prev => {
        const next = { ...prev };
        delete next[key];
        return next;
      }), 1500);
    } catch {
      setSaving(prev => ({ ...prev, [key]: 'error' }));
      // Revert
      setPrefs(p => ({
        ...p,
        [event]: { ...(p[event] || {}), [channel]: !newVal },
      }));
    }
  };

  const toggleAll = async (enabled: boolean) => {
    try {
      await apiClient.put(`/notifications/preferences/all?enabled=${enabled}`);
      const newPrefs: PrefsMap = {};
      Object.keys(prefs).forEach(event => {
        newPrefs[event] = {};
        CHANNELS.forEach(ch => { newPrefs[event][ch.id] = enabled; });
      });
      setPrefs(newPrefs);
    } catch {}
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 text-primary animate-spin" />
          <p className="text-text-muted text-sm">Loading preferences...</p>
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
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 p-2.5 shadow-lg">
              <Bell className="w-full h-full text-white" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Notifications</h1>
          </div>
          <p className="text-text-muted mt-1">Control which events notify you and through which channels</p>
        </div>

        {/* Global Toggles */}
        <div className="flex gap-2">
          <button
            onClick={() => toggleAll(true)}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium hover:bg-emerald-500/20 transition-all"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            Enable All
          </button>
          <button
            onClick={() => toggleAll(false)}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-medium hover:bg-red-500/20 transition-all"
          >
            <XCircle className="w-3.5 h-3.5" />
            Disable All
          </button>
        </div>
      </motion.div>

      {/* Channel Legend */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className="flex items-center gap-4 p-4 rounded-2xl bg-surface border border-border/60"
      >
        <Settings2 className="w-4 h-4 text-text-muted" />
        {CHANNELS.map(ch => (
          <div key={ch.id} className="flex items-center gap-1.5 text-xs text-text-muted">
            <ch.icon className="w-3.5 h-3.5" />
            <span>{ch.label}</span>
          </div>
        ))}
        <div className="ml-auto text-xs text-text-muted/50">
          {Object.keys(prefs).length} event types · {CHANNELS.length} channels
        </div>
      </motion.div>

      {/* Event Categories */}
      {Object.entries(EVENT_CATEGORIES).map(([catKey, category], catIdx) => {
        const visibleEvents = category.events.filter(e => e in prefs);
        if (visibleEvents.length === 0) return null;

        return (
          <motion.div
            key={catKey}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.08 + catIdx * 0.06 }}
            className="glass-panel-strong rounded-2xl overflow-hidden"
          >
            {/* Category Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-border/40 bg-surface/30">
              <h2 className="text-sm font-semibold text-text-heading">{category.label}</h2>
              <span className="text-xs text-text-muted">
                {visibleEvents.length} event{visibleEvents.length > 1 ? 's' : ''}
              </span>
            </div>

            {/* Event Rows */}
            <div className="divide-y divide-border/20">
              {visibleEvents.map((eventType, eIdx) => {
                const channels = prefs[eventType] || {};
                const enabledCount = CHANNELS.filter(ch => channels[ch.id]).length;

                return (
                  <motion.div
                    key={eventType}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 + eIdx * 0.03 }}
                    className="flex items-center justify-between px-6 py-3.5 hover:bg-surface-light/20 transition-colors group"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <div className={`w-2 h-2 rounded-full flex-shrink-0 ${
                        enabledCount > 0 ? 'bg-primary shadow-sm shadow-primary/50' : 'bg-border'
                      }`} />
                      <div>
                        <p className="text-sm font-medium text-text-heading">{lookupLabel(eventType)}</p>
                        <p className="text-[11px] text-text-muted mt-0.5">
                          {enabledCount}/{CHANNELS.length} channels active
                        </p>
                      </div>
                    </div>

                    {/* Channel Toggles */}
                    <div className="flex items-center gap-1.5">
                      {CHANNELS.map(ch => {
                        const isEnabled = channels[ch.id] ?? true;
                        const saveKey = `${eventType}:${ch.id}`;
                        const status = saving[saveKey];

                        return (
                          <button
                            key={ch.id}
                            onClick={() => toggle(eventType, ch.id)}
                            disabled={status === 'saving'}
                            className={`relative w-9 h-9 rounded-lg flex items-center justify-center transition-all duration-200 border ${
                              isEnabled
                                ? `bg-gradient-to-br ${ch.gradient} text-white border-transparent shadow-sm`
                                : 'bg-surface-lighter text-text-muted border-border/40 hover:border-border-light'
                            } disabled:opacity-50 hover:scale-110 active:scale-95`}
                            title={`${ch.label}: ${isEnabled ? 'On' : 'Off'}`}
                          >
                            {status === 'saving' ? (
                              <Loader2 className="w-3.5 h-3.5 animate-spin" />
                            ) : status === 'saved' ? (
                              <CheckCircle2 className="w-3.5 h-3.5" />
                            ) : (
                              <ch.icon className="w-3.5 h-3.5" />
                            )}
                          </button>
                        );
                      })}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        );
      })}

      {/* Empty State */}
      {Object.keys(prefs).length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-20 glass-panel rounded-2xl"
        >
          <div className="w-16 h-16 rounded-2xl bg-primary-light flex items-center justify-center mb-4">
            <Bell className="w-8 h-8 text-primary" />
          </div>
          <p className="text-text-heading font-medium mb-1">No notification preferences</p>
          <p className="text-text-muted text-sm">Preferences will appear once you have events to configure</p>
        </motion.div>
      )}

      {/* Footer */}
      <p className="text-center text-[11px] text-text-muted/50">
        Changes are saved instantly · Toggle individual channels per event type
      </p>
    </div>
  );
}
