# 🎯 Guia Completo dos Templates VibeKanban

Este guia mostra como usar os templates VibeKanban para automatizar análises de vídeos do Instagram com Claude Code e o MCP Server.

## 📋 Visão Geral dos Templates

### 1. **Análise de Vídeo Instagram** (`analise-video-instagram.yml`)
- **Propósito**: Análise individual de vídeos
- **Duração**: 5-10 minutos
- **Ideal para**: Análises pontuais, testes, validação de conteúdo

### 2. **Análise em Lote** (`analise-lote-videos.yml`)
- **Propósito**: Análise comparativa de múltiplos vídeos
- **Duração**: 15-30 minutos
- **Ideal para**: Pesquisa de mercado, análise de concorrentes, campanhas

### 3. **Monitoramento Contínuo** (`monitoramento-continuo.yml`)
- **Propósito**: Monitoramento automático e alertas
- **Duração**: Contínuo
- **Ideal para**: Vigilância competitiva, detecção de tendências

## 🚀 Instalação e Configuração

### Pré-requisitos

1. **VibeKanban** instalado e configurado
2. **Claude Code** com MCP server configurado
3. **Instagram Video Analyzer API** rodando
4. **Node.js 18+** para VibeKanban

### Instalação do VibeKanban

```bash
# Instalar VibeKanban
npm install -g @bloop/vibe-kanban

# Verificar instalação
vibe-kanban --version

# Inicializar projeto
vibe-kanban init instagram-analysis
cd instagram-analysis
```

### Configuração dos Templates

```bash
# Copiar templates para o projeto
cp vibekanban-templates/*.yml ./templates/

# Verificar templates
vibe-kanban list-templates
```

## 🎬 Template 1: Análise de Vídeo Instagram

### Uso Básico

```bash
# Executar análise simples
vibe-kanban run analise-video-instagram \
  --video_url "https://www.instagram.com/reel/DMiEEmlMI7J/" \
  --analysis_type "comprehensive" \
  --project_name "Análise Reel Marketing"
```

### Parâmetros Disponíveis

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `video_url` | string | ✅ | URL do vídeo do Instagram |
| `analysis_type` | select | ❌ | Tipo de análise (comprehensive, summary, transcription, visual_description) |
| `project_name` | string | ❌ | Nome do projeto |
| `output_format` | select | ❌ | Formato de saída (markdown, json, txt) |

### Exemplo Avançado

```bash
vibe-kanban run analise-video-instagram \
  --video_url "https://www.instagram.com/reel/DMiEEmlMI7J/" \
  --analysis_type "comprehensive" \
  --project_name "Campanha Verão 2024" \
  --output_format "markdown" \
  --notify-slack \
  --save-artifacts
```

### Saídas Geradas

- `relatorio_principal.md`: Relatório completo
- `conteudo_redes_sociais.md`: Conteúdo para redes sociais
- `dados_tecnicos.json`: Dados técnicos da análise
- `insights_principais.txt`: Resumo dos insights

## 📊 Template 2: Análise em Lote

### Uso Básico

```bash
# Preparar arquivo com URLs
cat > videos.txt << EOF
https://www.instagram.com/reel/video1/
https://www.instagram.com/reel/video2/
https://www.instagram.com/reel/video3/
EOF

# Executar análise em lote
vibe-kanban run analise-lote-videos \
  --video_urls "$(cat videos.txt)" \
  --project_name "Análise Concorrentes Q1" \
  --analysis_focus "content_strategy"
```

### Parâmetros Avançados

```bash
vibe-kanban run analise-lote-videos \
  --video_urls "$(cat videos.txt)" \
  --project_name "Pesquisa Mercado" \
  --analysis_focus "comprehensive" \
  --comparison_criteria "themes,visual_style,engagement" \
  --max_concurrent_videos 3 \
  --retry_failed_videos true
```

### Saídas Geradas

- `analise_comparativa.md`: Relatório comparativo
- `dashboard.html`: Dashboard interativo
- `resumo_executivo.md`: Resumo para stakeholders
- `dados_comparativos.json`: Dados estruturados

## 🔄 Template 3: Monitoramento Contínuo

### Configuração Inicial

```bash
# Configurar contas para monitorar
cat > contas.txt << EOF
@nike
@adidas
@puma
@underarmour
EOF

# Configurar monitoramento
vibe-kanban run monitoramento-continuo \
  --target_accounts "$(cat contas.txt)" \
  --monitoring_frequency "daily" \
  --analysis_triggers "new_video,high_engagement" \
  --report_frequency "weekly"
```

### Configuração de Alertas

```yaml
# alerts_config.yml
alert_thresholds:
  engagement_rate: 5.0
  view_count: 10000
  comment_rate: 2.0

notification_channels:
  slack:
    webhook_url: "https://hooks.slack.com/..."
    channel: "#marketing-alerts"
  
  email:
    smtp_server: "smtp.gmail.com"
    recipients: ["team@company.com"]
```

### Executar com Configuração

```bash
vibe-kanban run monitoramento-continuo \
  --config alerts_config.yml \
  --target_accounts "$(cat contas.txt)" \
  --monitoring_frequency "hourly"
```

## 🔧 Configurações Avançadas

### Configuração Global do VibeKanban

