import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Briefcase,
  FileText,
  Send,
  Sparkles,
  BarChart3,
  ArrowRight,
  Shield,
  Zap,
  Brain,
  CheckCircle2,
  ChevronRight,
  Star,
  Gem,
  Layers,
  Target,
  TrendingUp,
  Users,
  Award,
} from 'lucide-react';

const features = [
  {
    icon: Briefcase,
    title: 'Job Intelligence',
    description: 'Track opportunities with AI-powered search, smart filtering, and real-time market insights.',
    gradient: 'from-indigo-500 to-purple-500',
    glow: 'rgba(99,102,241,0.15)',
  },
  {
    icon: FileText,
    title: 'Resume Alchemy',
    description: 'Upload, analyze, and optimize resumes with ATS scoring and laser-focused recommendations.',
    gradient: 'from-cyan-500 to-blue-500',
    glow: 'rgba(34,211,238,0.15)',
  },
  {
    icon: Send,
    title: 'Application Nexus',
    description: 'Command-center for every application — from first submit to final offer, in one place.',
    gradient: 'from-emerald-500 to-teal-500',
    glow: 'rgba(16,185,129,0.15)',
  },
  {
    icon: Sparkles,
    title: 'AI Career Architect',
    description: 'Generate interview questions, optimize resumes, and unlock insights tailored to your path.',
    gradient: 'from-amber-500 to-orange-500',
    glow: 'rgba(245,158,11,0.15)',
  },
  {
    icon: BarChart3,
    title: 'Analytics Vault',
    description: 'Visual dashboards that reveal your job search velocity, win rates, and growth trajectory.',
    gradient: 'from-rose-500 to-pink-500',
    glow: 'rgba(244,63,94,0.15)',
  },
  {
    icon: Shield,
    title: 'Fortress Security',
    description: 'Enterprise-grade encryption, RBAC, and JWT authentication protecting your career data.',
    gradient: 'from-violet-500 to-indigo-500',
    glow: 'rgba(139,92,246,0.15)',
  },
];

