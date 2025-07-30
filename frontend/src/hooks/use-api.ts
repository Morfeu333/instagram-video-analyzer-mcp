import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  videoApi, 
  jobsApi, 
  healthApi 
} from '@/services/api'
import { 
  VideoAnalysisRequest, 
  JobStatusResponse, 
  JobListResponse, 
  SystemStatsResponse 
} from '@/types'
import { useToast } from '@/hooks/use-toast'
import { useAppStore } from '@/store/app-store'

// Health Check
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: healthApi.checkHealth,
    refetchInterval: 30000, // Check every 30 seconds
    retry: 3,
  })
}

// Video Analysis
export const useAnalyzeVideo = () => {
  const { toast } = useToast()
  const queryClient = useQueryClient()
  const { setCurrentJobId, addToHistory } = useAppStore()

  return useMutation({
    mutationFn: (data: VideoAnalysisRequest) => videoApi.analyzeVideo(data),
    onSuccess: (response) => {
      setCurrentJobId(response.job_id)
      addToHistory({
        job_id: response.job_id,
        instagram_url: '',
        status: 'pending',
        created_at: new Date().toISOString(),
      })
      toast({
        title: "Análise Iniciada",
        description: `Job ${response.job_id} criado com sucesso!`,
        variant: "default",
      })
      // Invalidate jobs list to refresh
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
    onError: (error: any) => {
      toast({
        title: "Erro na Análise",
        description: error.response?.data?.detail || "Erro ao iniciar análise",
        variant: "destructive",
      })
    },
  })
}

// Job Status
export const useJobStatus = (jobId: string | null, enabled = true) => {
  const { updateHistoryItem, setCurrentAnalysis } = useAppStore()
  const { toast } = useToast()

  return useQuery({
    queryKey: ['job-status', jobId],
    queryFn: () => videoApi.getJobStatus(jobId!),
    enabled: enabled && !!jobId,
    refetchInterval: (data) => {
      // Stop polling if job is completed or failed
      if (data?.status === 'completed' || data?.status === 'failed') {
        return false
      }
      return 3000 // Poll every 3 seconds
    },
    onSuccess: (data: JobStatusResponse) => {
      // Update history
      updateHistoryItem(data.job_id, {
        status: data.status,
        completed_at: data.completed_at,
      })

      // If completed, set the analysis result
      if (data.status === 'completed' && data.analysis_result) {
        setCurrentAnalysis(data.analysis_result)
        toast({
          title: "Análise Concluída",
          description: "A análise do vídeo foi concluída com sucesso!",
          variant: "success",
        })
      }

      // If failed, show error
      if (data.status === 'failed') {
        toast({
          title: "Análise Falhou",
          description: data.error_message || "Erro durante a análise",
          variant: "destructive",
        })
      }
    },
  })
}

// Jobs List
export const useJobsList = (page = 0, perPage = 20) => {
  return useQuery({
    queryKey: ['jobs', page, perPage],
    queryFn: () => jobsApi.getJobs(page, perPage),
    staleTime: 30000, // Consider data fresh for 30 seconds
  })
}

// System Stats
export const useSystemStats = () => {
  const { setSystemStats } = useAppStore()

  return useQuery({
    queryKey: ['system-stats'],
    queryFn: jobsApi.getStats,
    refetchInterval: 60000, // Refresh every minute
    onSuccess: (data: SystemStatsResponse) => {
      setSystemStats(data)
    },
  })
}

// Delete Job (if we implement this endpoint)
export const useDeleteJob = () => {
  const { toast } = useToast()
  const queryClient = useQueryClient()
  const { removeFromHistory } = useAppStore()

  return useMutation({
    mutationFn: (jobId: string) => {
      // This would need to be implemented in the backend
      throw new Error('Delete job endpoint not implemented')
    },
    onSuccess: (_, jobId) => {
      removeFromHistory(jobId)
      toast({
        title: "Job Deletado",
        description: "Job removido com sucesso",
        variant: "success",
      })
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
    onError: (error: any) => {
      toast({
        title: "Erro ao Deletar",
        description: error.message || "Erro ao deletar job",
        variant: "destructive",
      })
    },
  })
}
