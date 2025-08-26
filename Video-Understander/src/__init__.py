"""
Video-Understander: A comprehensive video analysis application powered by Gemini.
"""

__version__ = "1.0.0"
__author__ = "Video-Understander Team"
__description__ = "Comprehensive video analysis using Google's Gemini Video Understanding API"

from .video_analyzer import VideoAnalyzer
from .video_downloader import VideoDownloader
from .file_manager import FileManager

__all__ = [
    "VideoAnalyzer",
    "VideoDownloader", 
    "FileManager"
]
