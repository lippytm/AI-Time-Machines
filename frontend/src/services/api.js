import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/profile', data),
};

// Time Series API
export const timeSeriesAPI = {
  getAll: () => api.get('/timeseries'),
  getById: (id) => api.get(`/timeseries/${id}`),
  create: (data) => api.post('/timeseries', data),
  update: (id, data) => api.put(`/timeseries/${id}`, data),
  delete: (id) => api.delete(`/timeseries/${id}`),
};

// Models API
export const modelsAPI = {
  getAll: () => api.get('/models'),
  getById: (id) => api.get(`/models/${id}`),
  create: (data) => api.post('/models', data),
  delete: (id) => api.delete(`/models/${id}`),
};

// Predictions API
export const predictionsAPI = {
  getAll: () => api.get('/predictions'),
  getById: (id) => api.get(`/predictions/${id}`),
  create: (data) => api.post('/predictions', data),
  delete: (id) => api.delete(`/predictions/${id}`),
  export: (id, format) => api.get(`/predictions/${id}/export`, { params: { format }, responseType: 'blob' }),
};

// AI Tools API
export const aiToolsAPI = {
  getAll: (params) => api.get('/aitools', { params }),
  getById: (id) => api.get(`/aitools/${id}`),
  create: (data) => api.post('/aitools', data),
  update: (id, data) => api.put(`/aitools/${id}`, data),
  delete: (id) => api.delete(`/aitools/${id}`),
  getCategories: () => api.get('/aitools/categories'),
  getTypes: () => api.get('/aitools/types'),
};

// Integrations API
export const integrationsAPI = {
  getAll: (params) => api.get('/integrations', { params }),
  getById: (id) => api.get(`/integrations/${id}`),
  create: (data) => api.post('/integrations', data),
  update: (id, data) => api.put(`/integrations/${id}`, data),
  delete: (id) => api.delete(`/integrations/${id}`),
  test: (id) => api.post(`/integrations/${id}/test`),
  send: (id, predictionId) => api.post(`/integrations/${id}/send`, { predictionId }),
  getPlatforms: () => api.get('/integrations/platforms'),
};

export default api;
