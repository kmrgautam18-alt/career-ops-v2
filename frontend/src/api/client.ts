import axios from 'axios';

const API_BASE = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE}/auth/refresh`, { refresh_token: refreshToken });
          const { access_token } = res.data.data;
          localStorage.setItem('access_token', access_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        } catch {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      } else {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  },
);

export default apiClient;

// Auth
export const authApi = {
  login: (email: string, password: string) => apiClient.post('/auth/login', { email, password }),
  register: (data: { email: string; password: string; username: string; full_name: string }) => apiClient.post('/users/register', data),
  refresh: (refresh_token: string) => apiClient.post('/auth/refresh', { refresh_token }),
  getMe: () => apiClient.get('/users/me'),
};

// Jobs
export const jobsApi = {
  list: (params?: Record<string, string>) => apiClient.get('/jobs', { params }),
  get: (id: number) => apiClient.get(`/jobs/${id}`),
  create: (data: Record<string, unknown>) => apiClient.post('/jobs', data),
  update: (id: number, data: Record<string, unknown>) => apiClient.patch(`/jobs/${id}`, data),
  delete: (id: number) => apiClient.delete(`/jobs/${id}`),
  match: (jobId: number, resumeId: number) => apiClient.post(`/jobs/${jobId}/match/${resumeId}`),
};

// Applications
export const applicationsApi = {
  list: (params?: Record<string, string>) => apiClient.get('/applications', { params }),
  get: (id: number) => apiClient.get(`/applications/${id}`),
  create: (data: Record<string, unknown>) => apiClient.post('/applications', data),
  update: (id: number, data: Record<string, unknown>) => apiClient.patch(`/applications/${id}`, data),
  delete: (id: number) => apiClient.delete(`/applications/${id}`),
};

// Resumes
export const resumesApi = {
  list: () => apiClient.get('/resumes'),
  get: (id: number) => apiClient.get(`/resumes/${id}`),
  upload: (formData: FormData) => apiClient.post('/resumes/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  update: (id: number, data: Record<string, unknown>) => apiClient.patch(`/resumes/${id}`, data),
  delete: (id: number) => apiClient.delete(`/resumes/${id}`),
};

// Dashboard
export const dashboardApi = {
  get: () => apiClient.get('/dashboard'),
  recentJobs: () => apiClient.get('/dashboard/recent-jobs'),
  recentApplications: () => apiClient.get('/dashboard/recent-applications'),
  statusSummary: () => apiClient.get('/dashboard/status-summary'),
  resumeSummary: () => apiClient.get('/dashboard/resume-summary'),
};

// --- SSE Streaming ---

export interface StreamCallbacks {
  onToken: (text: string) => void;
  onDone: () => void;
  onError: (error: string) => void;
}

async function streamSse(
  url: string,
  body: unknown,
  { onToken, onDone, onError }: StreamCallbacks,
): Promise<AbortController> {
  const controller = new AbortController();
  const token = localStorage.getItem('access_token');

  (async () => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!response.ok) { onError(`HTTP ${response.status}`); return; }

      const reader = response.body?.getReader();
      if (!reader) { onError('No response body'); return; }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6).trim();
            if (data === '[DONE]') { onDone(); return; }
            try {
              const parsed = JSON.parse(data);
              if (parsed.text) onToken(parsed.text);
              if (parsed.error) onError(parsed.error);
            } catch { /* ignore */ }
          }
        }
      }
      onDone();
    } catch (err: unknown) {
      if ((err as Error)?.name === 'AbortError') return;
      onError(String(err));
    }
  })();

  return controller;
}

// Auto-Apply (Job Application Engine)
export const autoApplyApi = {
  dashboard: () => apiClient.get('/auto-apply/dashboard'),
  list: () => apiClient.get('/auto-apply'),
  get: (id: number) => apiClient.get(`/auto-apply/${id}`),
  create: (data: Record<string, unknown>) => apiClient.post('/auto-apply', data),
  update: (id: number, data: Record<string, unknown>) => apiClient.patch(`/auto-apply/${id}`, data),
  delete: (id: number) => apiClient.delete(`/auto-apply/${id}`),
  scrape: (data: { source: string; query: string; location?: string; max_results?: number }) => apiClient.post('/auto-apply/scrape', data),
  optimize: (id: number) => apiClient.post(`/auto-apply/${id}/optimize`),
  sendEmail: (id: number, hrEmail?: string) => {
    const params = hrEmail ? `?hr_email=${encodeURIComponent(hrEmail)}` : '';
    return apiClient.post(`/auto-apply/${id}/send${params}`);
  },
  followup: (id: number) => apiClient.post(`/auto-apply/${id}/followup`),
  interview: (id: number, interviewDate: string, interviewType: string) =>
    apiClient.post(`/auto-apply/${id}/interview?interview_date=${encodeURIComponent(interviewDate)}&interview_type=${interviewType}`),
  fullPipeline: (source: string, query: string, location?: string, maxResults?: number) => {
    let url = `/auto-apply/full-pipeline?source=${encodeURIComponent(source)}&query=${encodeURIComponent(query)}`;
    if (location) url += `&location=${encodeURIComponent(location)}`;
    if (maxResults) url += `&max_results=${maxResults}`;
    return apiClient.post(url);
  },
};

// AI
export const aiApi = {
  atsScore: (data: { resume_text: string; job_description: string }) => apiClient.post('/ai/ats-score', data),
  interviewQuestions: (data: { job_title: string; company: string; difficulty?: string }) => apiClient.post('/ai/interview/questions', data),
  resumeOptimize: (data: { resume_text: string; job_description: string }) => apiClient.post('/ai/resume-optimize', data),
  jobMatch: (data: { profile: string; job_details: string }) => apiClient.post('/ai/job-match', data),
};

// Data Export
export const exportApi = {
  json: () => apiClient.get('/export/json', { responseType: 'blob' }),
  csv: () => apiClient.get('/export/csv', { responseType: 'blob' }),
};

// Email Verification
export const verificationApi = {
  sendVerification: () => apiClient.post('/auth/send-verification'),
  verify: (userId: number, token: string) => apiClient.get(`/auth/verify-email?user_id=${userId}&token=${token}`),
  forgotPassword: (email: string) => apiClient.post(`/auth/forgot-password?email=${encodeURIComponent(email)}`),
  resetPassword: (userId: number, token: string, newPassword: string) =>
    apiClient.post(`/auth/reset-password?user_id=${userId}&token=${token}&new_password=${encodeURIComponent(newPassword)}`),
};

// Notification Preferences
export const notificationPrefsApi = {
  get: () => apiClient.get('/notifications/preferences/'),
  update: (eventType: string, channel: string, enabled: boolean) =>
    apiClient.put(`/notifications/preferences/${eventType}/${channel}?enabled=${enabled}`),
  updateAll: (enabled: boolean) => apiClient.put(`/notifications/preferences/all?enabled=${enabled}`),
};

// Organizations
export const organizationsApi = {
  list: () => apiClient.get('/organizations/'),
  create: (name: string, slug: string) => apiClient.post(`/organizations/?name=${encodeURIComponent(name)}&slug=${encodeURIComponent(slug)}`),
  members: (orgId: number) => apiClient.get(`/organizations/${orgId}/members`),
  invite: (orgId: number, userId: number, role: string) => apiClient.post(`/organizations/${orgId}/invite?user_id=${userId}&role=${role}`),
};

// Audit Logs
export const auditLogsApi = {
  list: (params?: Record<string, string>) => apiClient.get('/audit-logs/', { params }),
};

export const aiStreamApi = {
  atsScore: (data: { resume_text: string; job_description: string }, cb: StreamCallbacks) =>
    streamSse(`${API_BASE}/ai/ats-score/stream`, data, cb),
  interviewQuestions: (data: { job_title: string; company: string; difficulty?: string }, cb: StreamCallbacks) =>
    streamSse(`${API_BASE}/ai/interview/questions/stream`, data, cb),
  resumeOptimize: (data: { resume_text: string; job_description: string }, cb: StreamCallbacks) =>
    streamSse(`${API_BASE}/ai/resume-optimize/stream`, data, cb),
  jobMatch: (data: { profile: string; job_details: string }, cb: StreamCallbacks) =>
    streamSse(`${API_BASE}/ai/job-match/stream`, data, cb),
};
