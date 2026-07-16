import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Send, MessageSquare, Target } from 'lucide-react';

export function InterviewCoach() {
  const [jobTitle, setJobTitle] = useState('');
  const [company, setCompany] = useState('');
  const [difficulty, setDifficulty] = useState('medium');
  const [messages, setMessages] = useState<Array<{role: string; content: string}>>([]);
  const [answer, setAnswer] = useState('');
  const [coaching, setCoaching] = useState(false);

  const startInterview = async () => {
    if (!jobTitle || !company) return;
    setCoaching(true);
    setMessages([{ role: 'ai', content: `Starting interview for ${jobTitle} at ${company}...\n\nLet me ask you the first question.` }]);
    // In production: call streaming AI endpoint
    setMessages(prev => [...prev, {
      role: 'ai',
      content: `Tell me about a challenging project you worked on as a ${jobTitle}. What was your approach and what was the outcome?`
    }]);
  };

  const submitAnswer = () => {
    if (!answer.trim()) return;
    setMessages(prev => [...prev, { role: 'user', content: answer }]);
    setMessages(prev => [...prev, {
      role: 'ai',
      content: `Great answer! Here's some feedback:\n\n✅ Strengths: Clear structure, good use of metrics\n📈 Score: 82/100\n💡 Improvement: Consider adding more about team collaboration\n\nFollow-up: How did you handle any technical debt in that project?`
    }]);
    setAnswer('');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-text-heading flex items-center gap-3">
          <MessageSquare className="w-6 h-6 text-primary" />
          Interview Coach AI
        </h1>
        <p className="text-text-muted mt-1">Practice mock interviews with real-time AI feedback</p>
      </motion.div>

      {!coaching ? (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="p-6 rounded-2xl bg-surface border border-border/60 space-y-4"
        >
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Job Title</label>
              <input value={jobTitle} onChange={e => setJobTitle(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:ring-2 focus:ring-primary/10 transition-all"
                placeholder="e.g., Senior Engineer" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-heading mb-1.5">Company</label>
              <input value={company} onChange={e => setCompany(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:ring-2 focus:ring-primary/10 transition-all"
                placeholder="e.g., Google" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-text-heading mb-1.5">Difficulty</label>
            <select value={difficulty} onChange={e => setDifficulty(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:ring-2 focus:ring-primary/10 transition-all"
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <button onClick={startInterview}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-luxury"
          >
            <Target className="w-4 h-4" />
            Start Mock Interview
          </button>
        </motion.div>
      ) : (
        <div className="space-y-4">
          <div className="p-6 rounded-2xl bg-surface border border-border/60 space-y-4 max-h-96 overflow-y-auto">
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                  msg.role === 'ai' ? 'bg-primary/20 text-primary' : 'bg-accent/20 text-accent'
                }`}>
                  {msg.role === 'ai' ? <Sparkles className="w-4 h-4" /> : <Send className="w-4 h-4" />}
                </div>
                <div className={`p-3 rounded-xl max-w-[80%] ${
                  msg.role === 'ai' ? 'bg-surface-light border border-border/40' : 'bg-primary/10 border border-primary/20'
                }`}>
                  <p className="text-sm text-text whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="flex gap-3">
            <input value={answer} onChange={e => setAnswer(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && submitAnswer()}
              className="flex-1 px-4 py-3 rounded-xl bg-background border border-border-light text-text-heading focus:border-primary/50 focus:ring-2 focus:ring-primary/10 transition-all"
              placeholder="Type your answer..." />
            <button onClick={submitAnswer}
              className="px-5 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-luxury flex items-center gap-2"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
