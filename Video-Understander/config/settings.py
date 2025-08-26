"""
Configuration settings for Video-Understander application.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API Configuration
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-2.0-flash-exp", env="GEMINI_MODEL")
    gemini_safety_settings: str = Field("default", env="GEMINI_SAFETY_SETTINGS")
    
    # Video Processing Configuration
    max_video_size: int = Field(2147483648, env="MAX_VIDEO_SIZE")  # 2GB
    max_video_duration: int = Field(7200, env="MAX_VIDEO_DURATION")  # 2 hours
    default_sampling_rate: int = Field(1, env="DEFAULT_SAMPLING_RATE")
    video_quality: str = Field("standard", env="VIDEO_QUALITY")
    
    # File Storage Configuration
    storage_path: str = Field("./storage", env="STORAGE_PATH")
    temp_path: str = Field("./temp", env="TEMP_PATH")
    downloads_path: str = Field("./downloads", env="DOWNLOADS_PATH")
    results_path: str = Field("./results", env="RESULTS_PATH")
    
    # MCP Server Configuration
    mcp_host: str = Field("localhost", env="MCP_HOST")
    mcp_port: int = Field(8001, env="MCP_PORT")
    mcp_log_level: str = Field("INFO", env="MCP_LOG_LEVEL")
    
    # API Server Configuration
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    api_workers: int = Field(1, env="API_WORKERS")
    
    # Video Download Configuration
    youtube_quality: str = Field("best", env="YOUTUBE_QUALITY")
    instagram_login_required: bool = Field(False, env="INSTAGRAM_LOGIN_REQUIRED")
    tiktok_watermark: bool = Field(False, env="TIKTOK_WATERMARK")
    
    # Processing Configuration
    batch_size: int = Field(10, env="BATCH_SIZE")
    concurrent_downloads: int = Field(3, env="CONCURRENT_DOWNLOADS")
    timeout_seconds: int = Field(300, env="TIMEOUT_SECONDS")
    
    # Database Configuration
    database_url: str = Field("sqlite:///./video_analysis.db", env="DATABASE_URL")
    database_echo: bool = Field(False, env="DATABASE_ECHO")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("./logs/video_understander.log", env="LOG_FILE")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Security Configuration
    allowed_origins: str = Field("*", env="ALLOWED_ORIGINS")
    cors_enabled: bool = Field(True, env="CORS_ENABLED")
    rate_limit_enabled: bool = Field(False, env="RATE_LIMIT_ENABLED")
    
    # Feature Flags
    enable_batch_processing: bool = Field(True, env="ENABLE_BATCH_PROCESSING")
    enable_youtube_download: bool = Field(True, env="ENABLE_YOUTUBE_DOWNLOAD")
    enable_instagram_download: bool = Field(True, env="ENABLE_INSTAGRAM_DOWNLOAD")
    enable_tiktok_download: bool = Field(True, env="ENABLE_TIKTOK_DOWNLOAD")
    enable_local_files: bool = Field(True, env="ENABLE_LOCAL_FILES")
    enable_streaming_urls: bool = Field(True, env="ENABLE_STREAMING_URLS")
    
    # Performance Configuration
    max_concurrent_analyses: int = Field(5, env="MAX_CONCURRENT_ANALYSES")
    memory_limit_gb: int = Field(8, env="MEMORY_LIMIT_GB")
    cpu_cores: str = Field("auto", env="CPU_CORES")
    
    # Optional AI Services
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.storage_path,
            self.temp_path,
            self.downloads_path,
            self.results_path,
            os.path.dirname(self.log_file)
        ]
        
        for directory in directories:
            if directory:
                Path(directory).mkdir(parents=True, exist_ok=True)
    
    @property
    def supported_video_formats(self) -> List[str]:
        """List of supported video formats."""
        return [
            ".mp4", ".mpeg", ".mov", ".avi", ".flv", 
            ".mkv", ".webm", ".wmv", ".3gp", ".m4v"
        ]
    
    @property
    def gemini_generation_config(self) -> dict:
        """Gemini generation configuration."""
        return {
            "temperature": 0.1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    
    @property
    def gemini_safety_config(self) -> dict:
        """Gemini safety settings configuration."""
        if self.gemini_safety_settings == "strict":
            return {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
            }
        elif self.gemini_safety_settings == "permissive":
            return {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        else:  # default
            return {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
            }


# Global settings instance
settings = Settings()
