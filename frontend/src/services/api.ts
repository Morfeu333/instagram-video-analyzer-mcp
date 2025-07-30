import axios from 'axios';
import {
  VideoAnalysisRequest,
  VideoAnalysisResponse,
  JobStatusResponse,
  JobListResponse,
  SystemStatsResponse,
} from '../types';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Video Analysis API
export const videoApi = {
  // Start video analysis
  analyzeVideo: async (request: VideoAnalysisRequest): Promise<VideoAnalysisResponse> => {
    const response = await api.post('/video/analyze', request);
    return response.data;
  },

  // Get job status
  getJobStatus: async (jobId: string): Promise<JobStatusResponse> => {
    const response = await api.get(`/video/status/${jobId}`);
    return response.data;
  },
};

// Jobs Management API
export const jobsApi = {
  // List jobs with pagination
  listJobs: async (
    page: number = 1,
    perPage: number = 10,
    status?: string
  ): Promise<JobListResponse> => {
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: perPage.toString(),
    });
    
    if (status) {
      params.append('status', status);
    }

    const response = await api.get(`/jobs?${params.toString()}`);
    return response.data;
  },

  // Delete job
  deleteJob: async (jobId: string, cleanupFiles: boolean = true): Promise<void> => {
    await api.delete(`/jobs/${jobId}?cleanup_files=${cleanupFiles}`);
  },

  // Cancel job
  cancelJob: async (jobId: string): Promise<void> => {
    await api.post(`/jobs/${jobId}/cancel`);
  },

  // Get system statistics
  getSystemStats: async (): Promise<SystemStatsResponse> => {
    const response = await api.get('/jobs/stats');
    return response.data;
  },
};

// Health check
export const healthApi = {
  // Check API health
  checkHealth: async (): Promise<{ status: string; timestamp: string }> => {
    const response = await api.get('/health');
    return response.data;
  },

  // Get root info
  getInfo: async (): Promise<{ message: string; version: string; status: string }> => {
    const response = await api.get('/');
    return response.data;
  },
};

// Utility functions
export const apiUtils = {
  // Format error message from API response
  formatErrorMessage: (error: any): string => {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
    if (error.message) {
      return error.message;
    }
    return 'An unexpected error occurred';
  },

  // Check if URL is valid Instagram URL
  isValidInstagramUrl: (url: string): boolean => {
    const instagramRegex = /^https?:\/\/(www\.)?instagram\.com\/(p|reel|tv)\/[A-Za-z0-9_-]+/;
    return instagramRegex.test(url);
  },

  // Format file size
  formatFileSize: (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  },

  // Format duration
  formatDuration: (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  },

  // Format date
  formatDate: (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
  },
};

export default api;
