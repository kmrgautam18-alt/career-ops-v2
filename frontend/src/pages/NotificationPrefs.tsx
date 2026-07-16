import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bell, Mail, MessageCircle, Smartphone, Loader2, type LucideIcon } from 'lucide-react';
import apiClient from '../api/client';

function IconWrapper({ icon: Icon }: { icon: LucideIcon }) {
  return <Icon className="w-4 h-4" />;
}

const CHANNEL_ICONS: Record<string, LucideIcon> = {
  email: Mail, telegram: MessageCircle, push: Smartphone, in_app: Bell,
};

const EVENT_LABELS: Record<string, string> = {
  'application.created': 'Application Submitted',
  'application.updated': 'Status Changed',
  'interview.scheduled': 'Interview Scheduled',
  'followup.sent': 'Follow-up Sent',
  'ai.complete': 'AI Task Complete',
  'digest.daily': 'Daily Digest',
  'job.found': 'New Jobs Found',
};

export function NotificationPrefs() {
  const [prefs, setPrefs] = useState<Record<string, Record<string, boolean>>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<string | null>(null);

  useEffect(() => {
    apiClient.get('/notifications/preferences/')
      .then(r => setPrefs(r.data.data || {}))
      .finally(() => setLoading(false));
  }, []);

  const toggle = async (event: string, channel: string) => {
    setSaving(`${event}-${channel}`);
    const current = prefs[event]?.[channel] ?? true;
    try {
      await apiClient.put(`/notifications/preferences/${event}/${channel}?enabled=${!current}`);
      setPrefs(p => ({
        ...p,
        [event]: { ...(p[event] || {}), [channel]: !current },
      }));
    } catch {}
    setSaving(null);
  };

  if (loading) return <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 text-primary animate-spin" /></div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-text-heading flex items-center gap-3">
          <Bell className="w-6 h-6 text-primary" />
          Notification Preferences
        </h1>
        <p className="text-text-muted mt-1">Control which events notify you and through which channels</p>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        className="p-6 rounded-2xl bg-surface border border-border/60 overflow-x-auto"
      >
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border/40">
              <th className="text-left py-3 px-2 text-text-heading font-medium">Event</th>
              {['email', 'telegram', 'push', 'in_app'].map(ch => (
                <th key={ch} className="text-center py-3 px-2 text-text-muted">
                  <div className="flex flex-col items-center gap-1">
                    {CHANNEL_ICONS[ch] ? <IconWrapper icon={CHANNEL_ICONS[ch]} /> : null}
                    <span className="text-[10px] uppercase">{ch}</span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Object.entries(prefs).map(([event, channels]) => (
              <tr key={event} className="border-b border-border/20 hover:bg-surface-light/50 transition-colors">
                <td className="py-3 px-2 text-text">{EVENT_LABELS[event] || event}</td>
                {['email', 'telegram', 'push', 'in_app'].map(ch => (
                  <td key={ch} className="text-center py-3 px-2">
                    <button
                      onClick={() => toggle(event, ch)}
                      disabled={saving === `${event}-${ch}`}
                      className={`w-8 h-8 rounded-lg transition-all duration-200 ${
                        channels[ch]
                          ? 'bg-primary/20 text-primary border border-primary/30'
                          : 'bg-surface-lighter text-text-muted border border-border/40'
                      } hover:scale-110 disabled:opacity-50`}
                    >
                      {saving === `${event}-${ch}` ? (
                        <Loader2 className="w-3.5 h-3.5 mx-auto animate-spin" />
                      ) : channels[ch] ? '✓' : '—'}
                    </button>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </motion.div>
    </div>
  );
}
