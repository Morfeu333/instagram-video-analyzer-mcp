"""
Video analysis service using Google Gemini API.
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Callable

from google import genai
from google.genai import types

from ..core.config import settings

logger = logging.getLogger(__name__)


class VideoAnalyzer:
    """Video analyzer using Google Gemini API."""
    
    def __init__(self):
        """Initialize the video analyzer."""
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = "gemini-2.5-flash"
    
    def analyze_video(
        self, 
        video_path: str,
        analysis_type: str = "comprehensive",
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> Dict[str, Any]:
        """
        Analyze video using Gemini API.
        
        Args:
            video_path: Path to the video file
            analysis_type: Type of analysis to perform
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            if progress_callback:
                progress_callback(0.1)
            
            # Check if file exists and is valid
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")

            # Validate file is not empty
            file_size = os.path.getsize(video_path)
            if file_size == 0:
                raise ValueError(f"Video file is empty: {video_path}")

            # Validate file extension
            if not video_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                raise ValueError(f"Unsupported video format: {video_path}")

            logger.info(f"Video file validated: {video_path} ({file_size} bytes)")
            
            if progress_callback:
                progress_callback(0.2)
            
            # Upload video file to Gemini
            logger.info(f"Uploading video file: {video_path}")
            try:
                uploaded_file = self.client.files.upload(file=video_path)
                logger.info(f"Successfully uploaded file to Gemini. File ID: {uploaded_file.name}")
            except Exception as e:
                raise RuntimeError(f"Failed to upload video to Gemini: {str(e)}")

            # Wait for file to be processed
            logger.info("Waiting for file to be processed by Gemini...")
            import time
            max_wait = 120  # Maximum wait time in seconds
            wait_time = 0

            while wait_time < max_wait:
                try:
                    file_info = self.client.files.get(name=uploaded_file.name)
                    logger.info(f"File state: {file_info.state}")

                    if file_info.state == "ACTIVE":
                        logger.info("File is ready for processing!")
                        break
                    elif file_info.state == "FAILED":
                        raise RuntimeError("File processing failed!")

                    time.sleep(3)
                    wait_time += 3
                    logger.info(f"Waiting for file processing... ({wait_time}s/{max_wait}s)")
                except Exception as e:
                    logger.error(f"Error checking file status: {e}")
                    break

            if wait_time >= max_wait:
                logger.warning("Timeout waiting for file to be processed, proceeding anyway...")

            if progress_callback:
                progress_callback(0.5)

            # Generate analysis prompt based on type
            prompt = self._get_analysis_prompt(analysis_type)

            # Analyze the video
            logger.info("Starting video analysis with Gemini")
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[uploaded_file, prompt]
                )
                logger.info("Successfully received response from Gemini")
            except Exception as e:
                raise RuntimeError(f"Failed to analyze video with Gemini: {str(e)}")
            
            if progress_callback:
                progress_callback(0.9)
            
            # Parse and structure the response
            analysis_result = {
                "analysis_type": analysis_type,
                "model_used": self.model,
                "file_size": file_size,
                "raw_response": response.text,
                "structured_analysis": self._parse_analysis_response(response.text, analysis_type)
            }
            
            if progress_callback:
                progress_callback(1.0)
            
            logger.info("Video analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            error_msg = f"Error analyzing video: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def _get_analysis_prompt(self, analysis_type: str) -> str:
        """
        Get analysis prompt based on type.
        
        Args:
            analysis_type: Type of analysis to perform
            
        Returns:
            Formatted prompt string
        """
        prompts = {
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
                1. Descrição de cada cena principal
                2. Pessoas, objetos e cenários
                3. Cores, iluminação e estilo visual
                4. Movimentos de câmera e transições
                5. Texto ou gráficos visíveis
                
                Seja específico e detalhado na descrição visual.
            """
        }
        
        return prompts.get(analysis_type, prompts["comprehensive"])
    
    def _parse_analysis_response(self, response_text: str, analysis_type: str) -> Dict[str, Any]:
        """
        Parse and structure the analysis response.
        
        Args:
            response_text: Raw response from Gemini
            analysis_type: Type of analysis performed
            
        Returns:
            Structured analysis data
        """
        # Basic parsing - can be enhanced with more sophisticated NLP
        sections = {}
        
        if analysis_type == "comprehensive":
            # Try to extract sections based on headers
            import re
            
            patterns = {
                "resumo": r"\*\*Resumo Geral\*\*:?\s*(.*?)(?=\*\*|$)",
                "visual": r"\*\*Análise Visual\*\*:?\s*(.*?)(?=\*\*|$)",
                "audio": r"\*\*Análise de Áudio\*\*:?\s*(.*?)(?=\*\*|$)",
                "temas": r"\*\*Temas e Mensagens\*\*:?\s*(.*?)(?=\*\*|$)",
                "timestamps": r"\*\*Timestamps Importantes\*\*:?\s*(.*?)(?=\*\*|$)",
                "insights": r"\*\*Insights e Análise\*\*:?\s*(.*?)(?=\*\*|$)"
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[key] = match.group(1).strip()
        
        return {
            "sections": sections,
            "full_text": response_text,
            "word_count": len(response_text.split()),
            "analysis_type": analysis_type
        }
