import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, Loader2, ArrowRight } from 'lucide-react';
import apiClient from '../api/client';

export function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Verifying your email...');

  useEffect(() => {
    const token = searchParams.get('token');
    const userId = searchParams.get('user_id');

    if (!token || !userId) {
      setStatus('error');
      setMessage('Invalid verification link.');
      return;
    }

    apiClient.get(`/auth/verify-email?user_id=${userId}&token=${token}`)
      .then(() => {
        setStatus('success');
        setMessage('Email verified successfully!');
      })
      .catch((err: unknown) => {
        const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Verification failed.';
        setStatus('error');
        setMessage(msg);
      });
  }, [searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-panel-strong rounded-2xl p-8 max-w-md w-full text-center space-y-6"
      >
        {status === 'loading' && (
          <div className="space-y-4">
            <Loader2 className="w-16 h-16 text-primary animate-spin mx-auto" />
            <h1 className="text-xl font-bold text-text-heading">Verifying...</h1>
            <p className="text-text-muted">{message}</p>
          </div>
        )}

        {status === 'success' && (
          <div className="space-y-4">
            <div className="w-16 h-16 rounded-full bg-success/20 flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-10 h-10 text-success" />
            </div>
            <h1 className="text-xl font-bold text-text-heading">Email Verified 🎉</h1>
            <p className="text-text-muted">{message}</p>
            <p className="text-sm text-text-muted">You can now access all Career-Ops features.</p>
            <Link to="/login"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-luxury"
            >
              Sign In <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        )}

        {status === 'error' && (
          <div className="space-y-4">
            <div className="w-16 h-16 rounded-full bg-danger/20 flex items-center justify-center mx-auto">
              <XCircle className="w-10 h-10 text-danger" />
            </div>
            <h1 className="text-xl font-bold text-text-heading">Verification Failed</h1>
            <p className="text-text-muted">{message}</p>
            <Link to="/login"
              className="inline-flex items-center gap-2 text-primary hover:text-primary-hover transition-colors"
            >
              Back to Login <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        )}
      </motion.div>
    </div>
  );
}
