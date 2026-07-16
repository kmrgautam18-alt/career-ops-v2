import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search, Sparkles, Send, Calendar, TrendingUp,
  CheckCircle2, ArrowRight, ChevronRight, Play,
  FileText, Briefcase, Bot, Mail, Bell,
  Users, Shield, Zap, BarChart3, Globe,
} from 'lucide-react';

const PIPELINE_STEPS = [
  {
    id: 'discover',
    icon: Search,
    title: '1. Discover Jobs',
    subtitle: 'AI-powered job sourcing from LinkedIn, Indeed & career portals',
    gradient: 'from-blue-500 to-indigo-600',
    details: [
      'Scrape jobs from 18+ company career portals',
      'AI-filter by skills, location, and salary',
      'Auto-detect new matching opportunities daily',
      'Save and organize by priority and fit score',
    ],
    apiCall: 'POST /api/v1/auto-apply/scrape',
  },
  {
    id: 'optimize',
    icon: Sparkles,
    title: '2. AI Resume Tailoring',
    subtitle: 'Gemini AI analyzes and optimizes your resume for each role',
    gradient: 'from-purple-500 to-pink-600',
    details: [
      'ATS score analysis (73% → 92% avg improvement)',
      'Keyword gap detection against job description',
      'Auto-generate tailored resume for each application',
      'Custom cover letter generation with AI',
    ],
    apiCall: 'POST /api/v1/auto-apply/{id}/optimize',
  },
  {
    id: 'apply',
    icon: Send,
    title: '3. Auto-Apply',
    subtitle: 'Automated application submission with tailored materials',
    gradient: 'from-cyan-500 to-blue-600',
    details: [
      'Send tailored application emails via SMTP',
      'Embed AI-optimized resume inline',
      'Track delivery and open rates',
      'Daily application limits with smart scheduling',
    ],
    apiCall: 'POST /api/v1/auto-apply/{id}/send',
  },
  {
    id: 'track',
    icon: Calendar,
    title: '4. Track & Interview',
    subtitle: 'Monitor status, get interview invites, schedule follow-ups',
    gradient: 'from-emerald-500 to-teal-600',
    details: [
      'Real-time status tracking (sourced → offered)',
      'Auto-detect interview dates from emails',
      'Calendar integration for interview scheduling',
      'Smart follow-up scheduling (7→14→21 day intervals)',
    ],
    apiCall: 'POST /api/v1/auto-apply/{id}/interview',
  },
  {
    id: 'analytics',
    icon: TrendingUp,
    title: '5. Analytics & Insights',
    subtitle: 'Visual dashboards showing your career search velocity',
    gradient: 'from-amber-500 to-orange-600',
    details: [
      'Pipeline conversion rates at every stage',
      'ATS score trends across applications',
      'Response rate analytics by company/industry',
      'Skill gap analysis and trending market demands',
    ],
    apiCall: 'GET /api/v1/dashboard',
  },
];

const MODULES = [
  { icon: Briefcase, label: 'Job Management', color: 'from-indigo-500 to-purple-500', desc: 'CRUD, search, filter, AI match' },
  { icon: FileText, label: 'Resume Engine', color: 'from-cyan-500 to-blue-500', desc: 'Upload, parse, ATS score, optimize' },
  { icon: Send, label: 'Applications', color: 'from-emerald-500 to-teal-500', desc: 'Track status, notes, interviews' },
  { icon: Bot, label: 'AI Tools', color: 'from-amber-500 to-orange-500', desc: 'Questions, match, streaming SSE' },
  { icon: Zap, label: 'Auto-Apply', color: 'from-rose-500 to-pink-500', desc: 'Scrape, tailor, email, follow-up' },
  { icon: Bell, label: 'Notifications', color: 'from-violet-500 to-indigo-500', desc: 'Telegram, Email, Slack, In-App' },
  { icon: Users, label: 'Organizations', color: 'from-blue-500 to-indigo-600', desc: 'Teams, roles, shared boards' },
  { icon: Shield, label: 'Security', color: 'from-gray-500 to-slate-600', desc: 'JWT, OAuth, RBAC, Argon2' },
  { icon: BarChart3, label: 'Monitoring', color: 'from-green-500 to-emerald-600', desc: 'Prometheus, Grafana, Loki' },
  { icon: Globe, label: 'Deployment', color: 'from-sky-500 to-cyan-600', desc: 'Docker, RHEL, EC2, Windows' },
];

