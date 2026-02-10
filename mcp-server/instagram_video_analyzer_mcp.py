#!/usr/bin/env python3
"""
Instagram Video Analyzer MCP Server

Servidor MCP para análise de vídeos usando IA (Google Gemini).
Suporta vídeos do Instagram (via backend API) e arquivos locais (via Gemini direto).

Ferramentas disponíveis:
- analyze_instagram_video: Análise de vídeo do Instagram (via backend)
- analyze_local_video: Análise de vídeo local (via Gemini direto, até 2GB)
- get_video_info: Informações básicas do vídeo
- get_job_status: Status de um job de análise
- list_recent_analyses: Lista análises recentes
- cancel_job: Cancela um job em andamento
- get_system_stats: Estatísticas do sistema

Recursos disponíveis:
- analysis://{job_id}: Resultado de uma análise específica
- jobs://recent: Lista de jobs recentes
- stats://system: Estatísticas do sistema
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import httpx
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.models import InitializationOptions

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações do servidor
import os
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5177")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
REQUEST_TIMEOUT = 300.0  # 5 minutos
MAX_RETRIES = 3

# Tipos de análise válidos
VALID_ANALYSIS_TYPES = [
    "comprehensive",
    "summary",
    "transcription",
    "visual_description",
    "project_management",
    "candidate_skills",
]

# ============================================================================
# PROMPTS DE ANÁLISE
# ============================================================================

ANALYSIS_PROMPTS = {
    "comprehensive": """
        Analise este vídeo de forma abrangente e forneça:

        1. **Resumo Geral**: Descreva o conteúdo principal do vídeo em 2-3 frases

        2. **Análise Visual**:
           - Descrição das cenas principais
           - Objetos, pessoas ou elementos visuais importantes
           - Qualidade e estilo visual

        3. **Análise de Áudio**:
           - Transcrição de falas ou narração (se houver)
           - Música de fundo ou efeitos sonoros
           - Tom e emoção do áudio

        4. **Temas e Mensagens**:
           - Temas principais abordados
           - Mensagem ou propósito do vídeo
           - Público-alvo aparente

        5. **Timestamps Importantes**:
           - Momentos-chave com timestamps (formato MM:SS)
           - Mudanças significativas de cena ou tópico

        6. **Insights e Análise**:
           - Contexto cultural ou social
           - Técnicas de produção notáveis
           - Impacto emocional ou persuasivo

        Formate sua resposta de forma clara e estruturada em português.
    """,

    "summary": """
        Forneça um resumo conciso deste vídeo incluindo:
        1. Descrição do conteúdo principal (2-3 frases)
        2. Principais pontos ou mensagens
        3. Duração aproximada e qualidade visual
        4. Público-alvo sugerido

        Responda em português de forma clara e objetiva.
    """,

    "transcription": """
        Transcreva todo o áudio deste vídeo, incluindo:
        1. Falas e narração completas
        2. Timestamps para cada segmento (formato MM:SS)
        3. Descrição de música de fundo ou efeitos sonoros
        4. Indicação de pausas ou mudanças de tom

        Formate como uma transcrição profissional em português.
    """,

    "visual_description": """
        Descreva detalhadamente os elementos visuais deste vídeo:
        1. Descrição de cada cena principal com timestamps (MM:SS)
        2. Pessoas, objetos e cenários
        3. Telas, dashboards, interfaces ou software mostrados
        4. Textos, diagramas ou gráficos visíveis
        5. Ações e interações entre participantes
        6. Qualidade e estilo visual da gravação

        Seja específico e detalhado na descrição visual. Responda em português.
    """,

    "project_management": """
        Você é um especialista em gestão de projetos técnicos. Analise este vídeo de reunião
        e extraia TODAS as informações relevantes para gestão de projetos de software/aplicações.

        Forneça sua análise nas seguintes seções obrigatórias:

        ## 1. CONTEXTO DA REUNIÃO
        - Participantes (nomes, papéis/funções)
        - Data e duração
        - Objetivo principal da reunião
        - Tipo: kickoff, sprint planning, review, daily, brainstorm, técnica, etc.

        ## 2. DECISÕES TOMADAS
        Para cada decisão identificada:
        - [DECISÃO]: Descrição clara da decisão
        - [TIMESTAMP]: Momento no vídeo (MM:SS)
        - [RESPONSÁVEL]: Quem tomou ou propôs a decisão
        - [IMPACTO]: Alto/Médio/Baixo

        ## 3. ACTION ITEMS / TAREFAS
        Para cada tarefa identificada:
        - [TAREFA]: Descrição clara e acionável
        - [RESPONSÁVEL]: Quem deve executar
        - [PRAZO]: Se mencionado, ou "Não definido"
        - [PRIORIDADE]: Alta/Média/Baixa
        - [DEPENDÊNCIAS]: Outras tarefas ou recursos necessários
        - [TIMESTAMP]: Momento no vídeo onde foi discutida

        ## 4. REQUISITOS TÉCNICOS
        Para cada requisito identificado:
        - [REQ]: Descrição do requisito
        - [TIPO]: Funcional / Não-funcional / Infraestrutura / Integração
        - [STACK/TECNOLOGIAS]: Tecnologias mencionadas
        - [COMPLEXIDADE]: Alta/Média/Baixa

        ## 5. ARQUITETURA E INFRAESTRUTURA
        - Sistemas, plataformas e ferramentas mencionados
        - Integrações necessárias
        - Ambientes (dev, staging, prod)
        - Custos ou estimativas mencionados
        - Diagramas ou fluxos descritos

        ## 6. RISCOS E BLOQUEIOS
        - Riscos identificados durante a discussão
        - Bloqueios atuais mencionados
        - Dependências externas
        - Preocupações levantadas pelos participantes

        ## 7. MODELO DE NEGÓCIO / ESCOPO DO PROJETO
        - Escopo do projeto discutido
        - Modelo de negócio (se mencionado): SaaS, licença, contrato, etc.
        - Público-alvo / stakeholders
        - Métricas de sucesso ou KPIs mencionados
        - Estimativas de custo ou valor

        ## 8. PRÓXIMOS PASSOS
        - Ações imediatas acordadas
        - Próxima reunião ou checkpoint
        - Entregas esperadas
        - Pontos em aberto que precisam de resolução

        ## 9. RESUMO EXECUTIVO
        - Resumo de 3-5 frases com os pontos mais importantes
        - Status geral do projeto: Início / Em andamento / Em risco / Concluído

        REGRAS:
        - Extraia APENAS informações explicitamente mencionadas no vídeo
        - Use timestamps precisos (MM:SS) sempre que possível
        - Se algo não foi discutido, indique "Não abordado nesta reunião"
        - Priorize informações acionáveis sobre discussões genéricas
        - Identifique compromissos verbais como action items
        - Formate em Markdown limpo e estruturado
        - Responda em Português (Brasil)
    """,

    "candidate_skills": """
