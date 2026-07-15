import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Target, MessageSquare, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';
import { aiApi } from '../api/client';

type Tool = 'ats' | 'interview';

export function AIPage() {
  const [activeTool, setActiveTool] = useState<Tool>('ats');

  // ATS State
  const [atsForm, setAtsForm] = useState({ resume_text: '', job_description: '' });
  const [atsResult, setAtsResult] = useState<Record<string, unknown> | null>(null);
  const [atsLoading, setAtsLoading] = useState(false);

  // Interview State
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
      setAtsResult(res.data.data);
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
      setInterviewResult(Array.isArray(questions) ? questions : [String(questions)]);
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { message?: string } } })?.response?.data?.message || 'Failed to generate questions';
      setError(msg);
    } finally {
      setInterviewLoading(false);
    }
  };

  const tools = [
    { id: 'ats' as Tool, label: 'ATS Score', icon: Target, desc: 'Analyze your resume against a job description' },
    { id: 'interview' as Tool, label: 'Interview Questions', icon: MessageSquare, desc: 'Generate practice interview questions' },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-text-heading flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-accent" />
          AI Tools
        </h1>
        <p className="text-text mt-1">Leverage AI to optimize your career journey</p>
      </div>

      {/* Tool Selector */}
      <div className="flex gap-3">
        {tools.map((tool) => (
          <button
            key={tool.id}
            onClick={() => setActiveTool(tool.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
              activeTool === tool.id
                ? 'bg-primary text-white'
                : 'bg-surface text-text hover:text-text-heading border border-border'
            }`}
          >
            <tool.icon className="w-4 h-4" />
            {tool.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-danger/10 border border-danger/20 text-sm text-danger">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {error}
        </div>
      )}

      {/* ATS Score Tool */}
      {activeTool === 'ats' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid lg:grid-cols-2 gap-6"
        >
          <div className="p-4 rounded-xl bg-surface border border-border">
            <h2 className="text-lg font-semibold text-text-heading mb-4">Resume & Job Description</h2>
            <form onSubmit={handleAtsScore} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Resume Text</label>
                <textarea
                  value={atsForm.resume_text}
                  onChange={(e) => setAtsForm({ ...atsForm, resume_text: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary min-h-[150px] resize-y"
                  placeholder="Paste your resume text here..."
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Job Description</label>
                <textarea
                  value={atsForm.job_description}
                  onChange={(e) => setAtsForm({ ...atsForm, job_description: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary min-h-[150px] resize-y"
                  placeholder="Paste the job description here..."
                  required
                />
              </div>
              <button
                type="submit"
                disabled={atsLoading}
                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-hover disabled:opacity-50 transition-colors"
              >
                {atsLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Calculate ATS Score'}
              </button>
            </form>
          </div>

          <div className="p-4 rounded-xl bg-surface border border-border">
            <h2 className="text-lg font-semibold text-text-heading mb-4">Results</h2>
            {atsResult ? (
              <div className="space-y-4">
                <div className="text-center">
                  <div className="text-5xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                    {typeof atsResult.score === 'number' ? `${String(atsResult.score)}%` : 'N/A'}
                  </div>
                  <p className="text-sm text-text mt-2">ATS Compatibility Score</p>
                </div>
                {Array.isArray(atsResult.recommendations) && (
                  <div>
                    <h3 className="text-sm font-semibold text-text-heading mb-2">Recommendations</h3>
                    <ul className="space-y-2">
                      {(atsResult.recommendations as string[]).map((rec, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-text">
                          <CheckCircle2 className="w-4 h-4 text-success mt-0.5 flex-shrink-0" />
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-text/40">
                <Target className="w-12 h-12 mb-3" />
                <p className="text-sm">Submit your resume and job description to see results</p>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Interview Questions Tool */}
      {activeTool === 'interview' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid lg:grid-cols-2 gap-6"
        >
          <div className="p-4 rounded-xl bg-surface border border-border">
            <h2 className="text-lg font-semibold text-text-heading mb-4">Generate Questions</h2>
            <form onSubmit={handleInterviewQuestions} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Job Title</label>
                <input
                  type="text"
                  value={interviewForm.job_title}
                  onChange={(e) => setInterviewForm({ ...interviewForm, job_title: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                  placeholder="e.g., Software Engineer"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Company</label>
                <input
                  type="text"
                  value={interviewForm.company}
                  onChange={(e) => setInterviewForm({ ...interviewForm, company: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                  placeholder="e.g., Google"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-heading mb-1">Difficulty</label>
                <select
                  value={interviewForm.difficulty}
                  onChange={(e) => setInterviewForm({ ...interviewForm, difficulty: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-background border border-border text-text-heading focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
              <button
                type="submit"
                disabled={interviewLoading}
                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-hover disabled:opacity-50 transition-colors"
              >
                {interviewLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Generate Questions'}
              </button>
            </form>
          </div>

          <div className="p-4 rounded-xl bg-surface border border-border">
            <h2 className="text-lg font-semibold text-text-heading mb-4">Generated Questions</h2>
            {interviewResult ? (
              <div className="space-y-3">
                {interviewResult.map((q, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-surface-light/50">
                    <span className="w-6 h-6 rounded-full bg-primary-light flex items-center justify-center flex-shrink-0">
                      <span className="text-xs font-semibold text-primary">{i + 1}</span>
                    </span>
                    <p className="text-sm text-text-heading">{q}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-text/40">
                <MessageSquare className="w-12 h-12 mb-3" />
                <p className="text-sm">Fill in the details to generate interview questions</p>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}
