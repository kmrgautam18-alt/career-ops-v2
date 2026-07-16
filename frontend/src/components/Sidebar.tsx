import { useRef, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Briefcase,
  FileText,
  Send,
  Sparkles,
  Zap,
  LogOut,
  X,
  Sun,
  Moon,
  Bell,
  Users,
  Library,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { AvatarTrail } from './AvatarTrail';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/jobs', icon: Briefcase, label: 'Jobs' },
  { to: '/applications', icon: Send, label: 'Applications' },
  { to: '/resumes', icon: FileText, label: 'Resumes' },
  { to: '/resume-templates', icon: Library, label: 'Templates' },
  { to: '/auto-apply', icon: Zap, label: 'Auto-Apply' },
  { to: '/ai', icon: Sparkles, label: 'AI Tools' },
  { to: '/interview-coach', icon: Sparkles, label: 'Coach' },
  { to: '/notifications', icon: Bell, label: 'Notifications' },
  { to: '/organizations', icon: Users, label: 'Teams' },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  trailFrom?: number;
  trailTo?: number;
  trailVisible?: boolean;
}

export function Sidebar({ open, onClose, trailFrom, trailTo, trailVisible }: SidebarProps) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const sidebarRef = useRef<HTMLDivElement>(null);
  const navRefs = useRef<(HTMLAnchorElement | null)[]>([]);
  const [trailPos, setTrailPos] = useState({ fromY: 0, toY: 0 });

  useEffect(() => {
    navRefs.current = navRefs.current.slice(0, navItems.length);
  }, []);

  useEffect(() => {
    if (!trailVisible || trailFrom === undefined || trailTo === undefined) return;
    if (!sidebarRef.current) return;

    const sidebarRect = sidebarRef.current.getBoundingClientRect();
    const fromEl = navRefs.current[trailFrom];
    const toEl = navRefs.current[trailTo];

    if (fromEl && toEl) {
      const fromRect = fromEl.getBoundingClientRect();
      const toRect = toEl.getBoundingClientRect();
      setTrailPos({
        fromY: fromRect.top - sidebarRect.top,
        toY: toRect.top - sidebarRect.top,
      });
    }
  }, [trailVisible, trailFrom, trailTo]);

  return (
    <>
      {open && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden" onClick={onClose} />
      )}
      <aside
        ref={sidebarRef}
        className={`
          fixed top-0 left-0 z-50 h-full w-64 bg-background/95 backdrop-blur-2xl
          border-r border-border/60
          transform transition-all duration-300 ease-out
          lg:translate-x-0 lg:static lg:z-auto
          ${open ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Logo Section */}
          <div className="flex items-center justify-between p-4 border-b border-border/40">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg shadow-primary-glow/20">
                <Briefcase className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-sm font-bold text-text-heading tracking-tight">
                  Career<span className="text-gradient-primary">Ops</span>
                </h1>
                <p className="text-[10px] text-text-muted tracking-wider uppercase">Dashboard</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden p-1.5 rounded-lg text-text-muted hover:text-text-heading hover:bg-surface-light transition-all"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-3 space-y-1 overflow-y-auto relative">
            {/* Avatar trail - slides from current to target nav item */}
            {trailVisible && trailFrom !== undefined && trailTo !== undefined && trailFrom !== trailTo && (
              <AvatarTrail
                fromY={trailPos.fromY}
                toY={trailPos.toY}
                visible={trailVisible}
              />
            )}

            {navItems.map((item, i) => (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onClose}
                ref={(el) => { navRefs.current[i] = el; }}
                  className={({ isActive }) =>
                    `relative flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 overflow-hidden group ${
                      (!trailVisible && isActive)
                        ? 'text-white'
                        : 'text-text-muted hover:text-text-heading'
                    }`
                  }
                >
                  {({ isActive }) => (
                    <>
                      {/* Active background - hidden during trail animation */}
                      {!trailVisible && isActive && (
                        <motion.div
                          layoutId="navActiveBg"
                          className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary/20 via-primary/10 to-transparent border border-primary/20"
                          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                        />
                      )}
                      <div className="absolute inset-0 rounded-xl bg-surface-light opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                      <div className={`relative z-10 flex items-center gap-3 ${(!trailVisible && isActive) ? 'text-text-heading' : ''}`}>
                        <div className={`w-5 h-5 flex items-center justify-center transition-all duration-200 ${
                          (!trailVisible && isActive) ? 'text-primary' : 'text-text-muted group-hover:text-text'
                        }`}>
                          <item.icon className="w-4 h-4" />
                        </div>
                        <span>{item.label}</span>
                      </div>
                      {/* Active indicator bar */}
                      {!trailVisible && isActive && (
                        <div className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-full bg-gradient-to-b from-primary to-accent" />
                      )}
                    </>                )}
              </NavLink>
            ))}
          </nav>

          {/* Theme Toggle */}
          <div className="px-3 py-2">
            <button
              onClick={toggleTheme}
              className="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium text-text-muted hover:text-text-heading hover:bg-surface-light transition-all duration-200 w-full group"
            >
              <div className="relative w-5 h-5 flex items-center justify-center">
                <Sun className={`w-4 h-4 transition-all duration-300 absolute ${
                  theme === 'light' ? 'opacity-100 rotate-0 scale-100' : 'opacity-0 rotate-90 scale-75'
                }`} />
                <Moon className={`w-4 h-4 transition-all duration-300 absolute ${
                  theme === 'dark' ? 'opacity-100 rotate-0 scale-100' : 'opacity-0 -rotate-90 scale-75'
                }`} />
              </div>
              <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
              <span className="ml-auto text-[10px] text-text-muted/50 uppercase tracking-wider">
                {theme === 'dark' ? '🌙' : '☀️'}
              </span>
            </button>
          </div>

          {/* User Section */}
          <div className="p-3 border-t border-border/40">
            <div className="px-3.5 py-2.5 mb-2 rounded-xl bg-surface/50">
              <p className="text-sm font-medium text-text-heading truncate">{user?.full_name || 'User'}</p>
              <p className="text-[11px] text-text-muted truncate">{user?.email}</p>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium text-text-muted hover:text-danger hover:bg-danger-light transition-all duration-200 w-full group"
            >
              <LogOut className="w-4 h-4 transition-transform group-hover:-translate-x-0.5" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
