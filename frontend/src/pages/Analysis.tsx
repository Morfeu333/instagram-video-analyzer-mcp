import React, { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  ArrowLeft, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  Download,
  Share2,
  Eye
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import JobStatus from '@/components/JobStatus'
import AnalysisResults from '@/components/AnalysisResults'
import { useJobStatus } from '@/hooks/use-api'
import { useAppStore } from '@/store/app-store'
import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'

const Analysis: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>()
  const navigate = useNavigate()
  const { currentAnalysis, setCurrentJobId, setCurrentAnalysis } = useAppStore()
  
  const { data: jobStatus, isLoading, error } = useJobStatus(jobId || null)

  useEffect(() => {
    if (jobId) {
      setCurrentJobId(jobId)
    }
  }, [jobId, setCurrentJobId])

  useEffect(() => {
    if (jobStatus?.analysis_result) {
      setCurrentAnalysis(jobStatus.analysis_result)
    }
  }, [jobStatus, setCurrentAnalysis])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-600" />
      case 'processing':
        return <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
      default:
        return <Clock className="w-5 h-5 text-gray-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success'
      case 'failed':
        return 'destructive'
      case 'processing':
        return 'warning'
      default:
        return 'default'
    }
  }

  const getProgressValue = (status: string, progress?: number) => {
    if (progress) return progress * 100
    
    switch (status) {
      case 'pending':
        return 0
      case 'processing':
        return 50
      case 'completed':
        return 100
      case 'failed':
        return 0
      default:
        return 0
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Carregando análise...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Card className="w-full max-w-md">
          <CardContent className="p-6 text-center">
            <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Erro ao Carregar</h3>
            <p className="text-gray-600 mb-4">
              Não foi possível carregar os dados da análise.
            </p>
            <Button onClick={() => navigate('/dashboard')} variant="outline">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar ao Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between"
      >
        <div className="flex items-center space-x-4">
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Análise de Vídeo
            </h1>
            <p className="text-gray-600">
              Job ID: {jobId}
            </p>
          </div>
        </div>
        
        {jobStatus && (
          <div className="flex items-center space-x-3">
            {getStatusIcon(jobStatus.status)}
            <Badge variant={getStatusColor(jobStatus.status) as any}>
              {jobStatus.status}
            </Badge>
          </div>
        )}
      </motion.div>

      {/* Status Card */}
      {jobStatus && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                {getStatusIcon(jobStatus.status)}
                <span>Status da Análise</span>
              </CardTitle>
              <CardDescription>
                Acompanhe o progresso da análise em tempo real
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Progress Bar */}
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Progresso</span>
                  <span>{Math.round(getProgressValue(jobStatus.status, jobStatus.progress))}%</span>
                </div>
                <Progress 
                  value={getProgressValue(jobStatus.status, jobStatus.progress)} 
                  className="w-full"
                />
              </div>

              {/* Timestamps */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                {jobStatus.created_at && (
                  <div>
                    <p className="font-medium text-gray-900">Criado</p>
                    <p className="text-gray-600">
                      {formatDistanceToNow(new Date(jobStatus.created_at), { 
                        addSuffix: true, 
                        locale: ptBR 
                      })}
                    </p>
                  </div>
                )}
                
                {jobStatus.started_at && (
                  <div>
                    <p className="font-medium text-gray-900">Iniciado</p>
                    <p className="text-gray-600">
                      {formatDistanceToNow(new Date(jobStatus.started_at), { 
                        addSuffix: true, 
                        locale: ptBR 
                      })}
                    </p>
                  </div>
                )}
                
                {jobStatus.completed_at && (
                  <div>
                    <p className="font-medium text-gray-900">Concluído</p>
                    <p className="text-gray-600">
                      {formatDistanceToNow(new Date(jobStatus.completed_at), { 
                        addSuffix: true, 
                        locale: ptBR 
                      })}
                    </p>
                  </div>
                )}
              </div>

              {/* Error Message */}
              {jobStatus.error_message && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                  <div className="flex items-center space-x-2">
                    <AlertCircle className="w-5 h-5 text-red-600" />
                    <p className="font-medium text-red-800">Erro na Análise</p>
                  </div>
                  <p className="text-red-700 mt-1">{jobStatus.error_message}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Analysis Results */}
      {currentAnalysis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <AnalysisResults result={currentAnalysis} />
        </motion.div>
      )}

      {/* Loading State for Processing */}
      {jobStatus?.status === 'processing' && !currentAnalysis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card>
            <CardContent className="p-12 text-center">
              <Loader2 className="w-12 h-12 animate-spin mx-auto mb-4 text-blue-600" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Processando Vídeo
              </h3>
              <p className="text-gray-600 mb-4">
                A IA está analisando o vídeo. Isso pode levar alguns minutos...
              </p>
              <div className="flex justify-center space-x-2 text-sm text-gray-500">
                <span>•</span>
                <span>Download do vídeo</span>
                <span>•</span>
                <span>Upload para IA</span>
                <span>•</span>
                <span>Análise em progresso</span>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  )
}

export default Analysis
