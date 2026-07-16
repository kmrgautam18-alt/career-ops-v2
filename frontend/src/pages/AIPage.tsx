import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Sparkles, Target, MessageSquare, Loader2, AlertCircle,
  CheckCircle2, Brain, Zap, ChevronRight,
} from 'lucide-react';
import { aiApi } from '../api/client';

type Tool = 'ats' | 'interview';

export function AIPage() {
  const [activeTool, setActiveTool] = useState<Tool>('ats');

  const [atsForm, setAtsForm] = useState({ resume_text: '', job_description: '' });
  const [atsResult, setAtsResult] = useState<Record<string, unknown> | null>(null);
  const [atsLoading, setAtsLoading] = useState(false);

  const [interviewForm, setInterviewForm] = useState({ job_title: '', company: '', difficulty: 'medium' });
  const [interviewResult, setInterviewResult] = useState<string[] | null>(null);
  const [interviewLoading, setInterviewLoading] = useState(false);

  const [error, setError] = useState('');

  const handleAtsScore = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setAtsLoading(true);
    setAtsResult(null);
    try {
      const res = await aiApi.atsScore(atsForm);
      setAtsResult(res.data.data || null);
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { message?: string } } })?.response?.data?.message || 'Failed to calculate ATS score';
      setError(msg);
    } finally {
      setAtsLoading(false);
    }
  };

  const handleInterviewQuestions = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setInterviewLoading(true);
    setInterviewResult(null);
    try {
      const res = await aiApi.interviewQuestions(interviewForm);
      const questions = res.data.data?.questions || res.data.data || [];
      const qs: string[] = Array.isArray(questions) ? questions.map((q: unknown) => String(q)) : [String(questions)];
      setInterviewResult(qs);
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { message?: string } } })?.response?.data?.message || 'Failed to generate questions';
      setError(msg);
    } finally {
      setInterviewLoading(false);
    }
  };

  const renderScore = (): string => {
    if (!atsResult) return 'N/A';
    const score = atsResult.score ?? atsResult.overall_score;
    if (typeof score === 'number') return `${score}%`;
    return 'N/A';
  };

  const renderRecommendations = (): string[] => {
    if (atsResult?.recommendations && Array.isArray(atsResult.recommendations)) {
      return atsResult.recommendations.map((r: unknown) => String(r));
    }
    return [];
  };

  const renderStrengths = (): string[] => {
    if (atsResult?.strengths && Array.isArray(atsResult.strengths)) {
      return atsResult.strengths.map((s: unknown) => String(s));
    }
    return [];
  };

  const tools = [
    {
      id: 'ats' as Tool,
      label: 'ATS Score Analyzer',
      icon: Target,
      desc: 'Evaluate your resume against any job description',
      gradient: 'from-indigo-500 to-purple-500',
    },
    {
      id: 'interview' as Tool,
      label: 'Interview Questions',
      icon: MessageSquare,
      desc: 'Generate tailored practice questions',
      gradient: 'from-cyan-500 to-blue-500',
    },
  ];

  return (
    <div className="space-y-7 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-2xl sm:text-3xl font-bold text-text-heading flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 p-2.5 shadow-lg">
            <Sparkles className="w-full h-full text-white" />
          </div>
          AI Tools
        </h1>
        <p className="text-text-muted mt-1">Leverage artificial intelligence to accelerate your career</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className="flex gap-3 p-1.5 rounded-2xl bg-surface border border-border/40 w-fit"
      >
        {tools.map((tool) => (
          <button
            key={tool.id}
            onClick={() => setActiveTool(tool.id)}
            className={`relative flex items-center gap-2.5 px-5 py-3 rounded-xl text-sm font-medium transition-all duration-300 ${
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
            <span className="relative z-10 flex items-center gap-2">
              <tool.icon className="w-4 h-4" />
              {tool.label}
            </span>
          </button>
        ))}
      </motion.div>

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

      {activeTool === 'ats' && (
        <motion.div
          key="ats"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="grid lg:grid-cols-2 gap-5"
        >
          <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
            <div className="flex items-center gap-2.5 mb-5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 p-2">
                <Target className="w-full h-full text-white" />
              </div>
              <h2 className="text-lg font-semibold text-text-heading">Resume & Job Description</h2>
            </div>
            <form onSubmit={handleAtsScore} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1.5">Resume Text</label>
                <textarea
                  value={atsForm.resume_text}
                  onChange={(e) => setAtsForm({ ...atsForm, resume_text: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[140px] resize-y"
                  placeholder="Paste your resume text here..."
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1.5">Job Description</label>
                <textarea
                  value={atsForm.job_description}
                  onChange={(e) => setAtsForm({ ...atsForm, job_description: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all min-h-[140px] resize-y"
                  placeholder="Paste the job description here..."
                  required
                />
              </div>
              <button
                type="submit"
                disabled={atsLoading}
                className="group relative w-full flex items-center justify-center gap-2.5 px-4 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold disabled:opacity-50 btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
              >
                {atsLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    <span>Calculate ATS Score</span>
                    <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
                  </>
                )}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
              </button>
            </form>
          </div>

          <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
            <div className="flex items-center gap-2.5 mb-5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-500 p-2">
                <Brain className="w-full h-full text-white" />
              </div>
              <h2 className="text-lg font-semibold text-text-heading">Analysis Results</h2>
            </div>
            {atsResult ? (
              <div className="space-y-5">
                <div className="text-center py-4">
                  <div className="text-6xl sm:text-7xl font-bold text-gradient-primary mb-2">
                    {renderScore()}
                  </div>
                  <p className="text-text-muted text-sm">ATS Compatibility Score</p>
                </div>
                <div className="space-y-4">
                  {renderRecommendations().length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-text-heading mb-3 flex items-center gap-2">
                        <Zap className="w-4 h-4 text-amber-400" />
                        Recommendations
                      </h3>
                      <ul className="space-y-2">
                        {renderRecommendations().map((rec, i) => (
                          <li key={i} className="flex items-start gap-2.5 text-sm text-text p-2.5 rounded-xl bg-surface-light/30">
                            <CheckCircle2 className="w-4 h-4 text-success mt-0.5 flex-shrink-0" />
                            <span>{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {renderStrengths().length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-text-heading mb-3 flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-primary" />
                        Strengths
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {renderStrengths().map((s, i) => (
                          <span key={i} className="px-3 py-1.5 rounded-lg bg-success-light text-success text-xs font-medium border border-success/20">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-[380px] text-text-muted">
                <Target className="w-16 h-16 mb-4 opacity-20" />
                <p className="text-sm">Submit your resume and job description</p>
                <p className="text-xs mt-1">to see the ATS analysis results</p>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {activeTool === 'interview' && (
        <motion.div
          key="interview"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="grid lg:grid-cols-2 gap-5"
        >
          <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
            <div className="flex items-center gap-2.5 mb-5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 p-2">
                <MessageSquare className="w-full h-full text-white" />
              </div>
              <h2 className="text-lg font-semibold text-text-heading">Generate Questions</h2>
            </div>
            <form onSubmit={handleInterviewQuestions} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1.5">Job Title</label>
                <input
                  type="text"
                  value={interviewForm.job_title}
                  onChange={(e) => setInterviewForm({ ...interviewForm, job_title: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                  placeholder="e.g., Software Engineer"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1.5">Company</label>
                <input
                  type="text"
                  value={interviewForm.company}
                  onChange={(e) => setInterviewForm({ ...interviewForm, company: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                  placeholder="e.g., Google"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1.5">Difficulty</label>
                <select
                  value={interviewForm.difficulty}
                  onChange={(e) => setInterviewForm({ ...interviewForm, difficulty: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all"
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                  <option value="All">All Levels</option>
                </select>
              </div>
              <button
                type="submit"
                disabled={interviewLoading}
                className="group relative w-full flex items-center justify-center gap-2.5 px-4 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-semibold disabled:opacity-50 btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden"
              >
                {interviewLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>Generate Questions</span>
                    <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
                  </>
                )}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
              </button>
            </form>
          </div>

          <div className="glass-panel-strong rounded-2xl p-6 sm:p-7">
            <div className="flex items-center gap-2.5 mb-5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500 to-orange-500 p-2">
                <Brain className="w-full h-full text-white" />
              </div>
              <h2 className="text-lg font-semibold text-text-heading">Generated Questions</h2>
            </div>
            {interviewResult && interviewResult.length > 0 ? (
              <div className="space-y-3">
                {interviewResult.map((q, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.08 }}
                    className="flex items-start gap-3.5 p-4 rounded-xl bg-surface-light/40 border border-border/30"
                  >
                    <span className="w-7 h-7 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center flex-shrink-0 shadow-sm">
                      <span className="text-xs font-bold text-white">{i + 1}</span>
                    </span>
                    <p className="text-sm text-text-heading leading-relaxed">{q}</p>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-[380px] text-text-muted">
                <MessageSquare className="w-16 h-16 mb-4 opacity-20" />
                <p className="text-sm">Enter job details above</p>
                <p className="text-xs mt-1">to generate tailored interview questions</p>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}