export function HowItWorks() {
  const [activeStep, setActiveStep] = useState(0);
  const [autoPlay, setAutoPlay] = useState(true);

  // Auto-play through steps
  useEffect(() => {
    if (!autoPlay) return;
    const timer = setInterval(() => {
      setActiveStep(prev => (prev + 1) % PIPELINE_STEPS.length);
    }, 4000);
    return () => clearInterval(timer);
  }, [autoPlay]);

  const currentStep = PIPELINE_STEPS[activeStep];

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-center gap-3 mb-1">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent p-2.5 shadow-lg">
            <Play className="w-full h-full text-white" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">How Career-Ops Works</h1>
        </div>
        <p className="text-text-muted mt-1">End-to-end guide from job discovery to offer letter</p>
      </motion.div>

      {/* Animated Pipeline Flow */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel-strong rounded-2xl p-6 sm:p-8"
      >
        {/* Pipeline Steps Bar */}
        <div className="relative mb-10">
          {/* Connecting line */}
          <div className="absolute top-5 left-[5%] right-[5%] h-[2px] bg-gradient-to-r from-primary/20 via-primary to-accent/20 hidden md:block" />

          <div className="flex justify-between gap-2 overflow-x-auto pb-2">
            {PIPELINE_STEPS.map((step, i) => {
              const isActive = i === activeStep;
              const isDone = i < activeStep;
              return (
                <button
                  key={step.id}
                  onClick={() => { setActiveStep(i); setAutoPlay(false); }}
                  className={`flex flex-col items-center gap-2 min-w-[80px] transition-all duration-300 group`}
                >
                  <div className={`relative w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-500 ${
                    isActive
                      ? `bg-gradient-to-br ${step.gradient} shadow-lg scale-110`
                      : isDone
                      ? 'bg-primary/20 border border-primary/30'
                      : 'bg-surface-lighter border border-border/40 group-hover:border-border'
                  }`}>
                    {isDone ? (
                      <CheckCircle2 className="w-5 h-5 text-primary" />
                    ) : (
                      <step.icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-text-muted'}`} />
                    )}
                    {/* Pulse ring on active */}
                    {isActive && (
                      <span className={`absolute inset-0 rounded-xl animate-ping opacity-20 bg-gradient-to-br ${step.gradient}`} />
                    )}
                  </div>
                  <span className={`text-[10px] font-medium text-center leading-tight ${
                    isActive ? 'text-primary' : isDone ? 'text-text' : 'text-text-muted'
                  }`}>
                    {step.title.replace(/^\d+\.\s*/, '')}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Auto-play toggle */}
          <button
            onClick={() => setAutoPlay(!autoPlay)}
            className={`absolute top-0 right-0 flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[10px] font-medium transition-all border ${
              autoPlay
                ? 'bg-primary/10 text-primary border-primary/20'
                : 'bg-surface text-text-muted border-border/40'
            }`}
          >
            {autoPlay ? '⏸ Pause' : '▶ Auto-Play'}
          </button>
        </div>

        {/* Active Step Detail */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep.id}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.4, ease: [0.25, 0.46, 0.45, 0.94] }}
          >
            <div className="grid lg:grid-cols-5 gap-6">
              {/* Left: Step info */}
              <div className="lg:col-span-3 space-y-4">
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${currentStep.gradient} p-3.5 shadow-lg mb-2`}>
                  <currentStep.icon className="w-full h-full text-white" />
                </div>
                <h2 className="text-xl sm:text-2xl font-bold text-text-heading">{currentStep.title}</h2>
                <p className="text-text-muted">{currentStep.subtitle}</p>

                <div className="space-y-2.5">
                  {currentStep.details.map((detail, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-start gap-2.5"
                    >
                      <div className={`w-5 h-5 rounded-lg bg-gradient-to-br ${currentStep.gradient} flex items-center justify-center flex-shrink-0 mt-0.5`}>
                        <CheckCircle2 className="w-3 h-3 text-white" />
                      </div>
                      <span className="text-sm text-text">{detail}</span>
                    </motion.div>
                  ))}
                </div>

                {/* API Call badge */}
                <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-light/50 border border-border/30">
                  <code className="text-[11px] font-mono text-primary">{currentStep.apiCall}</code>
                  <span className="text-[10px] text-text-muted">REST API</span>
                </div>
              </div>

              {/* Right: Visual pipeline demo */}
              <div className="lg:col-span-2">
                <div className="relative h-full min-h-[280px] rounded-xl bg-gradient-to-br from-surface-light/30 to-surface-lighter/20 border border-border/30 overflow-hidden p-5">
                  {/* Animated pipeline visualization based on step */}
                  {activeStep === 0 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
                      <div className="flex items-center gap-2 text-sm text-text-heading font-medium mb-4">
                        <Search className="w-4 h-4 text-blue-400" /> Scanning job portals...
                      </div>
                      {['Senior Engineer @ Google', 'Full Stack @ Meta', 'DevOps @ Amazon', 'ML Engineer @ Stripe'].map((job, i) => (
                        <motion.div key={job}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.15 }}
                          className="flex items-center justify-between p-2.5 rounded-lg bg-surface/50 border border-border/30"
                        >
                          <span className="text-xs text-text">{job}</span>
                          <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-400/10 text-blue-400 border border-blue-400/20">92% match</span>
                        </motion.div>
                      ))}
                    </motion.div>
                  )}

                  {activeStep === 1 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
                      <div className="flex items-center gap-2 text-sm text-text-heading font-medium mb-4">
                        <Sparkles className="w-4 h-4 text-purple-400" /> AI Optimizing resumes...
                      </div>
                      <div className="p-3 rounded-lg bg-surface/50 border border-border/30 space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-text-muted">ATS Score</span>
                          <span className="text-success font-bold">73% → 92%</span>
                        </div>
                        <div className="h-2 rounded-full bg-surface-lighter overflow-hidden">
                          <motion.div
                            initial={{ width: '73%' }}
                            animate={{ width: '92%' }}
                            transition={{ duration: 1.5, ease: 'easeOut' }}
                            className="h-full rounded-full bg-gradient-to-r from-purple-500 to-pink-500"
                          />
                        </div>
                      </div>
                      <div className="text-xs text-text-muted p-2">✓ 12 keywords matched · 3 gaps identified → auto-filled</div>
                    </motion.div>
                  )}

                  {activeStep === 2 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
                      <div className="flex items-center gap-2 text-sm text-text-heading font-medium mb-4">
                        <Send className="w-4 h-4 text-cyan-400" /> Sending applications...
                      </div>
                      {['hr@google.com', 'careers@meta.com', 'hr@amazon.com'].map((email, i) => (
                        <motion.div key={email}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.2 }}
                          className="flex items-center gap-2 p-2.5 rounded-lg bg-surface/50 border border-border/30"
                        >
                          <Mail className="w-3.5 h-3.5 text-cyan-400" />
                          <span className="text-xs text-text flex-1">{email}</span>
                          <CheckCircle2 className="w-3.5 h-3.5 text-success" />
                        </motion.div>
                      ))}
                    </motion.div>
                  )}

                  {activeStep === 3 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
                      <div className="flex items-center gap-2 text-sm text-text-heading font-medium mb-4">
                        <Calendar className="w-4 h-4 text-emerald-400" /> Tracking responses...
                      </div>
                      <div className="space-y-2.5">
                        <motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }}
                          className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-center">
                          <p className="text-sm font-semibold text-emerald-400">🎯 Interview Scheduled!</p>
                          <p className="text-xs text-text-muted mt-1">Google · Senior Engineer · July 25</p>
                        </motion.div>
                        <div className="flex items-center gap-2 text-xs text-text-muted">
                          <span className="px-2 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">⏳ Follow-up in 7 days</span>
                          <span className="px-2 py-1 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">📋 Application Viewed</span>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {activeStep === 4 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
                      <div className="flex items-center gap-2 text-sm text-text-heading font-medium mb-4">
                        <BarChart3 className="w-4 h-4 text-amber-400" /> Analytics Dashboard
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        {[
                          { label: 'Applications', value: '25', color: 'text-blue-400' },
                          { label: 'Interviews', value: '5', color: 'text-emerald-400' },
                          { label: 'Response Rate', value: '28%', color: 'text-amber-400' },
                          { label: 'Avg ATS Score', value: '87%', color: 'text-purple-400' },
                        ].map(stat => (
                          <div key={stat.label} className="p-2.5 rounded-lg bg-surface/50 border border-border/30 text-center">
                            <div className={`text-lg font-bold ${stat.color}`}>{stat.value}</div>
                            <div className="text-[10px] text-text-muted">{stat.label}</div>
                          </div>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Step Navigation */}
        <div className="flex items-center justify-between mt-8 pt-6 border-t border-border/40">
          <button
            onClick={() => { setActiveStep(Math.max(0, activeStep - 1)); setAutoPlay(false); }}
            disabled={activeStep === 0}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm text-text-muted hover:text-text-heading disabled:opacity-30 transition-all border border-border/40 hover:border-border"
          >
            <ChevronRight className="w-4 h-4 rotate-180" /> Previous
          </button>

          <div className="flex items-center gap-1.5">
            {PIPELINE_STEPS.map((_, i) => (
              <button
                key={i}
                onClick={() => { setActiveStep(i); setAutoPlay(false); }}
                className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  i === activeStep ? 'w-6 bg-primary' : 'bg-border hover:bg-border-light'
                }`}
              />
            ))}
          </div>

          <button
            onClick={() => { setActiveStep(Math.min(PIPELINE_STEPS.length - 1, activeStep + 1)); setAutoPlay(false); }}
            disabled={activeStep === PIPELINE_STEPS.length - 1}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm text-text-muted hover:text-text-heading disabled:opacity-30 transition-all border border-border/40 hover:border-border"
          >
            Next <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </motion.div>

      {/* All Modules Grid */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
        <h2 className="text-lg font-semibold text-text-heading mb-4">All Project Modules</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
          {MODULES.map((mod, i) => (
            <motion.div key={mod.label}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.04 }}
              className="group relative p-4 rounded-xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden"
            >
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                <div className="absolute top-0 left-1/4 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
              </div>
              <div className="relative flex items-start gap-3">
                <div className={`w-9 h-9 rounded-lg bg-gradient-to-br ${mod.color} p-2 flex items-center justify-center flex-shrink-0`}>
                  <mod.icon className="w-full h-full text-white" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-text-heading">{mod.label}</p>
                  <p className="text-[11px] text-text-muted mt-0.5">{mod.desc}</p>
                </div>
              </div>
              <div className={`absolute bottom-0 left-3 right-3 h-[1px] bg-gradient-to-r ${mod.color} scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left`} />
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* End-to-End Flow Summary */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
        className="glass-panel rounded-2xl p-6 sm:p-8"
      >
        <h2 className="text-lg font-semibold text-text-heading mb-4">⚡ Complete Data Flow</h2>
        <div className="flex flex-wrap items-center gap-2 text-sm">
          {['Job Discovery', '→', 'AI Optimization', '→', 'Auto-Apply', '→', 'Track Status', '→', 'Interview', '→', 'Offer', '→', 'Analytics'].map((item, i) => (
            <span key={i} className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
              i % 2 === 1
                ? 'text-text-muted'
                : 'bg-gradient-to-r from-primary/10 to-accent/10 border border-primary/20 text-primary'
            }`}>
              {item}
            </span>
          ))}
        </div>
        <div className="mt-4 text-xs text-text-muted">
          <p>Data flows through: <strong className="text-text">FastAPI Backend</strong> → <strong className="text-text">PostgreSQL</strong> (persistence) / <strong className="text-text">Redis</strong> (cache) / <strong className="text-text">Celery</strong> (async) → <strong className="text-text">React Frontend</strong> (real-time updates via WebSocket)</p>
        </div>
      </motion.div>

      {/* Quick Start */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }}
        className="flex flex-col sm:flex-row items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-br from-primary/5 via-primary/5 to-accent/5 border border-primary/10"
      >
        <div>
          <p className="text-sm font-semibold text-text-heading">🚀 Ready to deploy?</p>
          <p className="text-xs text-text-muted mt-1">One command: bash scripts/deploy-zero-click.sh</p>
        </div>
        <a href="/register"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20"
        >
          Get Started Free
          <ArrowRight className="w-4 h-4" />
        </a>
      </motion.div>
    </div>
  );
}
