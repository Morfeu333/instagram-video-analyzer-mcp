import React from 'react'
import { motion } from 'framer-motion'
import { 
  Video, 
  FileText, 
  Eye, 
  Sparkles, 
  TrendingUp, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  BarChart3,
  Activity
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import VideoUploader from '@/components/VideoUploader'
import { useSystemStats, useJobsList } from '@/hooks/use-api'
import { useAppStore } from '@/store/app-store'
import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'

const Dashboard: React.FC = () => {
  const { data: stats } = useSystemStats()
  const { data: jobsList } = useJobsList(0, 5) // Get last 5 jobs
  const { setCurrentJobId, setCurrentAnalysis } = useAppStore()

  const handleJobCreated = (jobId: string) => {
    setCurrentJobId(jobId)
    setCurrentAnalysis(null)
  }

  const statsCards = [
    {
      title: "Total de Análises",
      value: stats?.total_jobs || 0,
      icon: BarChart3,
      color: "text-blue-600",
      bgColor: "bg-blue-100",
    },
    {
      title: "Concluídas",
      value: stats?.completed_jobs || 0,
      icon: CheckCircle,
      color: "text-green-600",
      bgColor: "bg-green-100",
    },
    {
      title: "Em Processamento",
      value: stats?.processing_jobs || 0,
      icon: Activity,
      color: "text-yellow-600",
      bgColor: "bg-yellow-100",
    },
    {
      title: "Falharam",
      value: stats?.failed_jobs || 0,
      icon: AlertCircle,
      color: "text-red-600",
      bgColor: "bg-red-100",
    },
  ]

  const features = [
    {
      title: "Análise de Vídeo",
      description: "Análise completa de vídeos do Instagram usando IA avançada para extrair insights valiosos.",
      icon: Video,
      color: "text-blue-600",
      bgColor: "bg-blue-100",
    },
    {
      title: "Transcrição Automática",
      description: "Transcrição automática de áudio com timestamps e identificação de elementos sonoros.",
      icon: FileText,
      color: "text-green-600",
      bgColor: "bg-green-100",
    },
    {
      title: "Descrição Visual",
      description: "Descrição detalhada de elementos visuais, cenários, objetos e pessoas no vídeo.",
      icon: Eye,
      color: "text-purple-600",
      bgColor: "bg-purple-100",
    },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600 mt-2">
              Analise vídeos do Instagram com inteligência artificial
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="success" className="px-3 py-1">
              Sistema Online
            </Badge>
          </div>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {statsCards.map((stat, index) => (
          <Card key={stat.title}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 ${stat.bgColor} rounded-lg flex items-center justify-center`}>
                  <stat.icon className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </motion.div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Video Uploader */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-blue-600" />
                <span>Nova Análise</span>
              </CardTitle>
              <CardDescription>
                Insira a URL de um vídeo do Instagram para começar a análise
              </CardDescription>
            </CardHeader>
            <CardContent>
              <VideoUploader onJobCreated={handleJobCreated} />
            </CardContent>
          </Card>
        </motion.div>

        {/* Recent Jobs */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Clock className="w-5 h-5 text-green-600" />
                <span>Análises Recentes</span>
              </CardTitle>
              <CardDescription>
                Últimas análises realizadas
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {jobsList?.jobs?.length ? (
                  jobsList.jobs.map((job) => (
                    <div key={job.job_id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {job.instagram_url || `Job ${job.job_id.slice(0, 8)}`}
                        </p>
                        <p className="text-xs text-gray-500">
                          {job.created_at && formatDistanceToNow(new Date(job.created_at), { 
                            addSuffix: true, 
                            locale: ptBR 
                          })}
                        </p>
                      </div>
                      <Badge 
                        variant={
                          job.status === 'completed' ? 'success' :
                          job.status === 'failed' ? 'destructive' :
                          job.status === 'processing' ? 'warning' : 'default'
                        }
                      >
                        {job.status}
                      </Badge>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Video className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                    <p>Nenhuma análise encontrada</p>
                    <p className="text-sm">Faça sua primeira análise!</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Features Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        {features.map((feature, index) => (
          <Card key={feature.title} className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className={`w-12 h-12 ${feature.bgColor} rounded-lg flex items-center justify-center mb-4`}>
                <feature.icon className={`w-6 h-6 ${feature.color}`} />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">{feature.title}</h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </CardContent>
          </Card>
        ))}
      </motion.div>
    </div>
  )
}

export default Dashboard