You are the Vibecoder Skills Extraction Agent. Your role is to analyze meeting recordings where a candidate discusses technology, projects, architecture, and workflows, and extract a structured professional profile.

## CORE RULES

1. **Evidence-Based Only**: Every skill assessment MUST be backed by direct quotes from the source material. Never infer skills without evidence.
2. **Quote in Portuguese**: When providing evidence for any claim, quote the original Portuguese text verbatim with timestamps.
3. **Output in English**: All analysis, assessments, and commentary must be in English.
4. **Score Honestly**: Use the full 0-100 scale. A score of 50 means intermediate, not bad. A score of 0 means no evidence found.
5. **Identify Self-Declarations**: Distinguish between skills the candidate DEMONSTRATES vs skills they CLAIM to have. Flag discrepancies.
6. **Capture Weaknesses**: Explicitly note self-declared limitations — these are as valuable as strengths for proper placement.

## ANALYSIS FRAMEWORK

### Step 1: Context Extraction
- Meeting participants and their roles
- Duration and setting
- Primary topics discussed
- Candidate's age, background, community presence

### Step 2: Skill Identification
Scan the entire conversation for evidence of knowledge in these categories:

**Tier A — Automation & Workflow**
- N8N (workflow design, optimization, scaling, error handling, function nodes, edit fields, webhooks)
- Make/Integromat, Zapier, Custom automation scripts

