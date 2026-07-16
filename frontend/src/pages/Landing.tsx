import { Link, useNavigate } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import {
  Briefcase, FileText, Send, Sparkles, BarChart3,
  ArrowRight, Shield, Zap, Brain, CheckCircle2,
  ChevronRight, Star, Layers, Target, TrendingUp,
  Users, Award, Code2, Globe, Bell, MessageSquare,
  Play, Github, ExternalLink,
} from 'lucide-react';

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (i = 0) => ({
    opacity: 1, y: 0,
    transition: { duration: 0.6, delay: i * 0.1, ease: [0.25, 0.46, 0.45, 0.94] },
  }),
};

const stagger = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

export function Landing() {
  const navigate = useNavigate();
  const heroRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ['start start', 'end start'],
  });
  const heroY = useTransform(scrollYProgress, [0, 1], [0, 150]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

  const features = [
    { icon: Briefcase, title: 'Job Intelligence Hub', desc: 'Track every opportunity with AI-powered search, smart filtering across 18+ company career portals, and real-time market salary insights.', gradient: 'from-indigo-500 to-purple-500', glow: 'rgba(99,102,241,0.15)' },
    { icon: FileText, title: 'Resume Alchemy Engine', desc: 'Upload any resume format, extract skills with AI, get ATS scoring with keyword gap analysis, and receive laser-focused optimization suggestions.', gradient: 'from-cyan-500 to-blue-500', glow: 'rgba(34,211,238,0.15)' },
    { icon: Send, title: 'Auto-Apply Pipeline', desc: 'Scrape jobs from LinkedIn/Indeed, AI-tailor your resume for each role, auto-send applications via email, schedule follow-ups, and track interviews — all automated.', gradient: 'from-emerald-500 to-teal-500', glow: 'rgba(16,185,129,0.15)' },
    { icon: Sparkles, title: 'AI Career Architect', desc: 'Generate interview questions, get real-time ATS scores, optimize resumes for specific roles, compare profiles against job descriptions — all streaming in real-time.', gradient: 'from-amber-500 to-orange-500', glow: 'rgba(245,158,11,0.15)' },
    { icon: BarChart3, title: 'Analytics Command Center', desc: 'Visual dashboards revealing your job search velocity, win rates, interview conversion funnel, skill gap trends, and growth trajectory over time.', gradient: 'from-rose-500 to-pink-500', glow: 'rgba(244,63,94,0.15)' },
    { icon: Bell, title: 'Multi-Channel Notifications', desc: 'Telegram, Email, Slack, and In-App notifications for application status changes, interview reminders, follow-ups, and daily digests — all configurable per event.', gradient: 'from-violet-500 to-indigo-500', glow: 'rgba(139,92,246,0.15)' },
  ];

  const workflowSteps = [
    { step: '01', title: 'Discover', desc: 'Scrape jobs from LinkedIn, Indeed, and career portals', icon: SearchIcon },
    { step: '02', title: 'Optimize', desc: 'AI tailors your resume for each job description', icon: Sparkles },
    { step: '03', title: 'Apply', desc: 'Auto-send applications with customized cover letters', icon: Send },
    { step: '04', title: 'Track', desc: 'Monitor status, get interview invites, send follow-ups', icon: TrendingUp },
  ];

  return (
    <div className="min-h-screen bg-background noise-overlay overflow-x-hidden">
      {/* Skip link */}
      <a href="#main-content-landing" className="skip-link" aria-label="Skip to main content">Skip to content</a>

      {/* ===== NAVBAR ===== */}
      <nav className="fixed top-0 left-0 right-0 z-50" role="navigation" aria-label="Main navigation">
        <div className="absolute inset-0 bg-background/70 backdrop-blur-2xl border-b border-border-glow/30" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            <Link to="/" className="flex items-center gap-3 group" aria-label="Career-Ops Home">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-accent p-2 flex items-center justify-center shadow-lg shadow-primary-glow/30 group-hover:shadow-primary-glow/50 transition-all duration-300 will-change-transform">
                <Briefcase className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold text-text-heading tracking-tight">
                Career<span className="text-gradient-primary">Ops</span>
              </span>
            </Link>
            <div className="flex items-center gap-3 sm:gap-5">
              <Link to="/login" className="text-sm font-medium text-text hover:text-text-heading transition-all duration-200 px-3 py-2 rounded-lg hover:bg-primary-subtle">
                Sign In
              </Link>
              <Link to="/register" className="relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold overflow-hidden group btn-luxury shadow-lg shadow-primary-glow/20">
                <span className="relative z-10 flex items-center gap-2">
                  Get Started
                  <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main id="main-content-landing">
        {/* ===== HERO ===== */}
        <section ref={heroRef} className="relative pt-32 sm:pt-36 lg:pt-44 pb-20 sm:pb-28 px-4 overflow-hidden" aria-label="Hero section">
          <div className="absolute top-1/4 left-1/3 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-primary/5 blur-[120px] pointer-events-none will-change-transform" />
          <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] rounded-full bg-accent/5 blur-[100px] pointer-events-none will-change-transform" style={{ animationDelay: '-2s' }} />

          <motion.div style={{ y: heroY, opacity: heroOpacity }} className="max-w-7xl mx-auto text-center relative">
            <motion.div initial="hidden" animate="visible" variants={fadeUp}>
              <motion.div variants={fadeUp} custom={0} className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-light border border-primary/20 text-primary text-xs sm:text-sm font-medium mb-8 backdrop-blur-sm">
                <Zap className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">AI-Powered</span> Career Operating System
                <span className="hidden sm:inline">v2.0</span>
              </motion.div>

              <motion.h1 variants={fadeUp} custom={1} className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-bold tracking-tight mb-6 leading-[1.1] heading-balance">
                <span className="text-text-heading">Your Career,</span><br />
                <span className="text-gradient-primary">Supercharged by AI</span>
              </motion.h1>

              <motion.p variants={fadeUp} custom={2} className="text-base sm:text-lg md:text-xl text-text max-w-3xl mx-auto mb-10 leading-relaxed">
                The intelligent platform unifying job tracking, AI-powered resume optimization,
                automated applications, and real-time career analytics —{' '}
                <span className="text-text-heading font-semibold">all in one place</span>.
              </motion.p>

              <motion.div variants={fadeUp} custom={3} className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <button onClick={() => navigate('/register')}
                  className="group relative inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl bg-gradient-to-r from-primary via-primary to-accent text-white text-base font-semibold btn-luxury animate-pulse-glow"
                  aria-label="Start your free account">
                  <span className="relative z-10 flex items-center gap-2">
                    Start Your Journey
                    <ChevronRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
                  </span>
                </button>
                <button onClick={() => navigate('/login')}
                  className="group relative inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl glass-panel text-text-heading text-base font-semibold hover:bg-surface-light transition-all duration-300">
                  <span className="flex items-center gap-2">
                    Sign In
                    <ArrowRight className="w-5 h-5 opacity-0 -ml-5 group-hover:opacity-100 group-hover:ml-0 transition-all duration-300" />
                  </span>
                </button>
              </motion.div>

              <motion.div variants={fadeUp} custom={4} className="mt-12 flex flex-wrap items-center justify-center gap-6 sm:gap-10 text-xs text-text-muted">
                <span className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-success" /> 115+ Tests Passing</span>
                <span className="flex items-center gap-1.5"><Code2 className="w-4 h-4 text-primary" /> Open Source</span>
                <span className="flex items-center gap-1.5"><Shield className="w-4 h-4 text-accent" /> JWT + Argon2 Secured</span>
                <span className="flex items-center gap-1.5"><Globe className="w-4 h-4 text-amber-400" /> 5 Languages</span>
              </motion.div>
            </motion.div>
          </motion.div>
        </section>

        {/* ===== STATS ===== */}
        <section className="py-16 sm:py-20 relative" aria-label="Platform statistics">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary-subtle to-transparent opacity-30" />
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div className="glass-panel rounded-2xl p-8 sm:p-12">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 sm:gap-12">
                {[
                  { value: '98%', label: 'Tests Passing', icon: CheckCircle2 },
                  { value: '140+', label: 'API Endpoints', icon: Layers },
                  { value: '16', label: 'Docker Services', icon: Code2 },
                  { value: '100%', label: 'Free & Open', icon: Github },
                ].map((stat, i) => (
                  <motion.div key={stat.label}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-50px' }}
                    transition={{ delay: i * 0.1 }} className="text-center group">
                    <stat.icon className="w-5 h-5 text-primary/40 mx-auto mb-3 group-hover:text-primary/60 transition-colors" />
                    <div className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gradient-primary mb-1">{stat.value}</div>
                    <div className="text-sm text-text-muted tracking-wide uppercase">{stat.label}</div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ===== WORKFLOW ===== */}
        <section className="py-20 sm:py-28 px-4" aria-label="How it works">
          <div className="max-w-7xl mx-auto">
            <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} className="text-center mb-16">
              <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold tracking-wider uppercase bg-primary-light text-primary border border-primary/20 mb-4">The Pipeline</span>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-text-heading mb-4 heading-balance">
                From Job Discovery to <span className="text-gradient-primary">Offer Letter</span>
              </h2>
              <p className="text-base sm:text-lg text-text max-w-2xl mx-auto">Four steps. Fully automated. Entirely AI-powered.</p>
            </motion.div>

            <div className="relative">
              {/* Connecting line */}
              <div className="absolute top-12 left-[15%] right-[15%] h-[2px] bg-gradient-to-r from-primary/20 via-primary to-accent/20 hidden lg:block" />

              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {workflowSteps.map((ws, i) => (
                  <motion.div key={ws.step}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-50px' }}
                    transition={{ delay: i * 0.15 }}
                    className="relative text-center group">
                    <div className="w-20 h-20 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 flex items-center justify-center mx-auto mb-6 relative z-10">
                      <span className="text-2xl font-bold text-gradient-primary">{ws.step}</span>
                    </div>
                    <ws.icon className="w-6 h-6 text-primary mx-auto mb-3" />
                    <h3 className="text-lg font-semibold text-text-heading mb-2">{ws.title}</h3>
                    <p className="text-sm text-text-muted">{ws.desc}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ===== FEATURES ===== */}
        <section className="py-20 sm:py-28 px-4" aria-label="Features">
          <div className="max-w-7xl mx-auto">
            <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} className="text-center mb-16">
              <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold tracking-wider uppercase bg-primary-light text-primary border border-primary/20 mb-4">The Arsenal</span>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-text-heading mb-4 heading-balance">
                Everything You Need to <span className="text-gradient-primary">Dominate</span>
              </h2>
              <p className="text-base sm:text-lg text-text max-w-2xl mx-auto">A complete ecosystem purpose-built for career acceleration</p>
            </motion.div>

            <motion.div variants={stagger} initial="hidden" whileInView="visible" viewport={{ once: true }}
              className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
              {features.map((feature) => (
                <motion.div key={feature.title} variants={fadeUp} custom={0}
                  className="group relative p-6 sm:p-7 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden will-change-transform">
                  <div className="absolute -top-24 -right-24 w-48 h-48 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-3xl pointer-events-none"
                    style={{ background: feature.glow }} />
                  <div className="relative mb-5">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} p-3 shadow-lg will-change-transform group-hover:scale-110 transition-transform duration-300`}>
                      <feature.icon className="w-full h-full text-white" />
                    </div>
                  </div>
                  <h3 className="relative text-lg font-semibold text-text-heading mb-2.5 group-hover:text-gradient-primary transition-all duration-300">{feature.title}</h3>
                  <p className="relative text-sm text-text leading-relaxed">{feature.desc}</p>
                  <div className={`absolute bottom-0 left-6 right-6 h-[1px] bg-gradient-to-r ${feature.gradient} scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left`} />
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* ===== TESTIMONIAL ===== */}
        <section className="py-20 sm:py-28 px-4 relative" aria-label="Testimonials">
          <div className="max-w-5xl mx-auto">
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
              className="glass-panel-strong rounded-3xl p-8 sm:p-12 text-center relative overflow-hidden">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-[1px] bg-gradient-to-r from-transparent via-primary/40 to-transparent" />
              <Star className="w-10 h-10 text-gold mx-auto mb-6" />
              <blockquote className="text-lg sm:text-xl md:text-2xl text-text-heading font-medium mb-8 leading-relaxed max-w-3xl mx-auto">
                "Career-Ops transformed my job search. The AI resume optimization alone saved me weeks of manual tailoring. I landed interviews at 3 top tech companies in my first week."
              </blockquote>
              <div className="flex items-center justify-center gap-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                  <span className="text-sm font-bold text-white">KG</span>
                </div>
                <div className="text-left">
                  <p className="text-sm font-semibold text-text-heading">Kumar Gautam</p>
                  <p className="text-xs text-text-muted">Software Engineer · Career-Ops Creator</p>
                </div>
              </div>
              <div className="flex justify-center gap-1 mt-6">
                {[1, 2, 3, 4, 5].map(i => <Star key={i} className="w-4 h-4 text-gold fill-gold" />)}
              </div>
            </motion.div>
          </div>
        </section>

        {/* ===== CTA ===== */}
        <section className="py-20 sm:py-28 px-4 relative overflow-hidden" aria-label="Call to action">
          <div className="absolute inset-0 bg-gradient-to-b from-background via-primary-subtle to-background" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-primary/5 blur-[120px] pointer-events-none" />

          <div className="max-w-4xl mx-auto text-center relative">
            <motion.div initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} transition={{ duration: 0.6 }}>
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-primary-glow/30">
                <Brain className="w-10 h-10 text-white" />
              </div>

              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-text-heading mb-4 leading-tight heading-balance">
                Ready to <span className="text-gradient-primary">Transform</span> Your Career?
              </h2>
              <p className="text-base sm:text-lg text-text mb-10 max-w-2xl mx-auto">
                Join professionals using Career-Ops to accelerate their career growth with AI-powered tools and battle-tested strategies.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <button onClick={() => navigate('/register')}
                  className="group relative inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-base font-semibold btn-luxury shadow-lg shadow-primary-glow/20">
                  <span className="relative z-10 flex items-center gap-2">
                    Get Started Free
                    <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
                  </span>
                </button>
                <a href="https://github.com/kmrgautam18-alt/career-ops-v2" target="_blank" rel="noopener noreferrer"
                  className="group inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl glass-panel text-text-heading text-base font-semibold hover:bg-surface-lighter transition-all duration-300">
                  <Github className="w-5 h-5" />
                  View on GitHub
                  <ExternalLink className="w-4 h-4 opacity-0 -ml-4 group-hover:opacity-100 group-hover:ml-0 transition-all duration-300" />
                </a>
              </div>

              <div className="mt-16 pt-8 border-t border-border/40">
                <p className="text-xs text-text-muted uppercase tracking-widest mb-4">Built with modern tech</p>
                <div className="flex items-center justify-center gap-6 text-text-muted/40 flex-wrap">
                  <span className="flex items-center gap-1.5 text-xs"><Zap className="w-4 h-4" /> FastAPI</span>
                  <span className="flex items-center gap-1.5 text-xs"><Code2 className="w-4 h-4" /> React 19</span>
                  <span className="flex items-center gap-1.5 text-xs"><Layers className="w-4 h-4" /> PostgreSQL</span>
                  <span className="flex items-center gap-1.5 text-xs"><Globe className="w-4 h-4" /> Docker</span>
                  <span className="flex items-center gap-1.5 text-xs"><MessageSquare className="w-4 h-4" /> Gemini AI</span>
                </div>
              </div>
            </motion.div>
          </div>
        </section>
      </main>

      {/* ===== FOOTER ===== */}
      <footer className="py-10 border-t border-border/40 relative" role="contentinfo">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-sm">
                <Briefcase className="w-4 h-4 text-white" />
              </div>
              <div>
                <span className="text-sm font-semibold text-text-heading">Career-Ops</span>
                <span className="text-xs text-text-muted ml-2">v2.0</span>
              </div>
            </div>
            <div className="flex items-center gap-5 text-xs sm:text-sm text-text-muted">
              <span className="hidden sm:inline">Built with</span>
              <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-subtle text-primary text-xs font-medium">
                <Zap className="w-3 h-3" /> FastAPI + React
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-success" />
                <span>Open Source</span>
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Inline icon components for workflow steps
function SearchIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" strokeLinecap="round" />
    </svg>
  );
}
