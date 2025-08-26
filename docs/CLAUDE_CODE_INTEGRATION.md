# 🤖 Guia de Integração com Claude Code

Este guia mostra como integrar o Instagram Video Analyzer MCP Server com Claude Code para análise automatizada de vídeos do Instagram.

## 📋 Pré-requisitos

1. **Claude Code** instalado e configurado
2. **Instagram Video Analyzer API** rodando (localhost:8000)
3. **MCP Server** instalado e funcionando
4. **Node.js 18+** para gerenciamento de pacotes

## 🚀 Instalação Rápida

### Passo 1: Instalar o MCP Server

```bash
# Navegar para o diretório do MCP server
cd mcp-server

# Instalar dependências
uv sync

# Testar o servidor
uv run instagram-video-analyzer-mcp --help
```

### Passo 2: Configurar Claude Code

Adicione a configuração do MCP server no arquivo de configuração do Claude Code:

**Localização do arquivo de configuração**:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

**Conteúdo da configuração**:

```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "command": "uv",
      "args": ["run", "instagram-video-analyzer-mcp"],
      "cwd": "/caminho/para/mcp-server",
      "env": {
        "API_BASE_URL": "http://localhost:8000",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Passo 3: Reiniciar Claude Code

Após adicionar a configuração, reinicie o Claude Code para carregar o MCP server.

## 🎯 Comandos Disponíveis no Claude Code

### 1. Análise Completa de Vídeo

```bash
# Comando básico
claude analyze-instagram-video "https://www.instagram.com/reel/DMiEEmlMI7J/"

# Com tipo específico de análise
claude analyze-instagram-video "https://www.instagram.com/reel/DMiEEmlMI7J/" --type comprehensive

# Análise apenas de transcrição
claude analyze-instagram-video "https://www.instagram.com/reel/DMiEEmlMI7J/" --type transcription
```

### 2. Verificar Status de Job

```bash
claude get-job-status "uuid-do-job"
```

### 3. Listar Análises Recentes

```bash
# Listar últimas 10 análises
claude list-recent-analyses

# Listar com limite personalizado
claude list-recent-analyses --limit 20 --page 2
```

### 4. Obter Estatísticas do Sistema

```bash
claude get-system-stats
```

### 5. Cancelar Job

```bash
claude cancel-job "uuid-do-job"
```

## 💡 Exemplos Práticos de Uso

### Exemplo 1: Análise Básica

```bash
# Analisar um reel do Instagram
claude "Analise este vídeo do Instagram e me dê um resumo: https://www.instagram.com/reel/DMiEEmlMI7J/"
```

**Resposta esperada**:
```
🎬 Iniciando análise do vídeo...
✅ Análise concluída!

📊 Resumo da Análise:
- Tipo: Comprehensive
- Duração do processamento: 2m 30s
- Modelo usado: Gemini 2.5 Flash

