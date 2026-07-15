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
} from 'lucide-react';

const features = [
  {
    icon: Briefcase,
    title: 'Job Management',
    description: 'Track and manage job opportunities with powerful search, filtering, and organization tools.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: FileText,
    title: 'Resume Intelligence',
    description: 'Upload resumes and get AI-powered analysis, ATS scoring, and optimization suggestions.',
    color: 'from-purple-500 to-pink-500',
  },
  {
    icon: Send,
    title: 'Application Tracking',
    description: 'Monitor every stage of your job applications from submission to interview to offer.',
    color: 'from-emerald-500 to-teal-500',
  },
  {
    icon: Sparkles,
    title: 'AI Career Assistant',
    description: 'Get AI-powered interview questions, resume optimization, and career insights tailored to you.',
    color: 'from-orange-500 to-red-500',
  },
  {
    icon: BarChart3,
    title: 'Career Analytics',
    description: 'Visualize your job search progress with insightful dashboards and performance metrics.',
    color: 'from-indigo-500 to-violet-500',
  },
  {
    icon: Shield,
    title: 'Secure & Private',
    description: 'Your career data is encrypted and secure. Role-based access control keeps your information safe.',
    color: 'from-rose-500 to-pink-500',
  },
];

const stats = [
  { value: '98%', label: 'Tests Passing' },
  { value: '20+', label: 'API Endpoints' },
  { value: '8', label: 'Core Modules' },
  { value: '100%', label: 'Open Source' },
];

export function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                <Briefcase className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold text-text-heading">Career-Ops</span>
            </div>
            <div className="flex items-center gap-4">
              <Link
                to="/login"
                className="text-sm font-medium text-text hover:text-text-heading transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-hover transition-all duration-200"
              >
                Get Started
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-accent/5 to-transparent pointer-events-none" />
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-accent/10 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-7xl mx-auto text-center relative">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-light border border-primary/20 text-primary text-sm font-medium mb-8">
              <Zap className="w-4 h-4" />
              AI-Powered Career Operating System
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-text-heading tracking-tight mb-6">
              Your Career,
              <br />
              <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Supercharged by AI
              </span>
            </h1>

            <p className="text-lg sm:text-xl text-text max-w-2xl mx-auto mb-10 leading-relaxed">
              The intelligent platform that unifies job tracking, resume optimization,
              application management, and AI-powered career guidance — all in one place.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button
                onClick={() => navigate('/register')}
                className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-primary text-white text-base font-semibold hover:bg-primary-hover transition-all duration-200 animate-glow"
              >
                Start Your Journey
                <ArrowRight className="w-5 h-5" />
              </button>
              <button
                onClick={() => navigate('/login')}
                className="inline-flex items-center gap-2 px-8 py-3 rounded-xl border border-border text-text-heading text-base font-semibold hover:bg-surface-light transition-all duration-200"
              >
                Sign In
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 border-y border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="text-center"
              >
                <div className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                  {stat.value}
                </div>
                <div className="text-sm text-text mt-2">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl sm:text-4xl font-bold text-text-heading mb-4">
              Everything You Need
            </h2>
            <p className="text-lg text-text max-w-2xl mx-auto">
              A complete ecosystem for managing your professional journey
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="group relative p-6 rounded-xl border border-border bg-surface hover:bg-surface-light transition-all duration-300"
              >
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${feature.color} p-2.5 mb-4`}>
                  <feature.icon className="w-full h-full text-white" />
                </div>
                <h3 className="text-lg font-semibold text-text-heading mb-2">{feature.title}</h3>
                <p className="text-sm text-text leading-relaxed">{feature.description}</p>
                <div className="absolute inset-0 rounded-xl border border-primary/0 group-hover:border-primary/20 transition-all duration-300 pointer-events-none" />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-accent/10" />
        <div className="max-w-4xl mx-auto text-center relative">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
          >
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center mx-auto mb-6">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold text-text-heading mb-4">
              Ready to Transform Your Career?
            </h2>
            <p className="text-lg text-text mb-8 max-w-2xl mx-auto">
              Join Career-Ops and take control of your professional journey with AI-powered tools
              that help you land your dream job faster.
            </p>
            <button
              onClick={() => navigate('/register')}
              className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-primary text-white text-base font-semibold hover:bg-primary-hover transition-all duration-200"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5" />
            </button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                <Briefcase className="w-3 h-3 text-white" />
              </div>
              <span className="text-sm font-semibold text-text-heading">Career-Ops v2</span>
            </div>
            <div className="flex items-center gap-6 text-sm text-text">
              <span>Built with FastAPI + React</span>
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3 text-success" />
                Open Source
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
