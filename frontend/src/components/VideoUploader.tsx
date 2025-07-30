import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, AlertCircle, CheckCircle, Sparkles, Brain, FileText, Eye, Zap } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { useAnalyzeVideo } from '@/hooks/use-api'
import { VideoAnalysisRequest } from '@/types'

interface VideoUploaderProps {
  onJobCreated?: (jobId: string) => void
}

const VideoUploader: React.FC<VideoUploaderProps> = ({ onJobCreated }) => {
  const navigate = useNavigate()
  const [url, setUrl] = useState('')
  const [analysisType, setAnalysisType] = useState('comprehensive')
  const [error, setError] = useState<string | null>(null)

  const analyzeVideoMutation = useAnalyzeVideo()

  const isValidInstagramUrl = (url: string): boolean => {
    const instagramRegex = /^https?:\/\/(www\.)?(instagram\.com|instagr\.am)\/(p|reel|tv)\/[A-Za-z0-9_-]+\/?/
    return instagramRegex.test(url)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    // Validate URL
    if (!url.trim()) {
      setError('Por favor, insira uma URL do Instagram')
      return
    }

    if (!isValidInstagramUrl(url)) {
      setError('URL do Instagram inválida. Use uma URL de post, reel ou IGTV')
      return
    }

    const request: VideoAnalysisRequest = {
      instagram_url: url,
      analysis_type: analysisType,
    }

    analyzeVideoMutation.mutate(request, {
      onSuccess: (response) => {
        if (onJobCreated) {
          onJobCreated(response.job_id)
        }
        // Navigate to analysis page
        navigate(`/analysis/${response.job_id}`)
        setUrl('')
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Erro ao iniciar análise')
      },
    })
  }

  const analysisOptions = [
    {
      value: 'comprehensive',
      label: 'Análise Completa',
      description: 'Análise detalhada com todos os aspectos',
      icon: Brain,
      color: 'from-blue-500 to-purple-500'
    },
    {
      value: 'summary',
      label: 'Resumo',
      description: 'Resumo conciso do conteúdo',
      icon: Sparkles,
      color: 'from-green-500 to-blue-500'
    },
    {
      value: 'transcription',
      label: 'Transcrição',
      description: 'Transcrição completa do áudio',
      icon: FileText,
      color: 'from-yellow-500 to-orange-500'
    },
    {
      value: 'visual',
      label: 'Descrição Visual',
      description: 'Descrição detalhada dos elementos visuais',
      icon: Eye,
      color: 'from-purple-500 to-pink-500'
    },
  ]

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center space-x-3">
          <div className="p-2 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl">
            <Upload className="w-6 h-6 text-white" />
          </div>
          <span>Analisar Vídeo do Instagram</span>
        </CardTitle>
        <CardDescription>
          Cole a URL de um vídeo do Instagram e escolha o tipo de análise desejada
        </CardDescription>
      </CardHeader>
      <CardContent>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Error Messages */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-md">
              <div className="flex items-center space-x-2">
                <AlertCircle className="w-5 h-5 text-red-600" />
                <p className="font-medium text-red-800">Erro</p>
              </div>
              <p className="text-red-700 mt-1">{error}</p>
            </div>
          )}

          {/* URL Input */}
          <div className="space-y-2">
            <label htmlFor="url" className="block text-sm font-medium text-gray-700">
              URL do Instagram
            </label>
            <Input
              type="url"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.instagram.com/p/..."
              disabled={analyzeVideoMutation.isPending}
              className="w-full"
            />
            <p className="text-xs text-gray-500">
              Cole a URL de um post, reel ou IGTV do Instagram
            </p>
          </div>

          {/* Analysis Type Selection */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              Tipo de Análise
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {analysisOptions.map((option) => {
                const IconComponent = option.icon
                const isSelected = analysisType === option.value
                return (
                  <label
                    key={option.value}
                    className={`relative cursor-pointer group ${analyzeVideoMutation.isPending ? 'cursor-not-allowed opacity-50' : ''}`}
                  >
                    <input
                      type="radio"
                      name="analysisType"
                      value={option.value}
                      checked={isSelected}
                      onChange={(e) => setAnalysisType(e.target.value)}
                      className="sr-only"
                      disabled={analyzeVideoMutation.isPending}
                    />
                    <div className={`
                      relative p-4 rounded-xl border-2 transition-all duration-300
                      ${isSelected
                        ? 'border-blue-500 bg-blue-50 shadow-lg shadow-blue-500/20'
                        : 'border-gray-200 bg-white hover:border-blue-300 hover:bg-blue-50'
                      }
                    `}>
                      <div className="flex items-start space-x-3">
                        <div className={`
                          p-2 rounded-lg bg-gradient-to-r ${option.color}
                          ${isSelected ? 'shadow-lg' : 'opacity-70 group-hover:opacity-100'}
                        `}>
                          <IconComponent className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1">
                          <div className={`font-medium ${isSelected ? 'text-blue-700' : 'text-gray-700'}`}>
                            {option.label}
                          </div>
                          <div className={`text-sm mt-1 ${isSelected ? 'text-blue-600' : 'text-gray-500'}`}>
                            {option.description}
                          </div>
                        </div>
                      </div>
                      {isSelected && (
                        <div className="absolute top-2 right-2">
                          <CheckCircle className="w-5 h-5 text-blue-400" />
                        </div>
                      )}
                    </div>
                  </label>
                );
              })}
            </div>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={analyzeVideoMutation.isPending || !url.trim()}
            className="w-full"
            size="lg"
          >
            {analyzeVideoMutation.isPending ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                Iniciando Análise...
              </div>
            ) : (
              <div className="flex items-center justify-center">
                <Zap className="w-5 h-5 mr-2" />
                Iniciar Análise
              </div>
            )}
          </Button>
        </form>

        {/* Instructions */}
        <div className="mt-8 p-6 bg-gray-50 rounded-xl border border-gray-200">
          <h3 className="font-medium text-gray-800 mb-3 flex items-center">
            <Sparkles className="w-4 h-4 mr-2 text-blue-600" />
            Como usar:
          </h3>
          <ol className="text-sm text-gray-600 space-y-2">
            <li className="flex items-start">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-3 mt-0.5">1</span>
              Copie a URL de um vídeo do Instagram (post, reel ou IGTV)
            </li>
            <li className="flex items-start">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-3 mt-0.5">2</span>
              Cole a URL no campo acima
            </li>
            <li className="flex items-start">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-3 mt-0.5">3</span>
              Escolha o tipo de análise desejada
            </li>
            <li className="flex items-start">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-3 mt-0.5">4</span>
              Clique em "Iniciar Análise" e aguarde o processamento
            </li>
          </ol>
        </div>
      </CardContent>
    </Card>
  )
}

export default VideoUploader
