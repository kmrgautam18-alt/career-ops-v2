import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
import { ErrorBoundary } from './components/ErrorBoundary';

// Lazy-loaded pages — code splitting for better performance
const Landing = lazy(() => import('./pages/Landing').then(m => ({ default: m.Landing })));
const Login = lazy(() => import('./pages/Login').then(m => ({ default: m.Login })));
const Register = lazy(() => import('./pages/Register').then(m => ({ default: m.Register })));
const Dashboard = lazy(() => import('./pages/Dashboard').then(m => ({ default: m.Dashboard })));
const Jobs = lazy(() => import('./pages/Jobs').then(m => ({ default: m.Jobs })));
const Applications = lazy(() => import('./pages/Applications').then(m => ({ default: m.Applications })));
const Resumes = lazy(() => import('./pages/Resumes').then(m => ({ default: m.Resumes })));
const AIPage = lazy(() => import('./pages/AIPage').then(m => ({ default: m.AIPage })));
const AutoApply = lazy(() => import('./pages/AutoApply').then(m => ({ default: m.AutoApply })));
const InterviewCoach = lazy(() => import('./pages/InterviewCoach').then(m => ({ default: m.InterviewCoach })));
const NotificationPrefs = lazy(() => import('./pages/NotificationPrefs').then(m => ({ default: m.NotificationPrefs })));
const Organizations = lazy(() => import('./pages/Organizations').then(m => ({ default: m.Organizations })));
const ResumeTemplates = lazy(() => import('./pages/ResumeTemplates').then(m => ({ default: m.ResumeTemplates })));
const VerifyEmail = lazy(() => import('./pages/VerifyEmail').then(m => ({ default: m.VerifyEmail })));
const HowItWorks = lazy(() => import('./pages/HowItWorks').then(m => ({ default: m.HowItWorks })));

// Skeleton fallback for lazy-loaded routes
function PageLoader() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background" role="status" aria-label="Loading page">
      <div className="flex flex-col items-center gap-3">
        <div className="relative w-10 h-10">
          <div className="absolute inset-0 rounded-full border-2 border-primary/20" />
          <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-primary animate-spin" />
        </div>
        <p className="text-sm text-text-muted animate-pulse">Loading...</p>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <ErrorBoundary>
            <div className="noise-overlay">
              <Suspense fallback={<PageLoader />}>
                <Routes>
                  <Route path="/" element={<Landing />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/verify-email" element={<VerifyEmail />} />
                  <Route
                    element={
                      <ProtectedRoute>
                        <Layout />
                      </ProtectedRoute>
                    }
                  >
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/jobs" element={<Jobs />} />
                    <Route path="/applications" element={<Applications />} />
                    <Route path="/resumes" element={<Resumes />} />
                    <Route path="/auto-apply" element={<AutoApply />} />
                    <Route path="/ai" element={<AIPage />} />
                    <Route path="/resume-templates" element={<ResumeTemplates />} />
                    <Route path="/interview-coach" element={<InterviewCoach />} />
                    <Route path="/notifications" element={<NotificationPrefs />} />
                    <Route path="/organizations" element={<Organizations />} />
                  <Route path="/how-it-works" element={<HowItWorks />} />
                  </Route>
                  {/* 404 catch-all */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Suspense>
            </div>
          </ErrorBoundary>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="text-center space-y-4">
        <div className="text-6xl font-bold text-gradient-primary">404</div>
        <h1 className="text-2xl font-bold text-text-heading">Page Not Found</h1>
        <p className="text-text-muted">The page you're looking for doesn't exist.</p>
        <a href="/dashboard" className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-luxury">
          Go Home
        </a>
      </div>
    </div>
  );
}

export default App;
