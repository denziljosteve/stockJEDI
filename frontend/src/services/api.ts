import axios from 'axios';
import { AIReport, PredictionResult, SentimentResult } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const stockService = {
  getHistoricalData: async (ticker: string, period = '1y') => {
    const response = await apiClient.get(`/stock/${ticker}/historical`, { params: { period } });
    return response.data;
  },
  analyzeStock: async (ticker: string) => {
    const response = await apiClient.post(`/stock/analyze?ticker=${ticker}`);
    return response.data;
  },
};

export const predictionService = {
  getPrediction: async (ticker: string): Promise<PredictionResult> => {
    const response = await apiClient.post(`/prediction/${ticker}`);
    return response.data;
  },
};

export const sentimentService = {
  getSentiment: async (ticker: string): Promise<{ sentiment: SentimentResult }> => {
    const response = await apiClient.post(`/sentiment/${ticker}`);
    return response.data;
  },
};

export const reportService = {
  generateReport: async (ticker: string): Promise<AIReport> => {
    const response = await apiClient.post(`/report/${ticker}`);
    return response.data;
  },
};
