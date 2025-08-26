"""
Gemini API client for video analysis.
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from config.settings import settings


class GeminiClient:
    """Client for interacting with Google's Gemini Video Understanding API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.logger = logging.getLogger(__name__)
        
        # Configure Gemini
        genai.configure(api_key=settings.gemini_api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config=settings.gemini_generation_config,
            safety_settings=self._get_safety_settings()
        )
        
        self.logger.info(f"GeminiClient initialized with model: {settings.gemini_model}")
    
    def _get_safety_settings(self) -> Dict[HarmCategory, HarmBlockThreshold]:
        """Get safety settings for Gemini."""
        safety_config = settings.gemini_safety_config
        
        safety_settings = {}
        for category, threshold in safety_config.items():
            try:
                harm_category = getattr(HarmCategory, category)
                harm_threshold = getattr(HarmBlockThreshold, threshold)
                safety_settings[harm_category] = harm_threshold
            except AttributeError:
                self.logger.warning(f"Invalid safety setting: {category}={threshold}")
        
        return safety_settings
    
    async def upload_video_file(self, video_path: Union[str, Path]) -> Any:
        """
        Upload video file to Gemini Files API.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Uploaded file object
        """
        video_path = Path(video_path)
        
        try:
            self.logger.info(f"Uploading video file: {video_path}")
            
            # Upload file
            video_file = genai.upload_file(
                path=str(video_path),
                display_name=video_path.name
            )
            
            # Wait for processing
            while video_file.state.name == "PROCESSING":
                self.logger.info("Video processing...")
                await asyncio.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception(f"Video processing failed: {video_file.state}")
            
            self.logger.info(f"Video uploaded successfully: {video_file.name}")
            return video_file
            
        except Exception as e:
            self.logger.error(f"Error uploading video file: {str(e)}")
            raise
    
    async def analyze_video(
        self,
        video_input: Union[str, Path, Any],
        prompt: str,
        video_config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Analyze video using Gemini.
        
        Args:
            video_input: Video file path or uploaded file object
            prompt: Analysis prompt
            video_config: Video configuration (fps, offsets, etc.)
            
        Returns:
            Gemini response
        """
        try:
            self.logger.info("Starting video analysis with Gemini")
            
            # Prepare content
            if isinstance(video_input, (str, Path)):
                # For small files, use direct upload
                video_path = Path(video_input)
                if video_path.stat().st_size <= 20 * 1024 * 1024:  # 20MB
                    content = [prompt, video_input]
                else:
                    # Upload large file first
                    video_file = await self.upload_video_file(video_input)
                    content = [prompt, video_file]
            else:
                # Already uploaded file
                content = [prompt, video_input]
            
            # Add video configuration if provided
            if video_config:
                config_text = self._format_video_config(video_config)
                content[0] = f"{prompt}\n\nVideo Configuration: {config_text}"
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                content,
                stream=False
            )
            
            self.logger.info("Video analysis completed successfully")
            return response
            
        except Exception as e:
            self.logger.error(f"Error analyzing video: {str(e)}")
            raise
    
    async def batch_analyze_videos(
        self,
        video_inputs: List[Union[str, Path, Any]],
        prompts: List[str],
        video_configs: Optional[List[Dict[str, Any]]] = None
    ) -> List[Any]:
        """
        Analyze multiple videos in batch.
        
        Args:
            video_inputs: List of video inputs
            prompts: List of prompts for each video
            video_configs: Optional list of video configurations
            
        Returns:
            List of Gemini responses
        """
        if len(video_inputs) > settings.batch_size:
            raise ValueError(f"Batch size exceeds limit: {len(video_inputs)} > {settings.batch_size}")
        
        if len(video_inputs) != len(prompts):
            raise ValueError("Number of videos and prompts must match")
        
        try:
            self.logger.info(f"Starting batch analysis of {len(video_inputs)} videos")
            
            # Prepare all content
            batch_content = []
            for i, (video_input, prompt) in enumerate(zip(video_inputs, prompts)):
                video_config = video_configs[i] if video_configs and i < len(video_configs) else None
                
                # Handle video input
                if isinstance(video_input, (str, Path)):
                    video_path = Path(video_input)
                    if video_path.stat().st_size > 20 * 1024 * 1024:  # 20MB
                        video_file = await self.upload_video_file(video_input)
                        content = [prompt, video_file]
                    else:
                        content = [prompt, video_input]
                else:
                    content = [prompt, video_input]
                
                # Add video configuration
                if video_config:
                    config_text = self._format_video_config(video_config)
                    content[0] = f"{prompt}\n\nVideo Configuration: {config_text}"
                
                batch_content.append(content)
            
            # Process batch
            tasks = []
            for content in batch_content:
                task = asyncio.to_thread(
                    self.model.generate_content,
                    content,
                    stream=False
                )
                tasks.append(task)
            
            # Wait for all analyses to complete
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            self.logger.info(f"Batch analysis completed: {len(responses)} results")
            return responses
            
        except Exception as e:
            self.logger.error(f"Error in batch analysis: {str(e)}")
            raise
    
    async def analyze_youtube_video(
        self,
        youtube_url: str,
        prompt: str,
        video_config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Analyze YouTube video directly.
        
        Args:
            youtube_url: YouTube video URL
            prompt: Analysis prompt
            video_config: Video configuration
            
        Returns:
            Gemini response
        """
        try:
            self.logger.info(f"Analyzing YouTube video: {youtube_url}")
            
            # Prepare content with YouTube URL
            content = [prompt, youtube_url]
            
            # Add video configuration if provided
            if video_config:
                config_text = self._format_video_config(video_config)
                content[0] = f"{prompt}\n\nVideo Configuration: {config_text}"
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                content,
                stream=False
            )
            
            self.logger.info("YouTube video analysis completed")
            return response
            
        except Exception as e:
            self.logger.error(f"Error analyzing YouTube video: {str(e)}")
            raise
    
    def _format_video_config(self, config: Dict[str, Any]) -> str:
        """Format video configuration for prompt."""
        config_parts = []
        
        if "fps" in config:
            config_parts.append(f"Sampling rate: {config['fps']} FPS")
        
        if "start_offset" in config:
            config_parts.append(f"Start time: {config['start_offset']} seconds")
        
        if "end_offset" in config:
            config_parts.append(f"End time: {config['end_offset']} seconds")
        
        return ", ".join(config_parts) if config_parts else "Default settings"
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        try:
            model_info = genai.get_model(settings.gemini_model)
            return {
                "name": model_info.name,
                "display_name": model_info.display_name,
                "description": model_info.description,
                "input_token_limit": model_info.input_token_limit,
                "output_token_limit": model_info.output_token_limit,
                "supported_generation_methods": model_info.supported_generation_methods,
                "temperature": settings.gemini_generation_config.get("temperature"),
                "top_p": settings.gemini_generation_config.get("top_p"),
                "top_k": settings.gemini_generation_config.get("top_k"),
                "max_output_tokens": settings.gemini_generation_config.get("max_output_tokens")
            }
        except Exception as e:
            self.logger.error(f"Error getting model info: {str(e)}")
            return {"error": str(e)}
    
    async def list_uploaded_files(self) -> List[Dict[str, Any]]:
        """List all uploaded files."""
        try:
            files = genai.list_files()
            return [
                {
                    "name": file.name,
                    "display_name": file.display_name,
                    "mime_type": file.mime_type,
                    "size_bytes": file.size_bytes,
                    "create_time": file.create_time,
                    "update_time": file.update_time,
                    "state": file.state.name
                }
                for file in files
            ]
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}")
            return []
    
    async def delete_uploaded_file(self, file_name: str) -> bool:
        """Delete an uploaded file."""
        try:
            genai.delete_file(file_name)
            self.logger.info(f"Deleted file: {file_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting file {file_name}: {str(e)}")
            return False
