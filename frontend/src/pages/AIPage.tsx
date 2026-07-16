import { useState, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  Sparkles, Target, MessageSquare, Loader2, AlertCircle,
  Brain, Zap, ChevronRight, FileText, Scale,
  Wifi, WifiOff,
} from 'lucide-react';
import type { StreamCallbacks } from '../api/client';
import { aiApi, aiStreamApi } from '../api/client';

type Tool = 'ats' | 'interview' | 'optimize' | 'jobmatch';

function useToolState() {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const aborter = useRef<AbortController | null>(null);

  const stop = useCallback(() => {
    aborter.current?.abort();
    setLoading(false);
  }, []);

  const callbacks = useRef<StreamCallbacks>({
    onToken: () => {},
    onDone: () => {},
    onError: () => {},
  });

  callbacks.current.onToken = (text: string) => {
    setContent((prev) => prev + text);
  };
  callbacks.current.onDone = () => {
    setLoading(false);
  };
  callbacks.current.onError = (err: string) => {
    console.error('Stream error:', err);
    setLoading(false);
  };

  const startStream = useCallback(async (
    data: Record<string, unknown>,
    streamFn: (d: Record<string, unknown>, c: StreamCallbacks) => Promise<AbortController>,
  ) => {
    setLoading(true);
    setContent('');
    aborter.current?.abort();
    aborter.current = await streamFn(data, {
      onToken: (text: string) => setContent((prev) => prev + text),
      onDone: () => setLoading(false),
      onError: (err: string) => { console.error(err); setLoading(false); },
    });
  }, []);

  const startNonStream = useCallback(async (
    nonStreamFn: () => Promise<{ data: { data: Record<string, unknown> } }>,
  ) => {
    setLoading(true);
    setContent('');
    try {
      const res = await nonStreamFn();
      setContent(JSON.stringify(res.data.data, null, 2));
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { message?: string } } })?.response?.data?.message || 'Request failed';
      setContent(`Error: ${msg}`);
    }
    setLoading(false);
  }, []);

  return { content, loading, setContent, setLoading, startStream, startNonStream, stop };
}

