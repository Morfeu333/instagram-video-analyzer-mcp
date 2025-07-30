import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Eye,
  Volume2,
  MessageSquare,
  Lightbulb,
  Globe,
  Clapperboard,
  Download,
  Share2,
  Copy,
  FileText,
  Clock,
  User,
  Tag
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useToast } from '@/hooks/use-toast'
import { AnalysisResult } from '@/types'

interface AnalysisResultsProps {
  result: AnalysisResult
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result }) => {
  const { toast } = useToast()
  const [activeTab, setActiveTab] = useState('overview')

  // Extract the raw response from the analysis result
  const rawResponse = result.analysis?.raw_response || ''
  const analysisType = result.analysis?.analysis_type || 'comprehensive'
  const modelUsed = result.analysis?.model_used || 'gemini-2.5-flash'
  const fileSize = result.analysis?.file_size || 0

  const handleCopyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text)
    toast({
      title: "Copiado!",
      description: `${label} copiado para a área de transferência`,
      variant: "success",
    })
  }

  const handleDownload = (format: 'json' | 'txt') => {
    const content = format === 'json'
      ? JSON.stringify(result, null, 2)
      : formatAsText(result)

    const blob = new Blob([content], {
      type: format === 'json' ? 'application/json' : 'text/plain'
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `analysis-${Date.now()}.${format}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    toast({
      title: "Download Iniciado",
      description: `Arquivo ${format.toUpperCase()} baixado com sucesso`,
      variant: "success",
    })
  }

  const formatAsText = (result: AnalysisResult): string => {
    return `
ANÁLISE DE VÍDEO INSTAGRAM
==========================

Tipo de Análise: ${analysisType}
Modelo Usado: ${modelUsed}
Tamanho do Arquivo: ${(fileSize / 1024 / 1024).toFixed(2)} MB

ANÁLISE COMPLETA:
${rawResponse}
    `.trim()
  }

  // Parse sections from raw response if possible
  const parseSections = (text: string) => {
    const sections: { [key: string]: string } = {}

    // Try to extract sections based on markdown headers
    const sectionPatterns = [
      { key: 'resumo', pattern: /\*\*1\.\s*Resumo Geral\*\*\s*(.*?)(?=\*\*\d+\.|$)/s },
      { key: 'visual', pattern: /\*\*2\.\s*Análise Visual\*\*\s*(.*?)(?=\*\*\d+\.|$)/s },
      { key: 'audio', pattern: /\*\*3\.\s*Análise de Áudio\*\*\s*(.*?)(?=\*\*\d+\.|$)/s },
      { key: 'temas', pattern: /\*\*4\.\s*Temas e Mensagens\*\*\s*(.*?)(?=\*\*\d+\.|$)/s },
      { key: 'timestamps', pattern: /\*\*5\.\s*Timestamps Importantes\*\*\s*(.*?)(?=\*\*\d+\.|$)/s },
      { key: 'insights', pattern: /\*\*6\.\s*Insights e Análise\*\*\s*(.*?)(?=\*\*\d+\.|$)/s }
    ]

    sectionPatterns.forEach(({ key, pattern }) => {
      const match = text.match(pattern)
      if (match) {
        sections[key] = match[1].trim()
      }
    })

    return sections
  }

  const sections = parseSections(rawResponse)

  const sectionsList = [
    {
      id: 'visual',
      title: 'Análise Visual',
      icon: Eye,
      content: sections.visual,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      id: 'audio',
      title: 'Análise de Áudio',
      icon: Volume2,
      content: sections.audio,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      id: 'temas',
      title: 'Temas e Mensagens',
      icon: MessageSquare,
      content: sections.temas,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      id: 'timestamps',
      title: 'Timestamps Importantes',
      icon: Clock,
      content: sections.timestamps,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
    {
      id: 'insights',
      title: 'Insights e Análise',
      icon: Lightbulb,
      content: sections.insights,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header with Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between"
      >
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Resultados da Análise</h2>
          <p className="text-gray-600 mt-1">Análise completa do vídeo usando IA</p>
        </div>

        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleDownload('txt')}
          >
            <FileText className="w-4 h-4 mr-2" />
            TXT
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleDownload('json')}
          >
            <Download className="w-4 h-4 mr-2" />
            JSON
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              // TODO: Implement share functionality
              toast({
                title: "Em breve",
                description: "Funcionalidade de compartilhamento em desenvolvimento",
                variant: "info",
              })
            }}
          >
            <Share2 className="w-4 h-4 mr-2" />
            Compartilhar
          </Button>
        </div>
      </motion.div>

      {/* Analysis Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <FileText className="w-5 h-5 text-blue-600" />
              <span>Informações da Análise</span>
            </CardTitle>
            <CardDescription>
              Detalhes técnicos da análise realizada
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <p className="font-medium text-gray-900">Tipo de Análise</p>
                <p className="text-gray-600 capitalize">{analysisType}</p>
              </div>
              <div>
                <p className="font-medium text-gray-900">Modelo IA</p>
                <p className="text-gray-600">{modelUsed}</p>
              </div>
              <div>
                <p className="font-medium text-gray-900">Tamanho do Arquivo</p>
                <p className="text-gray-600">{(fileSize / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Full Analysis */}
      {rawResponse && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Lightbulb className="w-5 h-5 text-yellow-600" />
                <span>Análise Completa</span>
              </CardTitle>
              <CardDescription>
                Análise detalhada gerada pela IA
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none">
                <div className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {rawResponse}
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                className="mt-4"
                onClick={() => handleCopyToClipboard(rawResponse, 'Análise Completa')}
              >
                <Copy className="w-4 h-4 mr-2" />
                Copiar Análise Completa
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Summary Card */}
      {sections.resumo && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="w-5 h-5 text-green-600" />
                <span>Resumo Geral</span>
              </CardTitle>
              <CardDescription>
                Principais insights e conclusões da análise
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none">
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {sections.resumo}
                </p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                className="mt-4"
                onClick={() => handleCopyToClipboard(sections.resumo, 'Resumo')}
              >
                <Copy className="w-4 h-4 mr-2" />
                Copiar Resumo
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Detailed Analysis Tabs */}
      {sectionsList.some(section => section.content) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-3 lg:grid-cols-5">
              {sectionsList.filter(section => section.content).map((section) => (
                <TabsTrigger key={section.id} value={section.id} className="text-xs">
                  <section.icon className="w-4 h-4 mr-1" />
                  <span className="hidden sm:inline">{section.title}</span>
                </TabsTrigger>
              ))}
            </TabsList>

            {sectionsList.filter(section => section.content).map((section) => (
              <TabsContent key={section.id} value={section.id}>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <div className={`w-8 h-8 ${section.bgColor} rounded-lg flex items-center justify-center`}>
                        <section.icon className={`w-5 h-5 ${section.color}`} />
                      </div>
                      <span>{section.title}</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="prose prose-sm max-w-none">
                        <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                          {section.content}
                        </p>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleCopyToClipboard(section.content!, section.title)}
                      >
                        <Copy className="w-4 h-4 mr-2" />
                        Copiar {section.title}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            ))}
          </Tabs>
        </motion.div>
      )}
    </div>
  )
}

export default AnalysisResults;
