"""
Core video analysis module using Google's Gemini Video Understanding API.
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from config.settings import settings
from .utils.gemini_client import GeminiClient
from .utils.video_processor import VideoProcessor
from .utils.validators import VideoValidator
from .file_manager import FileManager
from .video_downloader import VideoDownloader


@dataclass
class VideoAnalysisResult:
    """Result of video analysis."""
    video_id: str
    video_path: str
    analysis_type: str
    result: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: float
    processing_time: float
    error: Optional[str] = None


class VideoAnalyzer:
    """Main video analysis class using Gemini Video Understanding."""
    
    def __init__(self):
        """Initialize the video analyzer."""
        self.logger = logging.getLogger(__name__)
        self.gemini_client = GeminiClient()
        self.video_processor = VideoProcessor()
        self.validator = VideoValidator()
        self.file_manager = FileManager()
        self.downloader = VideoDownloader()
        
        # Configure Gemini
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        
        self.logger.info("VideoAnalyzer initialized successfully")
    
    async def analyze_video_url(
        self,
        url: str,
        analysis_type: str = "comprehensive",
        custom_prompt: Optional[str] = None,
        sampling_rate: Optional[int] = None,
        start_offset: Optional[int] = None,
        end_offset: Optional[int] = None
    ) -> VideoAnalysisResult:
        """
        Analyze video from URL.
        
        Args:
            url: Video URL (YouTube, Instagram, TikTok, etc.)
            analysis_type: Type of analysis (comprehensive, transcription, summary, etc.)
            custom_prompt: Custom analysis prompt
            sampling_rate: Frame sampling rate (FPS)
            start_offset: Start time in seconds
            end_offset: End time in seconds
            
        Returns:
            VideoAnalysisResult object
        """
        start_time = time.time()
        video_id = self._generate_video_id(url)
        
        try:
            self.logger.info(f"Starting analysis for URL: {url}")
            
            # Download video
            video_path = await self.downloader.download_video(url)
            
            # Analyze the downloaded video
            result = await self.analyze_video_file(
                video_path=video_path,
                analysis_type=analysis_type,
                custom_prompt=custom_prompt,
                sampling_rate=sampling_rate,
                start_offset=start_offset,
                end_offset=end_offset
            )
            
            # Update result with URL metadata
            result.video_id = video_id
            result.metadata.update({
                "source_url": url,
                "download_path": video_path
            })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing video URL {url}: {str(e)}")
            return VideoAnalysisResult(
                video_id=video_id,
                video_path="",
                analysis_type=analysis_type,
                result={},
                metadata={"source_url": url},
                timestamp=time.time(),
                processing_time=time.time() - start_time,
                error=str(e)
            )
    
    async def analyze_video_file(
        self,
        video_path: Union[str, Path],
        analysis_type: str = "comprehensive",
        custom_prompt: Optional[str] = None,
        sampling_rate: Optional[int] = None,
        start_offset: Optional[int] = None,
        end_offset: Optional[int] = None
    ) -> VideoAnalysisResult:
        """
        Analyze local video file.
        
        Args:
            video_path: Path to video file
            analysis_type: Type of analysis
            custom_prompt: Custom analysis prompt
            sampling_rate: Frame sampling rate (FPS)
            start_offset: Start time in seconds
            end_offset: End time in seconds
            
        Returns:
            VideoAnalysisResult object
        """
        start_time = time.time()
        video_path = Path(video_path)
        video_id = self._generate_video_id(str(video_path))
        
        try:
            self.logger.info(f"Starting analysis for file: {video_path}")
            
            # Validate video file
            if not self.validator.validate_video_file(video_path):
                raise ValueError(f"Invalid video file: {video_path}")
            
            # Get video metadata
            metadata = await self.video_processor.get_video_metadata(video_path)
            
            # Upload video to Gemini (if large file)
            if video_path.stat().st_size > 20 * 1024 * 1024:  # 20MB
                video_file = await self.gemini_client.upload_video_file(video_path)
            else:
                video_file = video_path
            
            # Prepare analysis prompt
            prompt = self._build_analysis_prompt(
                analysis_type, custom_prompt, start_offset, end_offset
            )
            
            # Configure video parameters
            video_config = self._build_video_config(
                sampling_rate, start_offset, end_offset
            )
            
            # Perform analysis
            response = await self.gemini_client.analyze_video(
                video_file, prompt, video_config
            )
            
            # Process and structure the result
            analysis_result = self._process_analysis_response(
                response, analysis_type
            )
            
            processing_time = time.time() - start_time
            
            return VideoAnalysisResult(
                video_id=video_id,
                video_path=str(video_path),
                analysis_type=analysis_type,
                result=analysis_result,
                metadata=metadata,
                timestamp=time.time(),
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing video file {video_path}: {str(e)}")
            return VideoAnalysisResult(
                video_id=video_id,
                video_path=str(video_path),
                analysis_type=analysis_type,
                result={},
                metadata={},
                timestamp=time.time(),
                processing_time=time.time() - start_time,
                error=str(e)
            )
    
    async def transcribe_video(
        self,
        video_path: Union[str, Path],
        include_timestamps: bool = True,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get video transcription with timestamps.
        
        Args:
            video_path: Path to video file
            include_timestamps: Include timestamp information
            language: Target language for transcription
            
        Returns:
            Transcription result with timestamps
        """
        result = await self.analyze_video_file(
            video_path=video_path,
            analysis_type="transcription",
            custom_prompt=self._build_transcription_prompt(include_timestamps, language)
        )
        
        return result.result
    
    async def ask_video_question(
        self,
        video_path: Union[str, Path],
        question: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ask specific question about video content.
        
        Args:
            video_path: Path to video file
            question: Question to ask about the video
            context: Additional context for the question
            
        Returns:
            Answer to the question
        """
        prompt = f"Question: {question}"
        if context:
            prompt = f"Context: {context}\n\n{prompt}"
        
        result = await self.analyze_video_file(
            video_path=video_path,
            analysis_type="question_answering",
            custom_prompt=prompt
        )
        
        return result.result
    
    def _generate_video_id(self, source: str) -> str:
        """Generate unique video ID."""
        import hashlib
        return hashlib.md5(f"{source}_{time.time()}".encode()).hexdigest()[:12]
    
    def _build_analysis_prompt(
        self,
        analysis_type: str,
        custom_prompt: Optional[str],
        start_offset: Optional[int],
        end_offset: Optional[int]
    ) -> str:
        """Build analysis prompt based on type."""
        if custom_prompt:
            return custom_prompt
        
        prompts = {
            "comprehensive": """
            Provide a comprehensive analysis of this video including:
            1. Detailed description of visual content with timestamps
            2. Complete audio transcription with precise timestamps (MM:SS format)
            3. Scene segmentation and key moments
            4. Objects, people, and actions identified
            5. Overall summary and key insights
            6. Any text or graphics visible in the video
            """,
            "transcription": """
            Provide a complete transcription of all spoken content in this video.
            Include precise timestamps in MM:SS format for each segment.
            Format: [MM:SS] Transcribed text
            """,
            "summary": """
            Provide a concise summary of this video including:
            - Main topic and purpose
            - Key points discussed
            - Important visual elements
            - Duration and structure
            """,
            "visual_description": """
            Describe the visual content of this video in detail:
            - Scene descriptions with timestamps
            - Objects and people present
            - Actions and movements
            - Visual style and quality
            - Any text or graphics shown
            """,
            "question_answering": "Answer the following question about this video:"
        }
        
        base_prompt = prompts.get(analysis_type, prompts["comprehensive"])
        
        if start_offset or end_offset:
            time_info = f"\nAnalyze the video segment"
            if start_offset:
                time_info += f" starting from {start_offset} seconds"
            if end_offset:
                time_info += f" ending at {end_offset} seconds"
            base_prompt += time_info
        
        return base_prompt
    
    def _build_video_config(
        self,
        sampling_rate: Optional[int],
        start_offset: Optional[int],
        end_offset: Optional[int]
    ) -> Dict[str, Any]:
        """Build video configuration for Gemini."""
        config = {}
        
        if sampling_rate:
            config["fps"] = sampling_rate
        
        if start_offset:
            config["start_offset"] = start_offset
        
        if end_offset:
            config["end_offset"] = end_offset
        
        return config
    
    def _build_transcription_prompt(
        self,
        include_timestamps: bool,
        language: Optional[str]
    ) -> str:
        """Build transcription-specific prompt."""
        prompt = "Transcribe all spoken content in this video."
        
        if include_timestamps:
            prompt += " Include precise timestamps in MM:SS format for each segment."
        
        if language:
            prompt += f" Provide transcription in {language}."
        
        prompt += "\nFormat each line as: [MM:SS] Transcribed text"
        
        return prompt
    
    def _process_analysis_response(
        self,
        response: Any,
        analysis_type: str
    ) -> Dict[str, Any]:
        """Process and structure the Gemini response."""
        # Extract text from response
        if hasattr(response, 'text'):
            content = response.text
        else:
            content = str(response)
        
        # Structure based on analysis type
        result = {
            "content": content,
            "analysis_type": analysis_type,
            "timestamp": time.time()
        }
        
        # Parse specific formats
        if analysis_type == "transcription":
            result["transcription"] = self._parse_transcription(content)
        elif analysis_type == "comprehensive":
            result.update(self._parse_comprehensive_analysis(content))
        
        return result
    
    def _parse_transcription(self, content: str) -> List[Dict[str, str]]:
        """Parse transcription with timestamps."""
        lines = content.split('\n')
        transcription = []
        
        for line in lines:
            line = line.strip()
            if line and '[' in line and ']' in line:
                try:
                    timestamp = line[line.find('[')+1:line.find(']')]
                    text = line[line.find(']')+1:].strip()
                    if text:
                        transcription.append({
                            "timestamp": timestamp,
                            "text": text
                        })
                except:
                    continue
        
        return transcription
    
    def _parse_comprehensive_analysis(self, content: str) -> Dict[str, Any]:
        """Parse comprehensive analysis into structured format."""
        # This is a simplified parser - can be enhanced based on response format
        return {
            "full_analysis": content,
            "sections": content.split('\n\n') if '\n\n' in content else [content]
        }
