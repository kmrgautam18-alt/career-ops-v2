import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
import { Landing } from './pages/Landing';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Jobs } from './pages/Jobs';
import { Applications } from './pages/Applications';
import { Resumes } from './pages/Resumes';
import { AIPage } from './pages/AIPage';
import { AutoApply } from './pages/AutoApply';
import { InterviewCoach } from './pages/InterviewCoach';
import { NotificationPrefs } from './pages/NotificationPrefs';
import { Organizations } from './pages/Organizations';
import { VerifyEmail } from './pages/VerifyEmail';

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
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
            <Route path="/interview-coach" element={<InterviewCoach />} />
            <Route path="/notifications" element={<NotificationPrefs />} />
            <Route path="/organizations" element={<Organizations />} />
            <Route path="/verify-email" element={<VerifyEmail />} />
          </Route>
        </Routes>
      </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
