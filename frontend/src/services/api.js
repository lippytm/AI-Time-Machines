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
};

export default api;
