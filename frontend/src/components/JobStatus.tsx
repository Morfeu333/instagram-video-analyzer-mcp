import React, { useState, useEffect } from 'react';
import { Clock, CheckCircle, XCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { videoApi, apiUtils } from '../services/api';
import { JobStatusProps, JobStatus as JobStatusEnum } from '../types';

const JobStatus: React.FC<JobStatusProps> = ({ jobId, onJobComplete }) => {
  const [jobStatus, setJobStatus] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJobStatus = async () => {
    try {
      const status = await videoApi.getJobStatus(jobId);
      setJobStatus(status);
      setError(null);

      // Call onJobComplete when job is completed
      if (status.status === JobStatusEnum.COMPLETED && status.analysis_result && onJobComplete) {
        onJobComplete(status.analysis_result);
      }
    } catch (error: any) {
      setError(apiUtils.formatErrorMessage(error));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchJobStatus();

    // Poll for updates if job is not completed
    const interval = setInterval(() => {
      if (jobStatus?.status === JobStatusEnum.PENDING || jobStatus?.status === JobStatusEnum.PROCESSING) {
        fetchJobStatus();
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, jobStatus?.status]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case JobStatusEnum.PENDING:
        return <Clock className="w-5 h-5 text-yellow-600" />;
      case JobStatusEnum.PROCESSING:
        return <RefreshCw className="w-5 h-5 text-blue-600 animate-spin" />;
      case JobStatusEnum.COMPLETED:
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case JobStatusEnum.FAILED:
        return <XCircle className="w-5 h-5 text-red-600" />;
      case JobStatusEnum.CANCELLED:
        return <AlertCircle className="w-5 h-5 text-gray-600" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case JobStatusEnum.PENDING:
        return 'Aguardando processamento';
      case JobStatusEnum.PROCESSING:
        return 'Processando vídeo';
      case JobStatusEnum.COMPLETED:
        return 'Análise concluída';
      case JobStatusEnum.FAILED:
        return 'Falha na análise';
      case JobStatusEnum.CANCELLED:
        return 'Análise cancelada';
      default:
        return 'Status desconhecido';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case JobStatusEnum.PENDING:
        return 'text-yellow-700 bg-yellow-50 border-yellow-200';
      case JobStatusEnum.PROCESSING:
        return 'text-blue-700 bg-blue-50 border-blue-200';
      case JobStatusEnum.COMPLETED:
        return 'text-green-700 bg-green-50 border-green-200';
      case JobStatusEnum.FAILED:
        return 'text-red-700 bg-red-50 border-red-200';
      case JobStatusEnum.CANCELLED:
        return 'text-gray-700 bg-gray-50 border-gray-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center">
          <RefreshCw className="w-6 h-6 text-blue-600 animate-spin mr-2" />
          <span className="text-gray-600">Carregando status...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center p-3 bg-red-50 border border-red-200 rounded-md">
          <XCircle className="w-5 h-5 text-red-600 mr-2" />
          <span className="text-red-700">{error}</span>
        </div>
      </div>
    );
  }

  if (!jobStatus) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Status da Análise</h3>

      {/* Job ID */}
      <div className="mb-4">
        <span className="text-sm text-gray-500">ID do Job: </span>
        <span className="text-sm font-mono text-gray-700">{jobStatus.job_id}</span>
      </div>

      {/* Status Badge */}
      <div className={`flex items-center p-3 border rounded-md mb-4 ${getStatusColor(jobStatus.status)}`}>
        {getStatusIcon(jobStatus.status)}
        <span className="ml-2 font-medium">{getStatusText(jobStatus.status)}</span>
      </div>

      {/* Progress Bar */}
      {(jobStatus.status === JobStatusEnum.PROCESSING || jobStatus.status === JobStatusEnum.PENDING) && (
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Progresso</span>
            <span>{Math.round(jobStatus.progress * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${jobStatus.progress * 100}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Timestamps */}
      <div className="space-y-2 text-sm text-gray-600">
        {jobStatus.created_at && (
          <div>
            <span className="font-medium">Criado em: </span>
            {apiUtils.formatDate(jobStatus.created_at)}
          </div>
        )}
        {jobStatus.started_at && (
          <div>
            <span className="font-medium">Iniciado em: </span>
            {apiUtils.formatDate(jobStatus.started_at)}
          </div>
        )}
        {jobStatus.completed_at && (
          <div>
            <span className="font-medium">Concluído em: </span>
            {apiUtils.formatDate(jobStatus.completed_at)}
          </div>
        )}
      </div>

      {/* Error Message */}
      {jobStatus.error_message && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <div className="flex items-start">
            <XCircle className="w-5 h-5 text-red-600 mr-2 mt-0.5" />
            <div>
              <div className="font-medium text-red-800">Erro na análise:</div>
              <div className="text-red-700 text-sm mt-1">{jobStatus.error_message}</div>
            </div>
          </div>
        </div>
      )}

      {/* Refresh Button */}
      <div className="mt-4 flex justify-end">
        <button
          onClick={fetchJobStatus}
          className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
        >
          <RefreshCw className="w-4 h-4 inline mr-1" />
          Atualizar
        </button>
      </div>
    </div>
  );
};

export default JobStatus;