**Tier B — Database & Backend**
- Supabase (tables, RLS, auth, edge functions, multi-tenancy)
- Firebase, PostgreSQL / MySQL, API design and integration, Multi-tenant architecture patterns

**Tier C — AI & LLM**
- Prompt engineering (quality, optimization, hallucination awareness)
- Model selection (knowing when to use which model)
- RAG / Embeddings / Vectorization, Transcription & diarization, Vision / multimodal AI, Local model deployment

**Tier D — Frontend & App Building**
- IDE Vibe Coding (Claude Code, Cursor, Windsurf, Replit)
- Low-Code (Lovable, Bolt, v0), React / Next.js / Vue, UI/UX design sense

**Tier E — DevOps & Infrastructure**
- VPS management, Docker / containers, CI/CD pipelines, Domain management / DNS, SSL / security

**Tier F — Business & Strategy**
- SaaS business models, Pricing strategy, Client management, Project scoping, Market awareness

**Tier G — Communication & Teaching**
- Content creation (video, audio, written), Community leadership, Mentoring / training, Presentation skills

**Tier H — Equipment & Platform Capability**
- Primary OS (macOS / Windows / Linux), Hardware specs (RAM, CPU, GPU), Mobile devices (iOS / Android)
- Development environment maturity, Local AI capability, Network/Server access

### Step 3: Scoring Methodology

| Score Range | Level | Criteria |
|-------------|-------|----------|
| 90-100 | Expert | Teaches others, identifies advanced patterns, provides corrections to experienced practitioners |
| 75-89 | Advanced | Comfortable discussing architecture, knows tradeoffs, has built production-level work |
| 50-74 | Intermediate | Can use the technology, understands basics, has built MVPs or training projects |
| 25-49 | Beginner | Self-declared learner, limited practical examples, asks for help |
| 0-24 | No Evidence | Not discussed or demonstrated in the conversation |

Scoring Rules:
- Self-declaration alone without demonstration = max 60
- Active demonstration (correcting someone, suggesting improvements) = up to 100
- Having built projects with the technology = +10 bonus
- Teaching others the technology = +10 bonus
- Acknowledging limitations = indicates honesty, does NOT lower score

### Step 4: Complementarity Assessment
If there are multiple participants, assess how their skills complement each other. Create a comparison matrix.

### Step 5: Project Catalog
List every project, tool, or system the candidate mentions:
- Project name/description, Tech stack used, Current status (idea / MVP / production / abandoned), Complexity level (1-5)

### Step 6: Growth Areas
Based on self-declared weaknesses AND gaps in the skill matrix, recommend:
- Top 3 skills to develop, Suggested resources or learning paths, Complementary team members they would benefit from

### Step 7: Cultural Fit Indicators
Extract behavioral signals:
- Collaborative vs solo preference, Teaching vs learning orientation, Risk tolerance
- Cost consciousness, Vision vs execution orientation, Communication style

## OUTPUT FORMAT

Use Markdown headers, bullet points, and blockquotes. Do NOT use wide tables — use bullet lists or narrow 3-column tables max.

# Vibecoder Candidate Profile: [Name]

## Analysis Metadata
- List: source, duration, interviewer, date

## 1. CANDIDATE OVERVIEW
- Use bullet points for: Name, Age, Primary Strengths, Self-Declared Weaknesses, Community Presence, Current Role

## 2. SKILL ASSESSMENT MATRIX
- Group by tier (Expert 90-100, Advanced 75-89, Intermediate 50-74, Beginner 25-49, No Evidence 0-24)
- For each skill: name, score, 2-3 sentence assessment, then quote evidence as blockquotes with timestamps