```yaml
# vibe-kanban.config.yml
project:
  name: "Instagram Analysis Suite"
  version: "1.0.0"

agents:
  claude-code:
    model: "claude-3-5-sonnet"
    max_tokens: 4000
    temperature: 0.1

mcp_servers:
  instagram-video-analyzer:
    endpoint: "http://localhost:8000"
    timeout: 300

notifications:
  slack:
    default_channel: "#ai-analysis"
    webhook_url: "${SLACK_WEBHOOK_URL}"
  
  email:
    smtp_server: "smtp.gmail.com"
    from: "ai-analysis@company.com"

storage:
  artifacts_path: "./artifacts"
  max_retention_days: 90
  compress_old_files: true

monitoring:
  health_check_interval: "5min"
  log_level: "INFO"
  metrics_enabled: true
```

### Variáveis de Ambiente

```bash
# .env
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
EMAIL_PASSWORD="app_password"
INSTAGRAM_API_URL="http://localhost:8000"
CLAUDE_API_KEY="sk-ant-..."
MCP_SERVER_PATH="/path/to/mcp-server"
```

## 📊 Monitoramento e Métricas

### Dashboard de Métricas

```bash
# Visualizar métricas em tempo real
vibe-kanban dashboard --port 3000

# Acessar em: http://localhost:3000
```

### Métricas Coletadas

- **Performance**: Tempo de execução, taxa de sucesso
- **Qualidade**: Número de insights, precisão das análises
- **Uso**: Vídeos analisados, templates executados
- **Alertas**: Alertas gerados, tempo de resposta

### Exportar Métricas

```bash
# Exportar métricas para análise
vibe-kanban export-metrics \
  --format json \
  --period "last_30_days" \
  --output metrics_report.json
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Template não encontrado
```bash
# Verificar templates disponíveis
vibe-kanban list-templates

# Verificar sintaxe do template
vibe-kanban validate-template analise-video-instagram.yml
```

#### 2. MCP Server não responde
```bash
# Verificar status do MCP server
curl http://localhost:8000/health

# Verificar logs do VibeKanban
vibe-kanban logs --follow
```

#### 3. Análise falha
```bash
# Verificar logs detalhados
vibe-kanban logs --task analyze_video --verbose

# Reexecutar com debug
vibe-kanban run analise-video-instagram \
  --video_url "..." \
  --debug \
  --verbose
```

### Logs e Debugging

```bash
# Logs em tempo real
vibe-kanban logs --follow --level DEBUG

# Logs de um template específico
vibe-kanban logs --template analise-video-instagram

# Logs de uma execução específica
vibe-kanban logs --run-id "run_123456"
```

## 🔄 Automação e CI/CD

### GitHub Actions

```yaml
# .github/workflows/video-analysis.yml
name: Análise Automática de Vídeos

on:
  schedule:
    - cron: '0 9 * * *'  # Diariamente às 9h
  workflow_dispatch:

jobs:
  analyze-videos:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
    
    - name: Install VibeKanban
      run: npm install -g @bloop/vibe-kanban
    
    - name: Run Daily Analysis
      run: |
        vibe-kanban run monitoramento-continuo \
          --target_accounts "${{ secrets.TARGET_ACCOUNTS }}" \
          --monitoring_frequency "daily"
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        CLAUDE_API_KEY: ${{ secrets.CLAUDE_API_KEY }}
```

### Cron Jobs

```bash
# Adicionar ao crontab
crontab -e

# Monitoramento a cada 4 horas
0 */4 * * * cd /path/to/project && vibe-kanban run monitoramento-continuo

# Relatório semanal às segundas 9h
0 9 * * 1 cd /path/to/project && vibe-kanban run analise-lote-videos --weekly-report
```

## 📚 Exemplos Práticos

### Caso 1: Análise de Campanha

```bash
# 1. Analisar vídeo principal da campanha
vibe-kanban run analise-video-instagram \
  --video_url "https://instagram.com/reel/campanha_principal/" \
  --project_name "Campanha Black Friday"

# 2. Analisar concorrentes
vibe-kanban run analise-lote-videos \
  --video_urls "$(cat concorrentes_urls.txt)" \
  --project_name "Análise Concorrentes Black Friday"

# 3. Monitorar reações
vibe-kanban run monitoramento-continuo \
  --target_accounts "@nossa_marca,@concorrente1,@concorrente2" \
  --monitoring_frequency "hourly"
```

### Caso 2: Pesquisa de Mercado

```bash
# Análise de tendências do setor
vibe-kanban run analise-lote-videos \
  --video_urls "$(cat trending_videos.txt)" \
  --analysis_focus "visual_trends" \
  --comparison_criteria "themes,visual_style,production_quality"
```

### Caso 3: Monitoramento de Crise

```bash
# Monitoramento intensivo durante crise
vibe-kanban run monitoramento-continuo \
  --target_accounts "@nossa_marca" \
  --monitoring_frequency "hourly" \
  --analysis_triggers "new_video,high_engagement,trending_hashtag" \
  --alert_thresholds '{"engagement_rate": 2.0, "comment_rate": 5.0}'
```

## 🤝 Contribuição e Customização

### Criar Template Personalizado

```yaml
# meu-template.yml
name: "Meu Template Personalizado"
description: "Template customizado para necessidades específicas"

variables:
  - name: "custom_param"
    description: "Parâmetro personalizado"
    type: "string"

tasks:
  - id: "custom_task"
    name: "Tarefa Personalizada"
    agent: "claude-code"
    prompt: |
      Execute tarefa personalizada com {{custom_param}}
```

### Validar Template

```bash
vibe-kanban validate-template meu-template.yml
```

### Compartilhar Template

```bash
# Publicar no registry
vibe-kanban publish-template meu-template.yml

# Instalar template de terceiros
vibe-kanban install-template @user/template-name
```

---

**💡 Dica**: Comece com o template básico e vá evoluindo conforme suas necessidades. Os templates são totalmente customizáveis!
