# Instagram Video Analyzer MCP Server

Um servidor MCP (Model Context Protocol) completo para análise de vídeos do Instagram usando inteligência artificial.

## 🎯 Visão Geral

Este servidor MCP permite que LLMs (como Claude) analisem vídeos do Instagram de forma inteligente, fornecendo:

- **Análise Completa**: Transcrição, análise visual, temas, insights
- **Múltiplos Tipos**: Comprehensive, summary, transcription, visual_description
- **Processamento Assíncrono**: Jobs com monitoramento em tempo real
- **Recursos Dinâmicos**: Acesso a resultados e estatísticas
- **Logging Inteligente**: Logs estruturados para debugging

## 🛠️ Instalação

### Pré-requisitos

- Python 3.11+
- Instagram Video Analyzer API rodando (localhost:8000)
- uv ou pip para gerenciamento de dependências

### Instalação via uv (Recomendado)

```bash
# Clonar ou baixar os arquivos
cd mcp-server

# Instalar dependências
uv sync

# Executar servidor
uv run instagram-video-analyzer-mcp
```

### Instalação via pip

```bash
cd mcp-server
pip install -e .
python instagram_video_analyzer_mcp.py
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# URL da API (padrão: http://localhost:8000)
export API_BASE_URL="http://localhost:8000"

# Timeout para requisições (padrão: 300 segundos)
export REQUEST_TIMEOUT="300"

# Nível de log (padrão: INFO)
export LOG_LEVEL="INFO"
```

### Verificar Conectividade

```bash
# Testar se a API está respondendo
curl http://localhost:8000/health

# Resposta esperada:
# {"status": "healthy", "timestamp": "..."}
```

## 🎬 Ferramentas Disponíveis

### 1. `analyze_instagram_video`

**Descrição**: Analisa um vídeo do Instagram usando IA

**Parâmetros**:
- `url` (string, obrigatório): URL do vídeo do Instagram
- `analysis_type` (string, opcional): Tipo de análise
  - `comprehensive` (padrão): Análise completa
  - `summary`: Resumo conciso
  - `transcription`: Transcrição do áudio
  - `visual_description`: Descrição visual

**Exemplo de Uso**:
```python
result = await session.call_tool("analyze_instagram_video", {
    "url": "https://www.instagram.com/reel/DMiEEmlMI7J/",
    "analysis_type": "comprehensive"
})
```

**Retorno**:
```json
{
  "success": true,
  "job_id": "uuid-do-job",
  "status": "completed",
  "analysis": {
    "analysis_type": "comprehensive",
    "model_used": "gemini-2.5-flash",
    "raw_response": "Análise detalhada...",
    "file_size": 19058688
  }
}
```

### 2. `get_job_status`

**Descrição**: Verifica o status de um job de análise

**Parâmetros**:
- `job_id` (string, obrigatório): ID do job

**Exemplo de Uso**:
```python
status = await session.call_tool("get_job_status", {
    "job_id": "uuid-do-job"
})
```

**Retorno**:
```json
{
  "job_id": "uuid-do-job",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:32:30Z",
  "analysis_result": { ... }
}
```

### 3. `list_recent_analyses`

**Descrição**: Lista análises recentes

**Parâmetros**:
- `limit` (int, opcional): Número máximo de resultados (padrão: 10)
- `page` (int, opcional): Página para paginação (padrão: 1)

**Exemplo de Uso**:
```python
analyses = await session.call_tool("list_recent_analyses", {
    "limit": 5,
    "page": 1
})
```

### 4. `cancel_job`

**Descrição**: Cancela um job em andamento

**Parâmetros**:
- `job_id` (string, obrigatório): ID do job a cancelar

**Exemplo de Uso**:
```python
result = await session.call_tool("cancel_job", {
    "job_id": "uuid-do-job"
})
```

### 5. `get_system_stats`

**Descrição**: Obtém estatísticas do sistema

**Parâmetros**: Nenhum

**Exemplo de Uso**:
```python
stats = await session.call_tool("get_system_stats", {})
```