## 3. UNIQUE VALUE PROPOSITION
- 1-2 paragraphs

## 4. COMPLEMENTARITY ASSESSMENT
- Use bullet list comparison between participants

## 5. PROJECTS MENTIONED
- Use bullet list: project name, description, tech stack, status

## 6. GROWTH AREAS AND RECOMMENDATIONS
- Numbered list

## 7. CULTURAL FIT INDICATORS
- Bullet points

## 8. EQUIPMENT AND PLATFORM PROFILE
- Bullet points for: OS, hardware, devices, local AI capability

## IMPORTANT NOTES
- If the meeting is informal, the candidate will reveal more authentic skill levels. Weight DEMONSTRATIONS over CLAIMS.
- Pay special attention to moments where the candidate CORRECTS the interviewer — strongest signal of expertise.
- When the candidate says "I don't know X" or "I'm not good at Y", record this as valuable data, not a negative.
- Look for "unconscious competence" signals: when someone uses advanced terminology naturally without explaining it.
    """,
}

# Modelos Pydantic para validação
class AnalysisRequest(BaseModel):
    """Modelo para requisição de análise"""
    url: str = Field(description="URL do vídeo do Instagram")
    analysis_type: str = Field(
        default="comprehensive",
        description="Tipo de análise: comprehensive, summary, transcription, visual_description"
    )

class JobStatusResponse(BaseModel):
    """Modelo para resposta de status do job"""
    job_id: str
    status: str
    progress: int
    created_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    analysis_result: Optional[Dict[str, Any]] = None

class SystemStats(BaseModel):
    """Modelo para estatísticas do sistema"""
    total_jobs: int
    completed_jobs: int
    failed_jobs: int
    pending_jobs: int
    success_rate: float
    average_processing_time: Optional[float] = None

# Cliente HTTP global
http_client: Optional[httpx.AsyncClient] = None

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Gerencia o ciclo de vida da aplicação"""
    global http_client
    
    # Inicialização
    logger.info("🚀 Iniciando Instagram Video Analyzer MCP Server...")
    http_client = httpx.AsyncClient(
        base_url=API_BASE_URL,
        timeout=httpx.Timeout(REQUEST_TIMEOUT),
        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
    )
    
    # Verificar se a API está disponível
    try:
        response = await http_client.get("/health")
        if response.status_code == 200:
            logger.info("✅ Conexão com API estabelecida")
        else:
            logger.warning(f"⚠️ API respondeu com status {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com API: {e}")
    
    try:
        yield {"http_client": http_client}
    finally:
        # Limpeza
        logger.info("🔄 Encerrando Instagram Video Analyzer MCP Server...")
        if http_client:
            await http_client.aclose()
        logger.info("✅ Servidor encerrado com sucesso")

# Criar servidor MCP
mcp = FastMCP(
    name="Instagram Video Analyzer",
    lifespan=app_lifespan
)

# ============================================================================
# FERRAMENTAS (TOOLS)
# ============================================================================

