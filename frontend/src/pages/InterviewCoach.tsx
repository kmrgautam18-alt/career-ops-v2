import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sparkles, Send, Loader2, Target,
  ChevronRight, Clock, Award, Lightbulb, TrendingUp,
  Brain, BarChart3, Play,
} from 'lucide-react';

interface Message {
  role: 'ai' | 'user' | 'feedback';
  content: string;
  timestamp: Date;
  score?: number;
}

const sampleQuestions = [
  "Tell me about a time you led a difficult engineering project. What was your approach?",
  "How do you stay updated with the latest industry trends and technologies?",
  "Describe a situation where you had to resolve a conflict within your team.",
  "What's your approach to debugging complex production issues?",
  "Where do you see yourself professionally in 5 years?"
];

export function InterviewCoach() {
  const [jobTitle, setJobTitle] = useState('');
  const [company, setCompany] = useState('');
  const [difficulty, setDifficulty] = useState('medium');
  const [interviewType, setInterviewType] = useState('behavioral');
  const [sessionActive, setSessionActive] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isAiThinking, setIsAiThinking] = useState(false);
  const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
  const [sessionScore, setSessionScore] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const startSession = () => {
    if (!jobTitle || !company) return;
    setSessionActive(true);
    setMessages([{
      role: 'ai',
      content: `👋 Hey there! I'm your AI interview coach for the **${jobTitle}** position at **${company}**.\n\nI'll be asking you ${interviewType} interview questions at **${difficulty}** difficulty. Take your time with each answer — I'll provide feedback after every response.\n\nReady? Here's your first question:`,
      timestamp: new Date(),
    }]);
    setCurrentQuestionIdx(0);
    setSessionScore(0);

    // Simulate first question after a brief delay
    setTimeout(() => {
      setMessages(prev => [...prev, {
        role: 'ai',
        content: `**Question 1:** ${sampleQuestions[0]}`,
        timestamp: new Date(),
      }]);
      setIsAiThinking(false);
    }, 1200);
    setIsAiThinking(true);
  };

  const submitAnswer = () => {
    if (!inputValue.trim() || isAiThinking) return;

    const userMsg: Message = {
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsAiThinking(true);

    // Simulate AI feedback and next question
    setTimeout(() => {
      const score = Math.floor(Math.random() * 30) + 65;
      setSessionScore(prev => prev + score);
      const feedback: Message = {
        role: 'feedback',
        content: `📊 **Score: ${score}/100**\n\n✅ **Strengths:** Clear structure, good use of STAR method, relevant example\n💡 **Improvement areas:** Could add more quantifiable metrics, consider mentioning team collaboration\n\n📝 **Tip:** Try using the **CAR** format — Challenge, Action, Result — for maximum impact.`,
        timestamp: new Date(),
        score,
      };
      setMessages(prev => [...prev, feedback]);

      const nextIdx = currentQuestionIdx + 1;
      if (nextIdx < sampleQuestions.length) {
        setTimeout(() => {
          setMessages(prev => [...prev, {
            role: 'ai',
            content: `**Question ${nextIdx + 1}:** ${sampleQuestions[nextIdx]}`,
            timestamp: new Date(),
          }]);
          setCurrentQuestionIdx(nextIdx);
          setIsAiThinking(false);
        }, 800);
      } else {
        const totalScore = Math.round((sessionScore + score) / sampleQuestions.length);
        setTimeout(() => {
          setMessages(prev => [...prev, {
            role: 'ai',
            content: `🎉 **Interview Complete!**\n\n## Final Score: ${totalScore}/100\n\n### Summary\n- **Questions Answered:** ${sampleQuestions.length}\n- **Overall Performance:** ${totalScore >= 80 ? 'Excellent' : totalScore >= 65 ? 'Good' : 'Needs Practice'}\n- **Recommended Focus:** ${totalScore < 75 ? 'Structure, Quantifiable results, Technical depth' : 'Keep practicing with more specific examples'}\n\n### Next Steps\n1. Practice with **hard** difficulty next\n2. Record yourself to work on delivery\n3. Research the company's tech stack\n\nWant to try again with different questions?`,
            timestamp: new Date(),
          }]);
          setIsAiThinking(false);
        }, 1000);
      }
    }, 1500);
  };

  const resetSession = () => {
    setSessionActive(false);
    setMessages([]);
    setCurrentQuestionIdx(0);
    setSessionScore(0);
  };

  // Welcome / Setup Screen
  if (!sessionActive) {
    return (
      <div className="space-y-7 max-w-5xl mx-auto">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 p-2.5 shadow-lg">
              <Brain className="w-full h-full text-white" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-text-heading">Interview Coach AI</h1>
          </div>
          <p className="text-text-muted mt-1">Practice mock interviews with real-time AI feedback and scoring</p>
        </motion.div>

        {/* Setup Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-panel-strong rounded-2xl p-6 sm:p-8"
        >
          <div className="grid sm:grid-cols-2 gap-5 mb-6">
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Target Job Title</label>
              <input
                value={jobTitle} onChange={e => setJobTitle(e.target.value)}
                placeholder="e.g., Senior Software Engineer"
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all duration-200"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Target Company</label>
              <input
                value={company} onChange={e => setCompany(e.target.value)}
                placeholder="e.g., Google, Meta, Stripe"
                className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all duration-200"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Difficulty</label>
              <div className="flex gap-2">
                {(['easy', 'medium', 'hard'] as const).map(d => (
                  <button
                    key={d}
                    onClick={() => setDifficulty(d)}
                    className={`flex-1 py-2.5 rounded-xl text-sm font-medium transition-all border ${
                      difficulty === d
                        ? 'bg-primary/15 text-primary border-primary/30 shadow-sm'
                        : 'bg-background text-text-muted border-border-light hover:text-text-heading hover:border-border'
                    }`}
                  >
                    {d === 'easy' ? '🌱 Easy' : d === 'medium' ? '🔥 Medium' : '🚀 Hard'}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Interview Type</label>
              <div className="flex gap-2">
                {(['behavioral', 'technical', 'system-design'] as const).map(t => (
                  <button
                    key={t}
                    onClick={() => setInterviewType(t)}
                    className={`flex-1 py-2.5 rounded-xl text-sm font-medium transition-all border ${
                      interviewType === t
                        ? 'bg-primary/15 text-primary border-primary/30 shadow-sm'
                        : 'bg-background text-text-muted border-border-light hover:text-text-heading hover:border-border'
                    }`}
                  >
                    {t === 'behavioral' ? '💬 Behavioral' : t === 'technical' ? '⚡ Technical' : '🏗️ System Design'}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={startSession}
            disabled={!jobTitle || !company}
            className="group relative w-full flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold text-sm btn-luxury shadow-lg shadow-primary-glow/20 overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-4 h-4" />
            <span>Start Mock Interview</span>
            <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
          </motion.button>

          {/* Tips */}
          <div className="mt-6 grid grid-cols-3 gap-3">
            {[
              { icon: Target, label: 'Realistic Questions', desc: 'Tailored to your role' },
              { icon: BarChart3, label: 'Score & Feedback', desc: 'Instant performance rating' },
              { icon: Lightbulb, label: 'Improvement Tips', desc: 'Actionable suggestions' },
            ].map((tip, i) => (
              <div key={i} className="flex items-start gap-2.5 p-3 rounded-xl bg-surface-light/30 border border-border/30">
                <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <tip.icon className="w-4 h-4 text-primary" />
                </div>
                <div>
                  <p className="text-xs font-medium text-text-heading">{tip.label}</p>
                  <p className="text-[11px] text-text-muted mt-0.5">{tip.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    );
  }

  // Active Interview Session
  return (
    <div className="max-w-5xl mx-auto space-y-5">
      {/* Session Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between p-4 rounded-2xl bg-surface border border-border/60"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 p-2.5 shadow-lg animate-pulse-glow">
            <Brain className="w-full h-full text-white" />
          </div>
          <div>
            <p className="text-sm font-semibold text-text-heading">{jobTitle} @ {company}</p>
            <p className="text-xs text-text-muted flex items-center gap-1.5">
              <Clock className="w-3 h-3" />
              Question {Math.min(currentQuestionIdx + 1, sampleQuestions.length)} of {sampleQuestions.length}
              <span className="mx-1.5 text-border-light">·</span>
              <Award className="w-3 h-3 text-primary" />
              Score: {sessionScore > 0 ? Math.round(sessionScore / Math.max(currentQuestionIdx, 1)) : '—'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-primary/10 to-accent/10 border border-primary/20">
            <TrendingUp className="w-3.5 h-3.5 text-primary" />
            <span className="text-xs font-medium text-primary">{difficulty}</span>
          </div>
          <button
            onClick={resetSession}
            className="px-3 py-1.5 rounded-lg bg-surface-lighter text-text-muted hover:text-danger hover:bg-danger-light text-xs font-medium transition-all border border-border/40"
          >
            End Session
          </button>
        </div>
      </motion.div>

      {/* Chat Area */}
      <div className="relative glass-panel-strong rounded-2xl overflow-hidden">
        <div className="h-[500px] overflow-y-auto p-4 sm:p-6 space-y-4">
          <AnimatePresence>
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.3, delay: i > 0 ? 0 : 0 }}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ${
                  msg.role === 'ai'
                    ? 'bg-gradient-to-br from-amber-500 to-orange-500'
                    : msg.role === 'feedback'
                    ? 'bg-gradient-to-br from-emerald-500 to-teal-500'
                    : 'bg-gradient-to-br from-primary to-accent'
                }`}>
                  {msg.role === 'ai' ? (
                    <Sparkles className="w-4 h-4 text-white" />
                  ) : msg.role === 'feedback' ? (
                    <BarChart3 className="w-4 h-4 text-white" />
                  ) : (
                    <Send className="w-4 h-4 text-white" />
                  )}
                </div>

                {/* Message Bubble */}
                <div className={`max-w-[80%] ${
                  msg.role === 'feedback'
                    ? 'bg-gradient-to-br from-emerald-500/5 to-teal-500/5 border border-emerald-500/20'
                    : msg.role === 'user'
                    ? 'bg-primary/10 border border-primary/20'
                    : 'bg-surface-light/50 border border-border/40'
                } rounded-2xl p-4 shadow-sm`}>
                  {/* Role label */}
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-[11px] font-semibold uppercase tracking-wider ${
                      msg.role === 'ai' ? 'text-amber-400' : msg.role === 'feedback' ? 'text-emerald-400' : 'text-primary'
                    }`}>
                      {msg.role === 'ai' ? '🤖 AI Coach' : msg.role === 'feedback' ? '📊 Feedback' : '👤 You'}
                    </span>
                    {msg.score && (
                      <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold ${
                        msg.score >= 80 ? 'bg-emerald-500/20 text-emerald-400' : msg.score >= 65 ? 'bg-amber-500/20 text-amber-400' : 'bg-red-500/20 text-red-400'
                      }`}>
                        {msg.score}/100
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-text-heading whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                  <p className="text-[10px] text-text-muted/50 mt-2">
                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* AI Thinking Indicator */}
          <AnimatePresence>
            {isAiThinking && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="flex items-center gap-3"
              >
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <div className="flex items-center gap-2 px-4 py-3 rounded-2xl bg-surface-light/50 border border-border/40">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                  <span className="text-xs text-text-muted">Analyzing your answer...</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex gap-3 items-end"
      >
        <div className="flex-1 relative">
          <textarea
            value={inputValue}
            onChange={e => setInputValue(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submitAnswer(); } }}
            placeholder={currentQuestionIdx >= sampleQuestions.length ? "Session complete! Start a new one." : "Type your answer here... (Shift+Enter for new line)"}
            disabled={currentQuestionIdx >= sampleQuestions.length}
            className="w-full px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading placeholder:text-text-muted focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 transition-all duration-200 min-h-[56px] max-h-[120px] resize-y disabled:opacity-40"
            rows={2}
          />
        </div>
        <button
          onClick={submitAnswer}
          disabled={!inputValue.trim() || isAiThinking || currentQuestionIdx >= sampleQuestions.length}
          className="h-[56px] px-5 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-luxury shadow-lg shadow-primary-glow/20 flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          {isAiThinking ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span className="hidden sm:inline">Send</span>
            </>
          )}
        </button>
      </motion.div>

      {/* Keyboard Hint */}
      <p className="text-center text-[11px] text-text-muted/50">
        Press <kbd className="px-1.5 py-0.5 rounded bg-surface-lighter border border-border/40 text-text-muted text-[10px]">Enter</kbd> to send · <kbd className="px-1.5 py-0.5 rounded bg-surface-lighter border border-border/40 text-text-muted text-[10px]">Shift+Enter</kbd> for new line
      </p>
    </div>
  );
}
