"""
Instagram video downloader service using Instaloader.
"""
import os
import re
import logging
from pathlib import Path
from typing import Optional, Tuple, Callable
from urllib.parse import urlparse

import instaloader
from instaloader import Post

from ..core.config import settings

logger = logging.getLogger(__name__)


class InstagramDownloader:
    """Instagram video downloader using Instaloader."""
    
    def __init__(self):
        """Initialize the Instagram downloader."""
        self.logged_in = False
        self.loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
        )
        
        # Login if credentials are provided and valid
        if (settings.instagram_username and
            settings.instagram_password and
            settings.instagram_username != "seu_usuario_aqui" and
            settings.instagram_password != "sua_senha_aqui"):
            try:
                self.loader.login(settings.instagram_username, settings.instagram_password)
                logger.info("Successfully logged into Instagram")
                self.logged_in = True
            except Exception as e:
                logger.warning(f"Failed to login to Instagram: {e}")
                logger.info("Continuing without login (limited functionality)")
                self.logged_in = False
        else:
            logger.info("No valid Instagram credentials provided, running without login")
            self.logged_in = False
    
    def extract_shortcode_from_url(self, url: str) -> Optional[str]:
        """
        Extract Instagram post shortcode from URL.
        
        Args:
            url: Instagram post URL
            
        Returns:
            Shortcode if found, None otherwise
        """
        patterns = [
            r'instagram\.com/p/([A-Za-z0-9_-]+)',
            r'instagram\.com/reel/([A-Za-z0-9_-]+)',
            r'instagram\.com/tv/([A-Za-z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def download_video(
        self, 
        instagram_url: str, 
        output_dir: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Download video from Instagram URL.
        
        Args:
            instagram_url: Instagram post URL
            output_dir: Directory to save the video
            progress_callback: Optional callback for progress updates
            
        Returns:
            Tuple of (success, video_path, error_message)
        """
        try:
            # Extract shortcode from URL
            shortcode = self.extract_shortcode_from_url(instagram_url)
            if not shortcode:
                return False, None, "Invalid Instagram URL format"
            
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Get post
            if progress_callback:
                progress_callback(0.1)
            
            post = Post.from_shortcode(self.loader.context, shortcode)
            
            if progress_callback:
                progress_callback(0.3)
            
            # Check if post has video
            if not post.is_video:
                return False, None, "Post does not contain a video"
            
            # Download the post
            if progress_callback:
                progress_callback(0.5)
            
            # Set target directory
            self.loader.dirname_pattern = str(output_path)
            
            # Download
            self.loader.download_post(post, target=str(output_path))
            
            if progress_callback:
                progress_callback(0.9)
            
            # Find the downloaded video file
            # Try multiple patterns as Instaloader may use different naming conventions
            video_files = []

            # Pattern 1: Files with shortcode
            video_files.extend(list(output_path.glob(f"*{shortcode}*.mp4")))

            # Pattern 2: Any MP4 files in the directory (fallback)
            if not video_files:
                video_files.extend(list(output_path.glob("*.mp4")))

            # Pattern 3: Look in subdirectories (Instaloader sometimes creates subdirs)
            if not video_files:
                video_files.extend(list(output_path.rglob("*.mp4")))

            if not video_files:
                # List all files for debugging
                all_files = list(output_path.rglob("*"))
                logger.error(f"No video files found. All files in {output_path}: {[str(f) for f in all_files]}")
                return False, None, "Video file not found after download"

            # Use the first (and likely only) video file found
            video_path = str(video_files[0])
            logger.info(f"Found video file: {video_path}")
            
            if progress_callback:
                progress_callback(1.0)
            
            logger.info(f"Successfully downloaded video: {video_path}")
            return True, video_path, None
            
        except Exception as e:
            error_msg = f"Error downloading video: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def get_post_info(self, instagram_url: str) -> Optional[dict]:
        """
        Get basic information about an Instagram post.
        
        Args:
            instagram_url: Instagram post URL
            
        Returns:
            Dictionary with post information or None if error
        """
        try:
            shortcode = self.extract_shortcode_from_url(instagram_url)
            if not shortcode:
                return None
            
            post = Post.from_shortcode(self.loader.context, shortcode)
            
            return {
                "shortcode": shortcode,
                "is_video": post.is_video,
                "caption": post.caption,
                "owner_username": post.owner_username,
                "date": post.date_utc.isoformat() if post.date_utc else None,
                "likes": post.likes,
                "comments": post.comments,
                "video_duration": post.video_duration if post.is_video else None,
            }
            
        except Exception as e:
            logger.error(f"Error getting post info: {e}")
            return None
