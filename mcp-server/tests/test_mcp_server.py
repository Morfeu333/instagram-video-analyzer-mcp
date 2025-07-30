#!/usr/bin/env python3
"""
Testes para o Instagram Video Analyzer MCP Server

Execute com: pytest test_mcp_server.py -v
"""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

# Importar o servidor MCP
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from instagram_video_analyzer_mcp import mcp, _wait_for_completion

class TestMCPServer:
    """Testes para o servidor MCP"""
    
    @pytest.fixture
    def mock_http_client(self):
        """Mock do cliente HTTP"""
        client = AsyncMock(spec=httpx.AsyncClient)
        return client
    
    @pytest.fixture
    def sample_video_url(self):
        """URL de exemplo para testes"""
        return "https://www.instagram.com/reel/DMiEEmlMI7J/"
    
    @pytest.fixture
    def sample_job_response(self):
        """Resposta de exemplo para criação de job"""
        return {
            "job_id": "test-job-123",
            "status": "pending",
            "message": "Job created successfully"
        }
    
    @pytest.fixture
    def sample_analysis_result(self):
        """Resultado de exemplo de análise"""
        return {
            "job_id": "test-job-123",
            "status": "completed",
            "progress": 100,
            "analysis_result": {
                "analysis": {
                    "analysis_type": "comprehensive",
                    "model_used": "gemini-2.5-flash",
                    "file_size": 19058688,
                    "raw_response": "Análise detalhada do vídeo..."
                }
            }
        }

class TestVideoAnalysis:
    """Testes para análise de vídeos"""
    
    @pytest.mark.asyncio
    async def test_analyze_instagram_video_success(self, mock_http_client, sample_video_url, sample_job_response, sample_analysis_result):
        """Testa análise bem-sucedida de vídeo"""
        
        # Mock das respostas HTTP
        mock_http_client.post.return_value.status_code = 200
        mock_http_client.post.return_value.json.return_value = sample_job_response
        
        mock_http_client.get.return_value.status_code = 200
        mock_http_client.get.return_value.json.return_value = sample_analysis_result
        
        # Mock do contexto
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            # Importar e testar a função
            from instagram_video_analyzer_mcp import analyze_instagram_video
            
            result = await analyze_instagram_video(
                url=sample_video_url,
                analysis_type="comprehensive",
                ctx=mock_ctx
            )
        
        # Verificações
        assert result["success"] is True
        assert result["job_id"] == "test-job-123"
        assert result["status"] == "completed"
        assert "analysis" in result
        
        # Verificar chamadas HTTP
        mock_http_client.post.assert_called_once()
        mock_http_client.get.assert_called()
        
        # Verificar logs
        mock_ctx.info.assert_called()
    
    @pytest.mark.asyncio
    async def test_analyze_instagram_video_invalid_url(self, mock_http_client):
        """Testa análise com URL inválida"""
        
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import analyze_instagram_video
            
            with pytest.raises(ValueError, match="URL deve ser do Instagram"):
                await analyze_instagram_video(
                    url="https://youtube.com/watch?v=invalid",
                    analysis_type="comprehensive",
                    ctx=mock_ctx
                )
    
    @pytest.mark.asyncio
    async def test_analyze_instagram_video_invalid_type(self, mock_http_client, sample_video_url):
        """Testa análise com tipo inválido"""
        
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import analyze_instagram_video
            
            with pytest.raises(ValueError, match="Tipo de análise deve ser um de"):
                await analyze_instagram_video(
                    url=sample_video_url,
                    analysis_type="invalid_type",
                    ctx=mock_ctx
                )

class TestJobManagement:
    """Testes para gerenciamento de jobs"""
    
    @pytest.mark.asyncio
    async def test_get_job_status_success(self, mock_http_client, sample_analysis_result):
        """Testa obtenção de status de job"""
        
        mock_http_client.get.return_value.status_code = 200
        mock_http_client.get.return_value.json.return_value = sample_analysis_result
        
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import get_job_status
            
            result = await get_job_status(
                job_id="test-job-123",
                ctx=mock_ctx
            )
        
        assert result["job_id"] == "test-job-123"
        assert result["status"] == "completed"
        mock_http_client.get.assert_called_with("/api/video/status/test-job-123")
    
    @pytest.mark.asyncio
    async def test_cancel_job_success(self, mock_http_client):
        """Testa cancelamento de job"""
        
        mock_http_client.post.return_value.status_code = 200
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import cancel_job
            
            result = await cancel_job(
                job_id="test-job-123",
                ctx=mock_ctx
            )
        
        assert result["success"] is True
        mock_http_client.post.assert_called_with("/api/jobs/test-job-123/cancel")
    
    @pytest.mark.asyncio
    async def test_list_recent_analyses(self, mock_http_client):
        """Testa listagem de análises recentes"""
        
        mock_response = {
            "jobs": [
                {"job_id": "job1", "status": "completed"},
                {"job_id": "job2", "status": "pending"}
            ],
            "total": 2,
            "page": 1
        }
        
        mock_http_client.get.return_value.status_code = 200
        mock_http_client.get.return_value.json.return_value = mock_response
        
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import list_recent_analyses
            
            result = await list_recent_analyses(
                limit=10,
                page=1,
                ctx=mock_ctx
            )
        
        assert len(result["jobs"]) == 2
        assert result["total"] == 2