const stats = [
  { value: '98%', label: 'Tests Passing', icon: CheckCircle2 },
  { value: '134', label: 'API Endpoints', icon: Layers },
  { value: '8', label: 'Core Engines', icon: Gem },
  { value: '100%', label: 'Open Source', icon: Users },
];

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const staggerItem = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background noise-overlay">
      {/* ===== NAVBAR ===== */}
      <nav className="fixed top-0 left-0 right-0 z-50">
        <div className="absolute inset-0 bg-background/70 backdrop-blur-2xl border-b border-border-glow/30" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            <Link to="/" className="flex items-center gap-3 group">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-accent p-2 flex items-center justify-center shadow-lg shadow-primary-glow/30 group-hover:shadow-primary-glow/50 transition-all duration-300">
                <Briefcase className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold text-text-heading tracking-tight">
                Career<span className="text-gradient-primary">Ops</span>
              </span>
            </Link>
            <div className="flex items-center gap-3 sm:gap-5">
              <Link
                to="/login"
                className="text-sm font-medium text-text hover:text-text-heading transition-all duration-200 px-3 py-2 rounded-lg hover:bg-primary-subtle"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="relative inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold overflow-hidden group btn-luxury shadow-lg shadow-primary-glow/20"
              >
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

      {/* ===== HERO SECTION ===== */}
      <section className="relative pt-32 sm:pt-36 lg:pt-44 pb-20 sm:pb-28 px-4 overflow-hidden">
        {/* Ambient Glow Orbs */}
        <div className="absolute top-1/4 left-1/3 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-primary/5 blur-[120px] pointer-events-none animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] rounded-full bg-accent/5 blur-[100px] pointer-events-none animate-float" style={{ animationDelay: '-2s' }} />
        <div className="absolute top-1/2 left-2/3 w-[400px] h-[400px] rounded-full bg-indigo-500/3 blur-[80px] pointer-events-none" />

        <div className="max-w-7xl mx-auto text-center relative">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            {/* Premium Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-light border border-primary/20 text-primary text-xs sm:text-sm font-medium mb-8 backdrop-blur-sm"
            >
              <Zap className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">AI-Powered</span> Career Operating System
              <span className="hidden sm:inline">v2.0</span>
            </motion.div>

            {/* Main Heading */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-bold tracking-tight mb-6 leading-[1.1]"
            >
              <span className="text-text-heading">Your Career,</span>
              <br />
              <span className="text-gradient-primary">
                Forged in Code
              </span>
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-base sm:text-lg md:text-xl text-text max-w-2xl mx-auto mb-10 leading-relaxed"
            >
              The intelligent platform unifying job tracking, resume optimization,
              application management, and AI-powered career guidance —{' '}
              <span className="text-text-heading font-medium">all in one place</span>.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <button
                onClick={() => navigate('/register')}
                className="group relative inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl bg-gradient-to-r from-primary via-primary to-accent text-white text-base font-semibold btn-luxury animate-pulse-glow"
              >
                <span className="relative z-10 flex items-center gap-2">
                  Start Your Journey
                  <ChevronRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
                </span>
              </button>
              <button
                onClick={() => navigate('/login')}
                className="group relative inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl glass-panel text-text-heading text-base font-semibold hover:bg-surface-light transition-all duration-300"
              >
                <span className="flex items-center gap-2">
                  Sign In
                  <ArrowRight className="w-5 h-5 opacity-0 -ml-5 group-hover:opacity-100 group-hover:ml-0 transition-all duration-300" />
                </span>
              </button>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* ===== STATS SECTION ===== */}
      <section className="py-16 sm:py-20 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary-subtle to-transparent opacity-30" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="glass-panel rounded-2xl p-8 sm:p-12">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 sm:gap-12">
              {stats.map((stat, i) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="text-center group"
                >
                  <stat.icon className="w-5 h-5 text-primary/40 mx-auto mb-3 group-hover:text-primary/60 transition-colors" />
                  <div className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gradient-primary mb-1">
                    {stat.value}
                  </div>
                  <div className="text-sm text-text-muted tracking-wide uppercase">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ===== FEATURES SECTION ===== */}
      <section className="py-20 sm:py-28 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold tracking-wider uppercase bg-primary-light text-primary border border-primary/20 mb-4">
              The Arsenal
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-text-heading mb-4">
              Everything You Need to{' '}
              <span className="text-gradient-primary">Dominate</span>
            </h2>
            <p className="text-base sm:text-lg text-text max-w-2xl mx-auto">
              A complete ecosystem purpose-built for career acceleration
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6"
          >
            {features.map((feature) => (
              <motion.div
                key={feature.title}
                variants={staggerItem}
                className="group relative p-6 sm:p-7 rounded-2xl bg-surface border border-border/60 hover:border-border-glow/40 transition-all duration-500 overflow-hidden"
              >
                {/* Hover Glow */}
                <div
                  className="absolute -top-24 -right-24 w-48 h-48 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-3xl pointer-events-none"
                  style={{ background: feature.glow }}
                />

                {/* Icon Container */}
                <div className="relative mb-5">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} p-3 shadow-lg`}>
                    <feature.icon className="w-full h-full text-white" />
                  </div>
                </div>

                <h3 className="relative text-lg font-semibold text-text-heading mb-2.5 group-hover:text-gradient-primary transition-all duration-300">
                  {feature.title}
                </h3>
                <p className="relative text-sm text-text leading-relaxed">
                  {feature.description}
                </p>

                {/* Bottom Accent Line */}
                <div className={`absolute bottom-0 left-6 right-6 h-[1px] bg-gradient-to-r ${feature.gradient} scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left`} />

                {/* Corner decoration */}
                <div className="absolute top-0 right-0 w-16 h-16 overflow-hidden opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                  <div className={`absolute -top-4 -right-4 w-8 h-8 rotate-45 bg-gradient-to-br ${feature.gradient} opacity-20`} />
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ===== CTA SECTION ===== */}
      <section className="py-20 sm:py-28 px-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-primary-subtle to-background" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-primary/5 blur-[120px] pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center relative">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            {/* Icon */}
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-primary-glow/30">
              <Brain className="w-10 h-10 text-white" />
            </div>

            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-text-heading mb-4 leading-tight">
              Ready to{' '}
              <span className="text-gradient-primary">Transform</span>{' '}
              Your Career?
            </h2>
            <p className="text-base sm:text-lg text-text mb-10 max-w-2xl mx-auto">
              Join thousands of professionals using Career-Ops to accelerate their career growth
              with AI-powered tools and battle-tested strategies.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button
                onClick={() => navigate('/register')}
                className="group relative inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-base font-semibold btn-luxury shadow-lg shadow-primary-glow/20"
              >
                <span className="relative z-10 flex items-center gap-2">
                  Get Started Free
                  <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
                </span>
              </button>
              <button
                onClick={() => {
                  document.querySelector('.features-section')?.scrollIntoView({ behavior: 'smooth' });
                }}
                className="group inline-flex items-center gap-2.5 px-8 py-3.5 rounded-xl glass-panel text-text-heading text-base font-semibold hover:bg-surface-lighter transition-all duration-300"
              >
                <Star className="w-4 h-4 text-gold" />
                View Features
              </button>
            </div>

            {/* Trusted By */}
            <div className="mt-16 pt-8 border-t border-border/40">
              <p className="text-xs text-text-muted uppercase tracking-widest mb-4">
                Trusted by career-driven professionals
              </p>
              <div className="flex items-center justify-center gap-6 text-text-muted/40">
                <Award className="w-8 h-8" />
                <Target className="w-8 h-8" />
                <TrendingUp className="w-8 h-8" />
                <Users className="w-8 h-8" />
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className="py-10 border-t border-border/40 relative">
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
                <Zap className="w-3 h-3" />
                FastAPI + React
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
