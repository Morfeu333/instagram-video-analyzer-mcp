#!/usr/bin/env python3
"""
Instagram Video Analyzer MCP Server

Este servidor MCP fornece ferramentas para análise de vídeos do Instagram usando IA.
Conecta-se à API do Instagram Video Analyzer para processar vídeos e retornar análises detalhadas.

Ferramentas disponíveis:
- analyze_instagram_video: Análise completa de vídeo
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
from datetime import datetime
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
API_BASE_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 300.0  # 5 minutos
MAX_RETRIES = 3

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
    valid_types = ["comprehensive", "summary", "transcription", "visual_description"]
    if analysis_type not in valid_types:
        await ctx.error(f"Tipo de análise inválido: {analysis_type}")
        raise ValueError(f"Tipo de análise deve ser um de: {', '.join(valid_types)}")
    
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