export function AIPage() {
  const [activeTool, setActiveTool] = useState<Tool>('ats');
  const [useStream, setUseStream] = useState(true);
  const [error, setError] = useState('');

  // ATS
  const [atsForm, setAtsForm] = useState({ resume_text: '', job_description: '' });
  const ats = useToolState();

  // Interview
  const [interviewForm, setInterviewForm] = useState({ job_title: '', company: '', difficulty: 'medium' });
  const interview = useToolState();

  // Optimize
  const [optimizeForm, setOptimizeForm] = useState({ resume_text: '', job_description: '' });
  const optimize = useToolState();

  // Job Match
  const [matchForm, setMatchForm] = useState({ profile: '', job_details: '' });
  const match = useToolState();

  const handleAts = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (useStream) {
      ats.startStream(atsForm, (d, c) => aiStreamApi.atsScore(d as typeof atsForm, c));
    } else {
      ats.startNonStream(() => aiApi.atsScore(atsForm));
    }
  };

  const handleInterview = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (useStream) {
      interview.startStream(interviewForm, (d, c) => aiStreamApi.interviewQuestions(d as typeof interviewForm, c));
    } else {
      interview.startNonStream(() => aiApi.interviewQuestions(interviewForm));
    }
  };

  const handleOptimize = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (useStream) {
      optimize.startStream(optimizeForm, (d, c) => aiStreamApi.resumeOptimize(d as typeof optimizeForm, c));
    } else {
      optimize.startNonStream(() => aiApi.resumeOptimize(optimizeForm));
    }
  };

  const handleJobMatch = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (useStream) {
      match.startStream(matchForm, (d, c) => aiStreamApi.jobMatch(d as typeof matchForm, c));
    } else {
      match.startNonStream(() => aiApi.jobMatch(matchForm));
    }
  };

  const tools = [
    { id: 'ats' as Tool, label: 'ATS Score', icon: Target, desc: 'Evaluate resume against a job description', gradient: 'from-indigo-500 to-purple-500' },
    { id: 'interview' as Tool, label: 'Interview Qs', icon: MessageSquare, desc: 'Generate tailored practice questions', gradient: 'from-cyan-500 to-blue-500' },
    { id: 'optimize' as Tool, label: 'Resume Optimizer', icon: FileText, desc: 'Improve your resume for any role', gradient: 'from-emerald-500 to-teal-500' },
    { id: 'jobmatch' as Tool, label: 'Job Match', icon: Scale, desc: 'AI profile vs job comparison', gradient: 'from-amber-500 to-orange-500' },
  ];

  const current = activeTool === 'ats' ? ats
    : activeTool === 'interview' ? interview
    : activeTool === 'optimize' ? optimize
    : match;

  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-heading flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 p-2.5 shadow-lg">
              <Sparkles className="w-full h-full text-white" />
            </div>
            AI Tools
          </h1>
          <p className="text-text-muted mt-1">Leverage artificial intelligence to accelerate your career</p>
        </div>
        <button
          onClick={() => setUseStream(!useStream)}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
            useStream
              ? 'bg-primary-light text-primary border border-primary/20'
              : 'bg-surface text-text-muted border border-border/40'
          }`}
        >
          {useStream ? <Wifi className="w-3.5 h-3.5" /> : <WifiOff className="w-3.5 h-3.5" />}
          {useStream ? 'Streaming' : 'Batch'}
        </button>
      </motion.div>

      {/* Tool tabs */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className="flex gap-2 p-1.5 rounded-2xl bg-surface border border-border/40 w-fit flex-wrap"
      >
        {tools.map((tool) => (
          <button
            key={tool.id}
            onClick={() => setActiveTool(tool.id)}
            className={`relative flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 ${
              activeTool === tool.id
                ? 'bg-gradient-to-r from-primary to-accent text-white shadow-lg shadow-primary-glow/20'
                : 'text-text-muted hover:text-text-heading'
            }`}
          >
            {activeTool === tool.id && (
              <motion.div
                layoutId="activeToolBg"
                className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary to-accent"
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              />
            )}
            <span className="relative z-10 flex items-center gap-1.5">
              <tool.icon className="w-4 h-4" />
              {tool.label}
            </span>
          </button>
        ))}
      </motion.div>

      {/* Error */}
      {error && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="flex items-center gap-2.5 p-3.5 rounded-xl bg-danger-light border border-danger/20 text-sm text-danger"
        >
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {error}
        </motion.div>
      )}

      {/* ===== ATS Score ===== */}
      {activeTool === 'ats' && (
        <motion.div key="ats" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid lg:grid-cols-2 gap-5">
          <FormPanel
            icon={Target} gradient="from-indigo-500 to-purple-500" title="Resume & Job Description"
            loading={ats.loading} onStop={ats.stop} onSubmit={handleAts} submitLabel="Analyze ATS Score"
          >
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Resume Text</label>
              <textarea value={atsForm.resume_text} onChange={(e) => setAtsForm({ ...atsForm, resume_text: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[120px] resize-y"
                placeholder="Paste your resume text here..." required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Job Description</label>
              <textarea value={atsForm.job_description} onChange={(e) => setAtsForm({ ...atsForm, job_description: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[120px] resize-y"
                placeholder="Paste the job description here..." required
              />
            </div>
          </FormPanel>
          <ResultPanel icon={Brain} gradient="from-emerald-500 to-teal-500" title="ATS Analysis Result"
            content={current.content} loading={current.loading}
          />
        </motion.div>
      )}

      {/* ===== Interview Questions ===== */}
      {activeTool === 'interview' && (
        <motion.div key="interview" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid lg:grid-cols-2 gap-5">
          <FormPanel
            icon={MessageSquare} gradient="from-cyan-500 to-blue-500" title="Generate Questions"
            loading={interview.loading} onStop={interview.stop} onSubmit={handleInterview} submitLabel="Generate Questions"
          >
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Job Title</label>
              <input type="text" value={interviewForm.job_title} onChange={(e) => setInterviewForm({ ...interviewForm, job_title: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                placeholder="e.g., Software Engineer" required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Company</label>
              <input type="text" value={interviewForm.company} onChange={(e) => setInterviewForm({ ...interviewForm, company: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                placeholder="e.g., Google" required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Difficulty</label>
              <select value={interviewForm.difficulty} onChange={(e) => setInterviewForm({ ...interviewForm, difficulty: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
                <option value="all">All Levels</option>
              </select>
            </div>
          </FormPanel>
          <ResultPanel icon={Brain} gradient="from-amber-500 to-orange-500" title="Generated Questions"
            content={current.content} loading={current.loading}
          />
        </motion.div>
      )}

      {/* ===== Resume Optimize ===== */}
      {activeTool === 'optimize' && (
        <motion.div key="optimize" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid lg:grid-cols-2 gap-5">
          <FormPanel
            icon={FileText} gradient="from-emerald-500 to-teal-500" title="Resume & Target Role"
            loading={optimize.loading} onStop={optimize.stop} onSubmit={handleOptimize} submitLabel="Optimize Resume"
          >
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Resume Text</label>
              <textarea value={optimizeForm.resume_text} onChange={(e) => setOptimizeForm({ ...optimizeForm, resume_text: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[120px] resize-y"
                placeholder="Paste your resume text here..." required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Job Description</label>
              <textarea value={optimizeForm.job_description} onChange={(e) => setOptimizeForm({ ...optimizeForm, job_description: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[120px] resize-y"
                placeholder="Paste the target job description..." required
              />
            </div>
          </FormPanel>
          <ResultPanel icon={Zap} gradient="from-purple-500 to-pink-500" title="Optimization Suggestions"
            content={current.content} loading={current.loading}
          />
        </motion.div>
      )}

      {/* ===== Job Match ===== */}
      {activeTool === 'jobmatch' && (
        <motion.div key="jobmatch" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid lg:grid-cols-2 gap-5">
          <FormPanel
            icon={Scale} gradient="from-amber-500 to-orange-500" title="Profile vs Job"
            loading={match.loading} onStop={match.stop} onSubmit={handleJobMatch} submitLabel="Analyze Match"
          >
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Your Profile</label>
              <textarea value={matchForm.profile} onChange={(e) => setMatchForm({ ...matchForm, profile: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[120px] resize-y"
                placeholder="Paste your resume or profile information..." required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Job Details</label>
              <textarea value={matchForm.job_details} onChange={(e) => setMatchForm({ ...matchForm, job_details: e.target.value })}
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[120px] resize-y"
                placeholder="Paste the job posting details..." required
              />
            </div>
          </FormPanel>
          <ResultPanel icon={Scale} gradient="from-green-500 to-teal-500" title="Match Analysis"
            content={current.content} loading={current.loading}
          />
        </motion.div>
      )}
    </div>
  );
}

// ===== Reusable Sub-components =====

function FormPanel({
  icon: Icon, gradient, title, children,
  loading, onStop, onSubmit, submitLabel,
}: {
  icon: typeof Target; gradient: string; title: string;
  children: React.ReactNode;
  loading: boolean; onStop: () => void; onSubmit: (e: React.FormEvent) => void;
  submitLabel: string;
}) {
  return (
    <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
      <div className="flex items-center gap-2.5 mb-5">
        <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${gradient} p-2`}>
          <Icon className="w-full h-full text-white" />
        </div>
        <h2 className="text-lg font-semibold text-text-heading">{title}</h2>
      </div>
      <form onSubmit={onSubmit} className="space-y-4">
        {children}
        <div className="flex gap-3 pt-1">
          {loading ? (
            <button
              type="button"
              onClick={onStop}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-danger text-white text-sm font-semibold hover:bg-danger/90 transition-all"
            >
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Stop</span>
            </button>
          ) : (
            <button
              type="submit"
              className="group relative flex-1 flex items-center justify-center gap-2.5 px-4 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
            >
              <Zap className="w-4 h-4" />
              <span>{submitLabel}</span>
              <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

function ResultPanel({
  icon: Icon, gradient, title, content, loading,
}: {
  icon: typeof Brain; gradient: string; title: string; content: string; loading: boolean;
}) {
  return (
    <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
      <div className="flex items-center gap-2.5 mb-5">
        <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${gradient} p-2`}>
          <Icon className="w-full h-full text-white" />
        </div>
        <h2 className="text-lg font-semibold text-text-heading">{title}</h2>
        {loading && (
          <span className="ml-auto flex items-center gap-1.5 text-xs text-primary">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary" />
            </span>
            Streaming
          </span>
        )}
      </div>
      <div className="min-h-[360px] max-h-[600px] overflow-y-auto">
        {content ? (
          <pre className="text-sm text-text-heading whitespace-pre-wrap font-sans leading-relaxed">{content}</pre>
        ) : loading ? (
          <div className="flex flex-col items-center justify-center h-[360px] text-text-muted">
            <div className="relative mb-4">
              <Loader2 className="w-10 h-10 text-primary animate-spin" />
              <div className="absolute inset-0 rounded-full bg-primary/5 blur-xl" />
            </div>
            <p className="text-sm animate-pulse">Waiting for AI response...</p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-[360px] text-text-muted">
            <Icon className="w-16 h-16 mb-4 opacity-20" />
            <p className="text-sm">Fill in the details and submit</p>
            <p className="text-xs mt-1">to see AI-powered results here</p>
          </div>
        )}
      </div>
    </div>
  );
}