class TestSystemStats:
    """Testes para estatísticas do sistema"""
    
    @pytest.mark.asyncio
    async def test_get_system_stats(self, mock_http_client):
        """Testa obtenção de estatísticas do sistema"""
        
        mock_stats = {
            "total_jobs": 150,
            "completed_jobs": 142,
            "failed_jobs": 3,
            "pending_jobs": 5,
            "success_rate": 94.67,
            "average_processing_time": 125.5
        }
        
        mock_http_client.get.return_value.status_code = 200
        mock_http_client.get.return_value.json.return_value = mock_stats
        
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import get_system_stats
            
            result = await get_system_stats(ctx=mock_ctx)
        
        assert result["total_jobs"] == 150
        assert result["success_rate"] == 94.67

class TestResources:
    """Testes para recursos MCP"""
    
    @pytest.mark.asyncio
    async def test_get_analysis_result_resource(self, mock_http_client, sample_analysis_result):
        """Testa recurso de resultado de análise"""
        
        mock_http_client.get.return_value.status_code = 200
        mock_http_client.get.return_value.json.return_value = sample_analysis_result
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import get_analysis_result
            
            result = await get_analysis_result(job_id="test-job-123")
        
        # Verificar se retorna JSON válido
        parsed_result = json.loads(result)
        assert parsed_result["job_id"] == "test-job-123"
        assert parsed_result["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_get_recent_jobs_resource(self, mock_http_client):
        """Testa recurso de jobs recentes"""
        
        mock_jobs = {
            "jobs": [{"job_id": "job1", "status": "completed"}],
            "total": 1
        }
        
        mock_http_client.get.return_value.status_code = 200
        mock_http_client.get.return_value.json.return_value = mock_jobs
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            from instagram_video_analyzer_mcp import get_recent_jobs
            
            result = await get_recent_jobs()
        
        parsed_result = json.loads(result)
        assert len(parsed_result["jobs"]) == 1

class TestUtilityFunctions:
    """Testes para funções utilitárias"""
    
    @pytest.mark.asyncio
    async def test_wait_for_completion_success(self, mock_http_client):
        """Testa espera por conclusão bem-sucedida"""
        
        # Simular progressão: pending -> processing -> completed
        responses = [
            {"status": "pending", "progress": 0},
            {"status": "processing", "progress": 50},
            {"status": "completed", "progress": 100, "analysis_result": {"test": "data"}}
        ]
        
        mock_http_client.get.return_value.status_code = 200
        
        call_count = 0
        def mock_json():
            nonlocal call_count
            response = responses[min(call_count, len(responses) - 1)]
            call_count += 1
            return response
        
        mock_http_client.get.return_value.json = mock_json
        
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            with patch('asyncio.sleep', new_callable=AsyncMock):  # Mock sleep para acelerar teste
                result = await _wait_for_completion("test-job", mock_ctx, max_wait=30)
        
        assert result == {"test": "data"}
    
    @pytest.mark.asyncio
    async def test_wait_for_completion_failure(self, mock_http_client):
        """Testa espera por conclusão com falha"""
        
        mock_response = {
            "status": "failed",
            "error_message": "Erro de teste"
        }
        
        mock_http_client.get.return_value.status_code = 200
        mock_http_client.get.return_value.json.return_value = mock_response
        
        mock_ctx = AsyncMock()
        
        with patch('instagram_video_analyzer_mcp.http_client', mock_http_client):
            with pytest.raises(Exception, match="Análise falhou: Erro de teste"):
                await _wait_for_completion("test-job", mock_ctx, max_wait=30)

class TestVideoInfo:
    """Testes para informações de vídeo"""
    
    @pytest.mark.asyncio
    async def test_get_video_info_success(self, sample_video_url):
        """Testa obtenção de informações de vídeo"""
        
        mock_ctx = AsyncMock()
        
        from instagram_video_analyzer_mcp import get_video_info
        
        result = await get_video_info(url=sample_video_url, ctx=mock_ctx)
        
        assert result["url"] == sample_video_url
        assert result["platform"] == "Instagram"
        assert result["status"] == "URL válida"
    
    @pytest.mark.asyncio
    async def test_get_video_info_invalid_url(self):
        """Testa obtenção de informações com URL inválida"""
        
        mock_ctx = AsyncMock()
        
        from instagram_video_analyzer_mcp import get_video_info
        
        with pytest.raises(ValueError, match="URL deve ser do Instagram"):
            await get_video_info(url="https://youtube.com/invalid", ctx=mock_ctx)

# Configuração do pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
