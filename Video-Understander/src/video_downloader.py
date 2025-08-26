"""
Video downloader for various platforms (YouTube, Instagram, TikTok, etc.).
"""

import asyncio
import logging
import re
from pathlib import Path
from typing import Dict, Optional, Union
from urllib.parse import urlparse

import yt_dlp
import requests
from instaloader import Instaloader, Post

from config.settings import settings


class VideoDownloader:
    """Download videos from various platforms."""
    
    def __init__(self):
        """Initialize the video downloader."""
        self.logger = logging.getLogger(__name__)
        self.downloads_path = Path(settings.downloads_path)
        self.downloads_path.mkdir(parents=True, exist_ok=True)
        
        # Configure yt-dlp
        self.yt_dlp_opts = {
            'outtmpl': str(self.downloads_path / '%(title)s.%(ext)s'),
            'format': settings.youtube_quality,
            'writeinfojson': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
        }
        
        # Configure instaloader
        self.instaloader = Instaloader(
            download_videos=True,
            download_pictures=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=True,
            save_metadata=True,
            dirname_pattern=str(self.downloads_path / '{profile}'),
            filename_pattern='{profile}_{shortcode}'
        )
        
        self.logger.info("VideoDownloader initialized")
    
    async def download_video(self, url: str) -> str:
        """
        Download video from URL.
        
        Args:
            url: Video URL
            
        Returns:
            Path to downloaded video file
        """
        try:
            self.logger.info(f"Starting download from: {url}")
            
            # Determine platform and download accordingly
            if self._is_youtube_url(url):
                return await self._download_youtube(url)
            elif self._is_instagram_url(url):
                return await self._download_instagram(url)
            elif self._is_tiktok_url(url):
                return await self._download_tiktok(url)
            else:
                # Try generic download with yt-dlp
                return await self._download_generic(url)
                
        except Exception as e:
            self.logger.error(f"Error downloading video from {url}: {str(e)}")
            raise
    
    async def _download_youtube(self, url: str) -> str:
        """Download YouTube video."""
        try:
            self.logger.info(f"Downloading YouTube video: {url}")
            
            with yt_dlp.YoutubeDL(self.yt_dlp_opts) as ydl:
                # Extract info first
                info = await asyncio.to_thread(ydl.extract_info, url, download=False)
                
                # Download the video
                await asyncio.to_thread(ydl.download, [url])
                
                # Find the downloaded file
                title = info.get('title', 'video')
                ext = info.get('ext', 'mp4')
                filename = f"{title}.{ext}"
                
                # Clean filename
                filename = self._clean_filename(filename)
                video_path = self.downloads_path / filename
                
                if video_path.exists():
                    self.logger.info(f"YouTube video downloaded: {video_path}")
                    return str(video_path)
                else:
                    # Try to find the actual file
                    for file in self.downloads_path.glob(f"*{title}*"):
                        if file.suffix in ['.mp4', '.webm', '.mkv']:
                            self.logger.info(f"Found downloaded file: {file}")
                            return str(file)
                    
                    raise FileNotFoundError(f"Downloaded file not found: {filename}")
                    
        except Exception as e:
            self.logger.error(f"Error downloading YouTube video: {str(e)}")
            raise
    
    async def _download_instagram(self, url: str) -> str:
        """Download Instagram video."""
        try:
            self.logger.info(f"Downloading Instagram video: {url}")
            
            # Extract shortcode from URL
            shortcode = self._extract_instagram_shortcode(url)
            if not shortcode:
                raise ValueError(f"Could not extract shortcode from URL: {url}")
            
            # Download using instaloader
            post = Post.from_shortcode(self.instaloader.context, shortcode)
            
            # Download the post
            await asyncio.to_thread(
                self.instaloader.download_post, post, target=str(self.downloads_path)
            )
            
            # Find the downloaded video file
            profile = post.owner_username
            pattern = f"{profile}_{shortcode}*.mp4"
            
            for video_file in self.downloads_path.glob(f"**/{pattern}"):
                if video_file.is_file():
                    self.logger.info(f"Instagram video downloaded: {video_file}")
                    return str(video_file)
            
            # If not found, try alternative patterns
            for video_file in self.downloads_path.glob(f"**/*{shortcode}*.mp4"):
                if video_file.is_file():
                    self.logger.info(f"Instagram video found: {video_file}")
                    return str(video_file)
            
            raise FileNotFoundError(f"Instagram video file not found for shortcode: {shortcode}")
            
        except Exception as e:
            self.logger.error(f"Error downloading Instagram video: {str(e)}")
            raise
    
    async def _download_tiktok(self, url: str) -> str:
        """Download TikTok video."""
        try:
            self.logger.info(f"Downloading TikTok video: {url}")
            
            tiktok_opts = self.yt_dlp_opts.copy()
            if not settings.tiktok_watermark:
                tiktok_opts['format'] = 'best[height<=720]'
            
            with yt_dlp.YoutubeDL(tiktok_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, url, download=False)
                await asyncio.to_thread(ydl.download, [url])
                
                title = info.get('title', 'tiktok_video')
                ext = info.get('ext', 'mp4')
                filename = self._clean_filename(f"{title}.{ext}")
                
                video_path = self.downloads_path / filename
                
                if video_path.exists():
                    self.logger.info(f"TikTok video downloaded: {video_path}")
                    return str(video_path)
                else:
                    # Find the actual file
                    for file in self.downloads_path.glob(f"*{title}*"):
                        if file.suffix in ['.mp4', '.webm']:
                            return str(file)
                    
                    raise FileNotFoundError(f"TikTok video file not found: {filename}")
                    
        except Exception as e:
            self.logger.error(f"Error downloading TikTok video: {str(e)}")
            raise
    
    async def _download_generic(self, url: str) -> str:
        """Download video using generic method."""
        try:
            self.logger.info(f"Downloading video with generic method: {url}")
            
            with yt_dlp.YoutubeDL(self.yt_dlp_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, url, download=False)
                await asyncio.to_thread(ydl.download, [url])
                
                title = info.get('title', 'video')
                ext = info.get('ext', 'mp4')
                filename = self._clean_filename(f"{title}.{ext}")
                
                video_path = self.downloads_path / filename
                
                if video_path.exists():
                    return str(video_path)
                else:
                    # Find the actual file
                    for file in self.downloads_path.glob(f"*{title}*"):
                        if file.suffix in ['.mp4', '.webm', '.mkv', '.avi']:
                            return str(file)
                    
                    raise FileNotFoundError(f"Downloaded file not found: {filename}")
                    
        except Exception as e:
            self.logger.error(f"Error with generic download: {str(e)}")
            raise
    
    def _is_youtube_url(self, url: str) -> bool:
        """Check if URL is from YouTube."""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        parsed = urlparse(url)
        return parsed.netloc.lower() in youtube_domains
    
    def _is_instagram_url(self, url: str) -> bool:
        """Check if URL is from Instagram."""
        instagram_domains = ['instagram.com', 'www.instagram.com', 'm.instagram.com']
        parsed = urlparse(url)
        return parsed.netloc.lower() in instagram_domains
    
    def _is_tiktok_url(self, url: str) -> bool:
        """Check if URL is from TikTok."""
        tiktok_domains = ['tiktok.com', 'www.tiktok.com', 'm.tiktok.com', 'vm.tiktok.com']
        parsed = urlparse(url)
        return parsed.netloc.lower() in tiktok_domains
    
    def _extract_instagram_shortcode(self, url: str) -> Optional[str]:
        """Extract Instagram shortcode from URL."""
        patterns = [
            r'/p/([A-Za-z0-9_-]+)',
            r'/reel/([A-Za-z0-9_-]+)',
            r'/tv/([A-Za-z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename for filesystem compatibility."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 200:
            name, ext = filename.rsplit('.', 1)
            filename = name[:190] + '.' + ext
        
        return filename
    
    async def get_video_info(self, url: str) -> Dict:
        """Get video information without downloading."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, url, download=False)
                
                return {
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'thumbnail': info.get('thumbnail'),
                    'webpage_url': info.get('webpage_url'),
                    'extractor': info.get('extractor'),
                    'format': info.get('format'),
                    'filesize': info.get('filesize')
                }
                
        except Exception as e:
            self.logger.error(f"Error getting video info: {str(e)}")
            return {'error': str(e)}
    
    async def cleanup_downloads(self, keep_recent: int = 10) -> None:
        """Clean up old downloaded files."""
        try:
            files = list(self.downloads_path.glob('**/*'))
            files = [f for f in files if f.is_file()]
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Keep only recent files
            for file in files[keep_recent:]:
                try:
                    file.unlink()
                    self.logger.info(f"Cleaned up old file: {file}")
                except Exception as e:
                    self.logger.warning(f"Could not delete {file}: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
