import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const evaluateDecision = async (payload) => {
  const response = await apiClient.post('/evaluate', payload);
  return response.data;
};

export const fetchForecast = async (params) => {
  const response = await apiClient.get('/forecast', { params });
  return response.data;
};

export const fetchVessels = async () => {
  const response = await apiClient.get('/vessels');
  return response.data;
};

export const fetchRoutes = async () => {
  const response = await apiClient.get('/routes');
  return response.data;
};

export default apiClient;