**Retorno**:
```json
{
  "total_jobs": 150,
  "completed_jobs": 142,
  "failed_jobs": 3,
  "pending_jobs": 5,
  "success_rate": 94.67,
  "average_processing_time": 125.5
}
```

### 6. `get_video_info`

**Descrição**: Obtém informações básicas de um vídeo

**Parâmetros**:
- `url` (string, obrigatório): URL do vídeo do Instagram

**Exemplo de Uso**:
```python
info = await session.call_tool("get_video_info", {
    "url": "https://www.instagram.com/reel/DMiEEmlMI7J/"
})
```

## 📚 Recursos Disponíveis

### 1. `analysis://{job_id}`

**Descrição**: Resultado de uma análise específica

**Exemplo**:
```python
content = await session.read_resource("analysis://uuid-do-job")
```

### 2. `jobs://recent`

**Descrição**: Lista de jobs recentes

**Exemplo**:
```python
jobs = await session.read_resource("jobs://recent")
```

### 3. `stats://system`

**Descrição**: Estatísticas do sistema

**Exemplo**:
```python
stats = await session.read_resource("stats://system")
```

## 🚀 Execução

### Modo Stdio (Para Claude Desktop)

```bash
uv run instagram-video-analyzer-mcp
```

### Modo SSE (Para desenvolvimento)

```bash
uv run instagram-video-analyzer-mcp --transport sse --port 8001
```

### Modo HTTP Streamable

```bash
uv run instagram-video-analyzer-mcp --transport streamable-http --port 8001
```

## 🔍 Debugging

### Logs Estruturados

O servidor produz logs estruturados para facilitar o debugging:

```
2024-01-15 10:30:00 INFO 🚀 Iniciando Instagram Video Analyzer MCP Server...
2024-01-15 10:30:01 INFO ✅ Conexão com API estabelecida
2024-01-15 10:30:15 INFO 🎬 Iniciando análise de vídeo: https://instagram.com/reel/...
2024-01-15 10:30:16 INFO ✅ Job criado com sucesso: uuid-do-job
2024-01-15 10:30:16 INFO ⏳ Aguardando conclusão da análise...
2024-01-15 10:32:30 INFO 🎉 Análise concluída com sucesso!
```

### Verificar Status da API

```bash
# Verificar se a API está rodando
curl http://localhost:8000/health

# Listar jobs recentes
curl http://localhost:8000/api/jobs

# Verificar status de um job específico
curl http://localhost:8000/api/video/status/uuid-do-job
```

## ⚠️ Tratamento de Erros

O servidor trata diversos tipos de erro:

- **URL Inválida**: Valida se a URL é do Instagram
- **Tipo de Análise Inválido**: Verifica tipos suportados
- **Timeout**: Limite de 5 minutos por análise
- **Falha na API**: Retorna erros estruturados
- **Conexão Perdida**: Reconecta automaticamente

## 📊 Monitoramento

### Métricas Disponíveis

- Total de jobs processados
- Taxa de sucesso
- Tempo médio de processamento
- Jobs pendentes/em andamento
- Estatísticas de erro

### Health Check

```bash
curl http://localhost:8000/health
```

## 🔧 Desenvolvimento

### Executar Testes

```bash
uv run pytest
```

### Linting e Formatação

```bash
# Formatação com black
uv run black .

# Linting com ruff
uv run ruff check .

# Type checking com mypy
uv run mypy .
```

### Estrutura do Projeto

```
mcp-server/
├── instagram_video_analyzer_mcp.py  # Servidor principal
├── pyproject.toml                   # Configuração do projeto
├── README.md                        # Esta documentação
├── tests/                          # Testes
└── examples/                       # Exemplos de uso
```

## 📝 Licença

MIT License - veja o arquivo LICENSE para detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/your-org/instagram-video-analyzer-mcp/issues)
- **Documentação**: [README](https://github.com/your-org/instagram-video-analyzer-mcp#readme)
- **API Reference**: Veja a documentação da API principal
