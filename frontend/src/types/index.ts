// API Types
export interface VideoAnalysisRequest {
  instagram_url: string;
  analysis_type: string;
}

export interface VideoAnalysisResponse {
  job_id: string;
  status: string;
  message: string;
}

export interface JobStatusResponse {
  job_id: string;
  status: string;
  progress: number;
  created_at?: string;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  analysis_result?: AnalysisResult;
}

export interface AnalysisResult {
  job_id: string;
  timestamp: string;
  analysis: {
    analysis_type: string;
    model_used: string;
    file_size: number;
    raw_response: string;
    structured_analysis: {
      sections: {
        resumo?: string;
        visual?: string;
        audio?: string;
        temas?: string;
        timestamps?: string;
        insights?: string;
      };
      full_text: string;
      word_count: number;
      analysis_type: string;
    };
  };
}

export interface JobSummary {
  job_id: string;
  instagram_url: string;
  status: string;
  created_at?: string;
  completed_at?: string;
  video_filename?: string;
  error_message?: string;
}

export interface JobListResponse {
  jobs: JobSummary[];
  total: number;
  page: number;
  per_page: number;
}

export interface SystemStatsResponse {
  total_jobs: number;
  pending_jobs: number;
  processing_jobs: number;
  completed_jobs: number;
  failed_jobs: number;
  disk_usage: {
    [key: string]: {
      path: string;
      total_size: number;
      total_size_mb: number;
      file_count: number;
    };
  };
}

// Component Props
export interface VideoUploaderProps {
  onJobCreated: (jobId: string) => void;
}

export interface JobStatusProps {
  jobId: string;
  onJobComplete?: (result: AnalysisResult) => void;
}

export interface AnalysisResultsProps {
  result: AnalysisResult;
}

// Job Status Enum
export enum JobStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled',
}

// Analysis Types
export enum AnalysisType {
  COMPREHENSIVE = 'comprehensive',
  SUMMARY = 'summary',
  TRANSCRIPTION = 'transcription',
  VISUAL_DESCRIPTION = 'visual_description',
}
