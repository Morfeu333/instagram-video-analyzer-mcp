"""
Input validation utilities.
"""

import logging
import re
from pathlib import Path
from typing import List, Optional, Union
from urllib.parse import urlparse

from config.settings import settings


class VideoValidator:
    """Validate video inputs and parameters."""
    
    def __init__(self):
        """Initialize the validator."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("VideoValidator initialized")
    
    def validate_video_file(self, file_path: Union[str, Path]) -> bool:
        """
        Validate video file.
        
        Args:
            file_path: Path to video file
            
        Returns:
            True if valid
        """
        try:
            file_path = Path(file_path)
            
            # Check if file exists
            if not file_path.exists():
                self.logger.error(f"Video file does not exist: {file_path}")
                return False
            
            # Check if it's a file (not directory)
            if not file_path.is_file():
                self.logger.error(f"Path is not a file: {file_path}")
                return False
            
            # Check file extension
            if file_path.suffix.lower() not in settings.supported_video_formats:
                self.logger.error(f"Unsupported video format: {file_path.suffix}")
                return False
            
            # Check file size
            file_size = file_path.stat().st_size
            if file_size > settings.max_video_size:
                self.logger.error(f"Video file too large: {file_size} bytes > {settings.max_video_size}")
                return False
            
            if file_size == 0:
                self.logger.error(f"Video file is empty: {file_path}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating video file: {str(e)}")
            return False
    
    def validate_video_url(self, url: str) -> bool:
        """
        Validate video URL.
        
        Args:
            url: Video URL
            
        Returns:
            True if valid
        """
        try:
            # Basic URL validation
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                self.logger.error(f"Invalid URL format: {url}")
                return False
            
            # Check if scheme is supported
            if parsed.scheme.lower() not in ['http', 'https']:
                self.logger.error(f"Unsupported URL scheme: {parsed.scheme}")
                return False
            
            # Check for supported platforms
            supported_domains = [
                'youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com',
                'instagram.com', 'www.instagram.com', 'm.instagram.com',
                'tiktok.com', 'www.tiktok.com', 'm.tiktok.com', 'vm.tiktok.com',
                'twitter.com', 'x.com', 'www.twitter.com', 'www.x.com',
                'facebook.com', 'www.facebook.com', 'fb.watch'
            ]
            
            domain = parsed.netloc.lower()
            if not any(supported_domain in domain for supported_domain in supported_domains):
                self.logger.warning(f"URL from potentially unsupported domain: {domain}")
                # Don't return False here as yt-dlp might still support it
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating URL: {str(e)}")
            return False
    
    def validate_analysis_type(self, analysis_type: str) -> bool:
        """
        Validate analysis type.
        
        Args:
            analysis_type: Type of analysis
            
        Returns:
            True if valid
        """
        valid_types = [
            'comprehensive',
            'transcription',
            'summary',
            'visual_description',
            'question_answering'
        ]
        
        if analysis_type not in valid_types:
            self.logger.error(f"Invalid analysis type: {analysis_type}")
            return False
        
        return True
    
    def validate_sampling_rate(self, sampling_rate: Optional[int]) -> bool:
        """
        Validate frame sampling rate.
        
        Args:
            sampling_rate: Frames per second
            
        Returns:
            True if valid
        """
        if sampling_rate is None:
            return True
        
        if not isinstance(sampling_rate, int):
            self.logger.error(f"Sampling rate must be integer: {sampling_rate}")
            return False
        
        if sampling_rate <= 0:
            self.logger.error(f"Sampling rate must be positive: {sampling_rate}")
            return False
        
        if sampling_rate > 30:
            self.logger.warning(f"High sampling rate may impact performance: {sampling_rate}")
        
        return True
    
    def validate_time_offset(self, offset: Optional[int], duration: Optional[float] = None) -> bool:
        """
        Validate time offset.
        
        Args:
            offset: Time offset in seconds
            duration: Video duration for validation
            
        Returns:
            True if valid
        """
        if offset is None:
            return True
        
        if not isinstance(offset, (int, float)):
            self.logger.error(f"Time offset must be numeric: {offset}")
            return False
        
        if offset < 0:
            self.logger.error(f"Time offset cannot be negative: {offset}")
            return False
        
        if duration and offset >= duration:
            self.logger.error(f"Time offset exceeds video duration: {offset} >= {duration}")
            return False
        
        return True
    
    def validate_batch_inputs(self, video_inputs: List[str]) -> bool:
        """
        Validate batch processing inputs.
        
        Args:
            video_inputs: List of video paths or URLs
            
        Returns:
            True if valid
        """
        if not isinstance(video_inputs, list):
            self.logger.error("Video inputs must be a list")
            return False
        
        if len(video_inputs) == 0:
            self.logger.error("Video inputs list cannot be empty")
            return False
        
        if len(video_inputs) > settings.batch_size:
            self.logger.error(f"Batch size exceeds limit: {len(video_inputs)} > {settings.batch_size}")
            return False
        
        # Validate each input
        for i, video_input in enumerate(video_inputs):
            if not isinstance(video_input, str):
                self.logger.error(f"Video input {i} must be string: {type(video_input)}")
                return False
            
            # Check if it's URL or file path
            if self._is_url(video_input):
                if not self.validate_video_url(video_input):
                    self.logger.error(f"Invalid URL at index {i}: {video_input}")
                    return False
            else:
                if not self.validate_video_file(video_input):
                    self.logger.error(f"Invalid file path at index {i}: {video_input}")
                    return False
        
        return True
    
    def validate_custom_prompt(self, prompt: Optional[str]) -> bool:
        """
        Validate custom prompt.
        
        Args:
            prompt: Custom prompt text
            
        Returns:
            True if valid
        """
        if prompt is None:
            return True
        
        if not isinstance(prompt, str):
            self.logger.error(f"Custom prompt must be string: {type(prompt)}")
            return False
        
        if len(prompt.strip()) == 0:
            self.logger.error("Custom prompt cannot be empty")
            return False
        
        if len(prompt) > 10000:  # Reasonable limit
            self.logger.warning(f"Custom prompt is very long: {len(prompt)} characters")
        
        return True
    
    def validate_question(self, question: str) -> bool:
        """
        Validate question for video Q&A.
        
        Args:
            question: Question text
            
        Returns:
            True if valid
        """
        if not isinstance(question, str):
            self.logger.error(f"Question must be string: {type(question)}")
            return False
        
        if len(question.strip()) == 0:
            self.logger.error("Question cannot be empty")
            return False
        
        if len(question) > 1000:
            self.logger.warning(f"Question is very long: {len(question)} characters")
        
        return True
    
    def validate_language_code(self, language: Optional[str]) -> bool:
        """
        Validate language code.
        
        Args:
            language: Language code (e.g., 'en', 'es', 'pt')
            
        Returns:
            True if valid
        """
        if language is None:
            return True
        
        if not isinstance(language, str):
            self.logger.error(f"Language must be string: {type(language)}")
            return False
        
        # Basic validation - could be enhanced with full language code list
        if len(language) < 2 or len(language) > 10:
            self.logger.error(f"Invalid language code format: {language}")
            return False
        
        # Check for basic format (letters, hyphens, underscores)
        if not re.match(r'^[a-zA-Z_-]+$', language):
            self.logger.error(f"Invalid language code characters: {language}")
            return False
        
        return True
    
    def validate_scene_criteria(self, criteria: str) -> bool:
        """
        Validate scene extraction criteria.
        
        Args:
            criteria: Scene extraction criteria
            
        Returns:
            True if valid
        """
        if not isinstance(criteria, str):
            self.logger.error(f"Scene criteria must be string: {type(criteria)}")
            return False
        
        if len(criteria.strip()) == 0:
            self.logger.error("Scene criteria cannot be empty")
            return False
        
        return True
    
    def _is_url(self, path: str) -> bool:
        """Check if path is a URL."""
        return path.startswith(('http://', 'https://'))
    
    def get_validation_summary(self) -> dict:
        """Get validation rules summary."""
        return {
            'supported_video_formats': settings.supported_video_formats,
            'max_video_size_mb': settings.max_video_size / (1024 * 1024),
            'max_video_duration_hours': settings.max_video_duration / 3600,
            'max_batch_size': settings.batch_size,
            'supported_analysis_types': [
                'comprehensive',
                'transcription', 
                'summary',
                'visual_description',
                'question_answering'
            ],
            'supported_platforms': [
                'YouTube',
                'Instagram',
                'TikTok',
                'Twitter/X',
                'Facebook',
                'Generic (via yt-dlp)'
            ]
        }