📝 Principais Insights:
[Conteúdo da análise detalhada...]
```

### Exemplo 2: Análise em Lote

```bash
# Analisar múltiplos vídeos
claude "Analise estes vídeos do Instagram e compare os insights:
1. https://www.instagram.com/reel/video1/
2. https://www.instagram.com/reel/video2/
3. https://www.instagram.com/reel/video3/"
```

### Exemplo 3: Monitoramento de Jobs

```bash
# Verificar status de análises em andamento
claude "Mostre o status de todas as análises em andamento e as estatísticas do sistema"
```

### Exemplo 4: Análise Específica

```bash
# Solicitar apenas transcrição
claude "Faça apenas a transcrição deste vídeo: https://www.instagram.com/reel/DMiEEmlMI7J/"
```

## 🔧 Configurações Avançadas

### Configuração com Múltiplos Ambientes

```json
{
  "mcpServers": {
    "instagram-analyzer-dev": {
      "command": "uv",
      "args": ["run", "instagram-video-analyzer-mcp"],
      "cwd": "/caminho/para/mcp-server",
      "env": {
        "API_BASE_URL": "http://localhost:8000",
        "LOG_LEVEL": "DEBUG"
      }
    },
    "instagram-analyzer-prod": {
      "command": "uv",
      "args": ["run", "instagram-video-analyzer-mcp"],
      "cwd": "/caminho/para/mcp-server",
      "env": {
        "API_BASE_URL": "https://api.production.com",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Configuração com Docker

```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--network", "host",
        "instagram-video-analyzer-mcp:latest"
      ],
      "env": {
        "API_BASE_URL": "http://localhost:8000"
      }
    }
  }
}
```

## 🐛 Troubleshooting

### Problema: MCP Server não conecta

**Sintomas**: Claude Code não reconhece o servidor

**Soluções**:
1. Verificar se o caminho no `cwd` está correto
2. Testar o servidor manualmente: `uv run instagram-video-analyzer-mcp`
3. Verificar logs do Claude Code
4. Confirmar que a API está rodando: `curl http://localhost:8000/health`

### Problema: Timeout nas análises

**Sintomas**: Análises demoram muito ou falham

**Soluções**:
1. Aumentar timeout na configuração:
   ```json
   "env": {
     "REQUEST_TIMEOUT": "600"
   }
   ```
2. Verificar se a API não está sobrecarregada
3. Usar análises mais simples (`summary` ao invés de `comprehensive`)

### Problema: Erro de permissão

**Sintomas**: Erro ao executar o comando `uv`

**Soluções**:
1. Verificar se `uv` está no PATH
2. Usar caminho absoluto para `uv`:
   ```json
   "command": "/usr/local/bin/uv"
   ```
3. Verificar permissões do diretório

### Problema: API não responde

**Sintomas**: Erro de conexão com a API

**Soluções**:
1. Verificar se a API está rodando: `curl http://localhost:8000/health`
2. Verificar se a porta está correta
3. Verificar firewall/proxy
4. Testar com URL diferente na configuração

## 📊 Monitoramento e Logs

### Visualizar Logs do MCP Server

```bash
# Logs em tempo real
tail -f ~/.local/share/claude/logs/mcp-server.log

# Logs com filtro
grep "ERROR" ~/.local/share/claude/logs/mcp-server.log
```

### Verificar Status da Conexão

```bash
# No Claude Code, execute:
claude "Verifique o status da conexão com o servidor de análise de vídeos"
```

### Estatísticas de Uso

```bash
# Obter métricas de performance
claude "Mostre as estatísticas de uso do sistema de análise de vídeos"
```

## 🎯 Melhores Práticas

### 1. Uso Eficiente

- Use `summary` para análises rápidas
- Use `comprehensive` apenas quando necessário
- Monitore o uso de tokens da API Gemini
- Cancele jobs desnecessários

### 2. Organização

- Mantenha um log das análises importantes
- Use nomes descritivos ao salvar resultados
- Organize análises por projeto/campanha

### 3. Performance

- Evite analisar vídeos muito longos
- Use análises em lote para eficiência
- Configure timeouts apropriados

### 4. Segurança

- Não compartilhe URLs privadas
- Mantenha logs seguros
- Use HTTPS em produção

## 🔄 Atualizações

### Atualizar o MCP Server

```bash
cd mcp-server
git pull origin main
uv sync
```

### Verificar Versão

```bash
claude "Qual é a versão atual do servidor de análise de vídeos?"
```

## 📚 Recursos Adicionais

- **Documentação da API**: [README da API](../README.md)
- **Exemplos de Código**: [Pasta examples/](../examples/)
- **Issues e Suporte**: [GitHub Issues](https://github.com/your-org/instagram-video-analyzer-mcp/issues)
- **Claude Code Docs**: [Documentação Oficial](https://docs.anthropic.com/en/docs/claude-code/overview)

## 🤝 Contribuição

Para contribuir com melhorias na integração:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Teste com Claude Code
4. Submeta um Pull Request

---

**💡 Dica**: Para melhor experiência, mantenha sempre a API e o MCP server atualizados!