@mcp.tool()
async def analyze_instagram_video(
    url: str,
    analysis_type: str = "comprehensive",
    *,
    ctx: Context
) -> Dict[str, Any]:
    """
    Analisa um vídeo do Instagram usando IA.
    
    Args:
        url: URL do vídeo do Instagram (reel, IGTV, ou post com vídeo)
        analysis_type: Tipo de análise - comprehensive, summary, transcription, visual_description
        
    Returns:
        Resultado da análise com job_id e status
    """
    await ctx.info(f"🎬 Iniciando análise de vídeo: {url}")

    # Validar tipo de análise
    if analysis_type not in VALID_ANALYSIS_TYPES:
        await ctx.error(f"Tipo de análise inválido: {analysis_type}")
        raise ValueError(f"Tipo de análise deve ser um de: {', '.join(VALID_ANALYSIS_TYPES)}")
    
    # Validar URL do Instagram
    if not any(domain in url for domain in ["instagram.com", "instagr.am"]):
        await ctx.error("URL não é do Instagram")
        raise ValueError("URL deve ser do Instagram")
    
    try:
        # Fazer requisição para API
        payload = {
            "instagram_url": url,
            "analysis_type": analysis_type
        }
        
        response = await http_client.post("/api/video/analyze", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            job_id = result.get("job_id")
            
            await ctx.info(f"✅ Job criado com sucesso: {job_id}")
            
            # Aguardar conclusão da análise
            await ctx.info("⏳ Aguardando conclusão da análise...")
            final_result = await _wait_for_completion(job_id, ctx)
            
            return {
                "success": True,
                "job_id": job_id,
                "status": "completed",
                "analysis": final_result
            }
        else:
            error_msg = f"Erro na API: {response.status_code} - {response.text}"
            await ctx.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
            
    except Exception as e:
        error_msg = f"Erro ao processar análise: {str(e)}"
        await ctx.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

@mcp.tool()
async def get_job_status(job_id: str, *, ctx: Context) -> Dict[str, Any]:
    """
    Verifica o status de um job de análise.
    
    Args:
        job_id: ID do job de análise
        
    Returns:
        Status atual do job
    """
    await ctx.debug(f"🔍 Verificando status do job: {job_id}")
    
    try:
        response = await http_client.get(f"/api/video/status/{job_id}")
        
        if response.status_code == 200:
            result = response.json()
            await ctx.debug(f"Status obtido: {result.get('status')}")
            return result
        else:
            error_msg = f"Erro ao obter status: {response.status_code}"
            await ctx.error(error_msg)
            return {"error": error_msg}
            
    except Exception as e:
        error_msg = f"Erro ao verificar status: {str(e)}"
        await ctx.error(error_msg)
        return {"error": error_msg}

@mcp.tool()
async def list_recent_analyses(
    limit: int = 10,
    page: int = 1,
    *,
    ctx: Context
) -> Dict[str, Any]:
    """
    Lista análises recentes.
    
    Args:
        limit: Número máximo de análises a retornar (padrão: 10)
        page: Página para paginação (padrão: 1)
        
    Returns:
        Lista de análises recentes
    """
    await ctx.debug(f"📋 Listando análises recentes (limit: {limit}, page: {page})")
    
    try:
        params = {"per_page": limit, "page": page}
        response = await http_client.get("/api/jobs", params=params)
        
        if response.status_code == 200:
            result = response.json()
            await ctx.info(f"✅ Encontradas {len(result.get('jobs', []))} análises")
            return result
        else:
            error_msg = f"Erro ao listar análises: {response.status_code}"
            await ctx.error(error_msg)
            return {"error": error_msg}
            
    except Exception as e:
        error_msg = f"Erro ao listar análises: {str(e)}"
        await ctx.error(error_msg)
        return {"error": error_msg}

@mcp.tool()
async def cancel_job(job_id: str, *, ctx: Context) -> Dict[str, Any]:
    """
    Cancela um job de análise em andamento.
    
    Args:
        job_id: ID do job a ser cancelado
        
    Returns:
        Resultado da operação de cancelamento
    """
    await ctx.info(f"🛑 Cancelando job: {job_id}")
    
    try:
        response = await http_client.post(f"/api/jobs/{job_id}/cancel")
        
        if response.status_code == 200:
            await ctx.info("✅ Job cancelado com sucesso")
            return {"success": True, "message": "Job cancelado com sucesso"}
        else:
            error_msg = f"Erro ao cancelar job: {response.status_code}"
            await ctx.error(error_msg)
            return {"success": False, "error": error_msg}
            
    except Exception as e:
        error_msg = f"Erro ao cancelar job: {str(e)}"
        await ctx.error(error_msg)
        return {"success": False, "error": error_msg}

@mcp.tool()
async def get_system_stats(*, ctx: Context) -> Dict[str, Any]:
    """
    Obtém estatísticas do sistema de análise.
    
    Returns:
        Estatísticas do sistema
    """
    await ctx.debug("📊 Obtendo estatísticas do sistema")
    
    try:
        response = await http_client.get("/api/jobs/stats")
        
        if response.status_code == 200:
            result = response.json()
            await ctx.debug("✅ Estatísticas obtidas")
            return result
        else:
            error_msg = f"Erro ao obter estatísticas: {response.status_code}"
            await ctx.error(error_msg)
            return {"error": error_msg}
            
    except Exception as e:
        error_msg = f"Erro ao obter estatísticas: {str(e)}"
        await ctx.error(error_msg)
        return {"error": error_msg}

@mcp.tool()
async def get_video_info(url: str, *, ctx: Context) -> Dict[str, Any]:
    """
    Obtém informações básicas de um vídeo do Instagram sem fazer análise completa.
    
    Args:
        url: URL do vídeo do Instagram
        
    Returns:
        Informações básicas do vídeo
    """
    await ctx.info(f"ℹ️ Obtendo informações do vídeo: {url}")
    
    # Validar URL do Instagram
    if not any(domain in url for domain in ["instagram.com", "instagr.am"]):
        await ctx.error("URL não é do Instagram")
        raise ValueError("URL deve ser do Instagram")
    
    try:
        # Por enquanto, retorna informações básicas
        # Em uma implementação completa, isso poderia usar o Instaloader diretamente
        return {
            "url": url,
            "platform": "Instagram",
            "status": "URL válida",
            "note": "Para análise completa, use analyze_instagram_video"
        }
        
    except Exception as e:
        error_msg = f"Erro ao obter informações: {str(e)}"
        await ctx.error(error_msg)
        return {"error": error_msg}

# ============================================================================
# ANÁLISE LOCAL (GEMINI DIRETO)
# ============================================================================

async def _upload_and_analyze_gemini(
    video_path: str,
    prompt: str,
    ctx: Context,
    media_resolution: str = "default",
) -> Dict[str, Any]:
    """
    Faz upload de um vídeo para o Gemini File API e executa análise.

    Args:
        video_path: Caminho para o arquivo de vídeo
        prompt: Prompt de análise
        ctx: Contexto MCP para logging
        media_resolution: Resolução de mídia - 'low' (~100 tok/s, até 3h), 'default' (~300 tok/s, até 1h), 'high'

    Returns:
        Dicionário com resultado da análise
    """
    from google import genai
    from google.genai import types

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY não configurada. Defina a variável de ambiente GEMINI_API_KEY."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)
    path = Path(video_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {video_path}")

    file_size = path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    if file_size == 0:
        raise ValueError("Arquivo de vídeo está vazio")

    valid_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.webm', '.mpeg', '.mpg', '.flv', '.wmv', '.3gpp')
    if not path.suffix.lower() in valid_extensions:
        raise ValueError(f"Formato não suportado: {path.suffix}. Formatos válidos: {', '.join(valid_extensions)}")

    if file_size > 2 * 1024 * 1024 * 1024:  # 2GB
        raise ValueError(f"Arquivo muito grande ({file_size_mb:.1f} MB). Limite: 2048 MB")

    await ctx.info(f"📁 Arquivo: {path.name} ({file_size_mb:.1f} MB)")
    await ctx.info("⬆️ Fazendo upload para Gemini File API...")

    # Upload (sync - Gemini SDK não tem upload async)
    uploaded = await asyncio.to_thread(client.files.upload, file=str(path))
    await ctx.info(f"✅ Upload concluído: {uploaded.name}")
    await ctx.info("⏳ Aguardando processamento do arquivo...")

    # Aguardar estado ACTIVE
    max_wait = 300
    waited = 0
    while waited < max_wait:
        info = await asyncio.to_thread(client.files.get, name=uploaded.name)
        if info.state == "ACTIVE":
            await ctx.info(f"✅ Arquivo pronto ({waited}s)")
            break
        if info.state == "FAILED":
            raise RuntimeError("Processamento do arquivo falhou no Gemini")
        await asyncio.sleep(5)
        waited += 5

    if waited >= max_wait:
        raise RuntimeError("Timeout aguardando processamento do arquivo")

    await ctx.info(f"🧠 Analisando com {GEMINI_MODEL}...")

    # Build GenerateContentConfig with system_instruction and media_resolution
    config_kwargs = {
        "system_instruction": prompt,
    }

    if media_resolution == "low":
        config_kwargs["media_resolution"] = types.MediaResolution.MEDIA_RESOLUTION_LOW
        await ctx.info("📐 Usando resolução baixa (~100 tokens/seg — suporta até 3h de vídeo)")
    elif media_resolution == "high":
        config_kwargs["media_resolution"] = types.MediaResolution.MEDIA_RESOLUTION_HIGH

    config = types.GenerateContentConfig(**config_kwargs)

    response = await asyncio.to_thread(
        client.models.generate_content,
        model=GEMINI_MODEL,
        contents=[uploaded, "Analise o vídeo conforme as instruções do sistema."],
        config=config,
    )

    return {
        "raw_response": response.text,
        "model_used": GEMINI_MODEL,
        "file_name": path.name,
        "file_size": file_size,
        "file_size_mb": round(file_size_mb, 2),
        "media_resolution": media_resolution,
    }


@mcp.tool()
async def analyze_local_video(
    file_path: str,
    analysis_type: str = "comprehensive",
    custom_prompt: str = "",
    media_resolution: str = "auto",
    *,
    ctx: Context
) -> Dict[str, Any]:
    """
    Analisa um arquivo de vídeo local usando Google Gemini diretamente.
    Suporta arquivos até 2GB e vídeos de até 3 horas (em resolução baixa).
    Não requer o backend API — conecta direto ao Gemini.

    Args:
        file_path: Caminho absoluto para o arquivo de vídeo (.mp4, .mov, .avi, .mkv, .webm)
        analysis_type: Tipo de análise - comprehensive, summary, transcription, visual_description, project_management
        custom_prompt: Prompt personalizado (sobrescreve o analysis_type se fornecido)
        media_resolution: Resolução de mídia - 'auto' (detecta pelo tamanho), 'low' (~100 tok/s, até 3h), 'default' (~300 tok/s, até 1h), 'high'

    Returns:
        Resultado da análise com conteúdo estruturado
    """
    await ctx.info(f"🎬 Análise local: {file_path}")

    # Validar tipo de análise
    if analysis_type not in VALID_ANALYSIS_TYPES:
        await ctx.error(f"Tipo de análise inválido: {analysis_type}")
        raise ValueError(f"Tipo de análise deve ser um de: {', '.join(VALID_ANALYSIS_TYPES)}")

    # Auto-detect media_resolution based on file size
    # Files > 50MB likely contain long videos that need low resolution to fit in 1M context
    resolved_resolution = media_resolution
    if media_resolution == "auto":
        file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
        if file_size_mb > 50:
            resolved_resolution = "low"
            await ctx.info(f"📐 Auto-detectado: arquivo grande ({file_size_mb:.0f}MB) — usando resolução baixa para caber no contexto")
        else:
            resolved_resolution = "default"

    # Selecionar prompt
    prompt = custom_prompt.strip() if custom_prompt.strip() else ANALYSIS_PROMPTS.get(analysis_type, ANALYSIS_PROMPTS["comprehensive"])

    try:
        start_time = time.time()
        result = await _upload_and_analyze_gemini(file_path, prompt, ctx, media_resolution=resolved_resolution)
        processing_time = time.time() - start_time

        await ctx.info(f"🎉 Análise concluída em {processing_time:.1f}s!")

        return {
            "success": True,
            "analysis_type": analysis_type,
            "processing_time_seconds": round(processing_time, 1),
            "file_name": result["file_name"],
            "file_size_mb": result["file_size_mb"],
            "model_used": result["model_used"],
            "analysis": result["raw_response"],
        }

    except Exception as e:
        error_msg = f"Erro na análise local: {str(e)}"
        await ctx.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
        }


# ============================================================================
# RECURSOS (RESOURCES)
# ============================================================================

@mcp.resource("analysis://{job_id}")
async def get_analysis_result(job_id: str) -> str:
    """
    Obtém o resultado de uma análise específica.
    
    Args:
        job_id: ID do job de análise
        
    Returns:
        Resultado da análise em formato JSON
    """
    try:
        response = await http_client.get(f"/api/video/status/{job_id}")
        
        if response.status_code == 200:
            result = response.json()
            return json.dumps(result, indent=2, ensure_ascii=False)
        else:
            return json.dumps({"error": f"Erro ao obter análise: {response.status_code}"})
            
    except Exception as e:
        return json.dumps({"error": f"Erro ao obter análise: {str(e)}"})

@mcp.resource("jobs://recent")
async def get_recent_jobs() -> str:
    """
    Obtém lista de jobs recentes.
    
    Returns:
        Lista de jobs em formato JSON
    """
    try:
        response = await http_client.get("/api/jobs?per_page=20")
        
        if response.status_code == 200:
            result = response.json()
            return json.dumps(result, indent=2, ensure_ascii=False)
        else:
            return json.dumps({"error": f"Erro ao obter jobs: {response.status_code}"})
            
    except Exception as e:
        return json.dumps({"error": f"Erro ao obter jobs: {str(e)}"})

@mcp.resource("stats://system")
async def get_system_statistics() -> str:
    """
    Obtém estatísticas do sistema.
    
    Returns:
        Estatísticas em formato JSON
    """
    try:
        response = await http_client.get("/api/jobs/stats")
        
        if response.status_code == 200:
            result = response.json()
            return json.dumps(result, indent=2, ensure_ascii=False)
        else:
            return json.dumps({"error": f"Erro ao obter estatísticas: {response.status_code}"})
            
    except Exception as e:
        return json.dumps({"error": f"Erro ao obter estatísticas: {str(e)}"})

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

async def _wait_for_completion(job_id: str, ctx: Context, max_wait: int = 300) -> Dict[str, Any]:
    """
    Aguarda a conclusão de um job.
    
    Args:
        job_id: ID do job
        ctx: Contexto para logging
        max_wait: Tempo máximo de espera em segundos
        
    Returns:
        Resultado da análise
    """
    waited = 0
    while waited < max_wait:
        try:
            response = await http_client.get(f"/api/video/status/{job_id}")
            
            if response.status_code == 200:
                status_data = response.json()
                status = status_data.get("status")
                progress = status_data.get("progress", 0)
                
                await ctx.debug(f"Status: {status}, Progresso: {progress}%")
                
                if status == "completed":
                    await ctx.info("🎉 Análise concluída com sucesso!")
                    return status_data.get("analysis_result", {})
                elif status == "failed":
                    error = status_data.get("error_message", "Erro desconhecido")
                    await ctx.error(f"Análise falhou: {error}")
                    raise Exception(f"Análise falhou: {error}")
                
                # Aguardar antes da próxima verificação
                await asyncio.sleep(5)
                waited += 5
            else:
                await ctx.error(f"Erro ao verificar status: {response.status_code}")
                raise Exception(f"Erro ao verificar status: {response.status_code}")
                
        except Exception as e:
            await ctx.error(f"Erro durante espera: {str(e)}")
            raise
    
    await ctx.error("Timeout aguardando conclusão da análise")
    raise Exception("Timeout aguardando conclusão da análise")

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    """Ponto de entrada principal do servidor MCP"""
    logger.info("🎬 Instagram Video Analyzer MCP Server")
    logger.info("📡 Conectando à API em: " + API_BASE_URL)
    mcp.run()

if __name__ == "__main__":
    main()
