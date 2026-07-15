import axios from 'axios';

const API_BASE = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
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
          const response = await axios.post(`${API_BASE}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          const { access_token } = response.data.data;
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
  }
);

export default apiClient;

// Auth
export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post('/auth/login', { email, password }),
  register: (data: { email: string; password: string; username: string; full_name: string }) =>
    apiClient.post('/users/register', data),
  refresh: (refresh_token: string) =>
    apiClient.post('/auth/refresh', { refresh_token }),
  getMe: () => apiClient.get('/users/me'),
};

// Jobs
export const jobsApi = {
  list: (params?: Record<string, string>) =>
    apiClient.get('/jobs', { params }),
  get: (id: number) => apiClient.get(`/jobs/${id}`),
  create: (data: Record<string, unknown>) =>
    apiClient.post('/jobs', data),
  update: (id: number, data: Record<string, unknown>) =>
    apiClient.patch(`/jobs/${id}`, data),
  delete: (id: number) => apiClient.delete(`/jobs/${id}`),
  match: (jobId: number, resumeId: number) =>
    apiClient.post(`/jobs/${jobId}/match/${resumeId}`),
};

// Applications
export const applicationsApi = {
  list: (params?: Record<string, string>) =>
    apiClient.get('/applications', { params }),
  get: (id: number) => apiClient.get(`/applications/${id}`),
  create: (data: Record<string, unknown>) =>
    apiClient.post('/applications', data),
  update: (id: number, data: Record<string, unknown>) =>
    apiClient.patch(`/applications/${id}`, data),
  delete: (id: number) => apiClient.delete(`/applications/${id}`),
};

// Resumes
export const resumesApi = {
  list: () => apiClient.get('/resumes'),
  get: (id: number) => apiClient.get(`/resumes/${id}`),
  upload: (formData: FormData) =>
    apiClient.post('/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  update: (id: number, data: Record<string, unknown>) =>
    apiClient.patch(`/resumes/${id}`, data),
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

// AI
export const aiApi = {
  atsScore: (data: { resume_text: string; job_description: string }) =>
    apiClient.post('/ai/ats-score', data),
  interviewQuestions: (data: { job_title: string; company: string; difficulty?: string }) =>
    apiClient.post('/ai/interview/questions', data),
  resumeOptimize: (data: { resume_text: string; job_description: string }) =>
    apiClient.post('/ai/resume-optimize', data),
};
