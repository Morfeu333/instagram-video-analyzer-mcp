"""
File management utilities for Video-Understander.
"""

import asyncio
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiofiles

from config.settings import settings


class FileManager:
    """Manage files and storage for video analysis."""
    
    def __init__(self):
        """Initialize the file manager."""
        self.logger = logging.getLogger(__name__)
        
        # Create directories
        self.storage_path = Path(settings.storage_path)
        self.temp_path = Path(settings.temp_path)
        self.downloads_path = Path(settings.downloads_path)
        self.results_path = Path(settings.results_path)
        
        for path in [self.storage_path, self.temp_path, self.downloads_path, self.results_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("FileManager initialized")
    
    async def save_analysis_result(
        self,
        result: Dict[str, Any],
        filename: Optional[str] = None
    ) -> str:
        """
        Save analysis result to file.
        
        Args:
            result: Analysis result dictionary
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_id = result.get('video_id', 'unknown')
                filename = f"analysis_{video_id}_{timestamp}.json"
            
            file_path = self.results_path / filename
            
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(result, indent=2, ensure_ascii=False))
            
            self.logger.info(f"Analysis result saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"Error saving analysis result: {str(e)}")
            raise
    
    async def save_transcription_markdown(
        self,
        transcription_data: Dict[str, Any],
        video_info: Dict[str, Any],
        output_path: Optional[Union[str, Path]] = None
    ) -> str:
        """
        Save transcription as markdown file.
        
        Args:
            transcription_data: Transcription data with timestamps
            video_info: Video metadata and information
            output_path: Optional custom output path
            
        Returns:
            Path to saved markdown file
        """
        try:
            if not output_path:
                # Generate filename from video info
                profile = video_info.get('profile', 'unknown')
                video_code = video_info.get('video_code', 'unknown')
                filename = f"{profile}_{video_code}.md"
                output_path = self.results_path / filename
            else:
                output_path = Path(output_path)
            
            # Generate markdown content
            markdown_content = self._generate_transcription_markdown(
                transcription_data, video_info
            )
            
            async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
                await f.write(markdown_content)
            
            self.logger.info(f"Transcription markdown saved: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error saving transcription markdown: {str(e)}")
            raise
    
    def _generate_transcription_markdown(
        self,
        transcription_data: Dict[str, Any],
        video_info: Dict[str, Any]
    ) -> str:
        """Generate markdown content for transcription."""
        
        profile = video_info.get('profile', 'Unknown')
        video_code = video_info.get('video_code', 'Unknown')
        url = video_info.get('url', 'Unknown')
        title = video_info.get('title', 'Unknown')
        description = video_info.get('description', '')
        duration = video_info.get('duration', 'Unknown')
        upload_date = video_info.get('upload_date', 'Unknown')
        view_count = video_info.get('view_count', 'Unknown')
        like_count = video_info.get('like_count', 'Unknown')
        
        markdown = f"""# Video Analysis - {profile}_{video_code}

## Video Information
- **Profile**: {profile}
- **Video Code**: {video_code}
- **URL**: {url}
- **Title**: {title}
- **Duration**: {duration}
- **Upload Date**: {upload_date}
- **Views**: {view_count}
- **Likes**: {like_count}

## Description
{description}

## Transcription with Timestamps

"""
        
        # Add transcription content
        transcription = transcription_data.get('transcription', [])
        if isinstance(transcription, list):
            for item in transcription:
                if isinstance(item, dict):
                    timestamp = item.get('timestamp', '00:00')
                    text = item.get('text', '')
                    markdown += f"**[{timestamp}]** {text}\n\n"
        else:
            # Handle raw transcription text
            markdown += f"{transcription}\n\n"
        
        # Add analysis metadata
        markdown += f"""## Analysis Metadata
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Processing Time**: {transcription_data.get('processing_time', 'Unknown')} seconds
- **Analysis Type**: {transcription_data.get('analysis_type', 'transcription')}

## Additional Information
{transcription_data.get('content', '')}
"""
        
        return markdown
    
    async def copy_video_to_storage(
        self,
        source_path: Union[str, Path],
        target_name: Optional[str] = None
    ) -> str:
        """
        Copy video file to storage directory.
        
        Args:
            source_path: Source video file path
            target_name: Optional target filename
            
        Returns:
            Path to copied file
        """
        try:
            source_path = Path(source_path)
            
            if not target_name:
                target_name = source_path.name
            
            target_path = self.storage_path / target_name
            
            # Copy file
            await asyncio.to_thread(shutil.copy2, source_path, target_path)
            
            self.logger.info(f"Video copied to storage: {target_path}")
            return str(target_path)
            
        except Exception as e:
            self.logger.error(f"Error copying video to storage: {str(e)}")
            raise
    
    async def create_temp_file(self, suffix: str = '.tmp') -> str:
        """
        Create temporary file.
        
        Args:
            suffix: File suffix
            
        Returns:
            Path to temporary file
        """
        import tempfile
        
        try:
            fd, temp_path = tempfile.mkstemp(suffix=suffix, dir=self.temp_path)
            # Close the file descriptor
            import os
            os.close(fd)
            
            self.logger.debug(f"Created temporary file: {temp_path}")
            return temp_path
            
        except Exception as e:
            self.logger.error(f"Error creating temporary file: {str(e)}")
            raise
    
    async def cleanup_temp_files(self, max_age_hours: int = 24) -> None:
        """
        Clean up old temporary files.
        
        Args:
            max_age_hours: Maximum age of files to keep
        """
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for file_path in self.temp_path.glob('*'):
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age_seconds:
                        try:
                            file_path.unlink()
                            self.logger.debug(f"Cleaned up temp file: {file_path}")
                        except Exception as e:
                            self.logger.warning(f"Could not delete temp file {file_path}: {str(e)}")
            
        except Exception as e:
            self.logger.error(f"Error during temp cleanup: {str(e)}")
    
    async def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get file information.
        
        Args:
            file_path: Path to file
            
        Returns:
            File information dictionary
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            stat = file_path.stat()
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': file_path.suffix,
                'is_video': file_path.suffix.lower() in settings.supported_video_formats
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {str(e)}")
            return {'error': str(e)}
    
    async def validate_video_file(self, file_path: Union[str, Path]) -> bool:
        """
        Validate video file.
        
        Args:
            file_path: Path to video file
            
        Returns:
            True if valid video file
        """
        try:
            file_path = Path(file_path)
            
            # Check if file exists
            if not file_path.exists():
                return False
            
            # Check file extension
            if file_path.suffix.lower() not in settings.supported_video_formats:
                return False
            
            # Check file size
            if file_path.stat().st_size > settings.max_video_size:
                return False
            
            # Additional validation could be added here
            # (e.g., checking if file is actually a video using ffmpeg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating video file: {str(e)}")
            return False
    
    async def list_files(
        self,
        directory: Union[str, Path],
        pattern: str = '*',
        recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List files in directory.
        
        Args:
            directory: Directory to list
            pattern: File pattern to match
            recursive: Whether to search recursively
            
        Returns:
            List of file information dictionaries
        """
        try:
            directory = Path(directory)
            
            if not directory.exists():
                return []
            
            if recursive:
                files = directory.rglob(pattern)
            else:
                files = directory.glob(pattern)
            
            file_list = []
            for file_path in files:
                if file_path.is_file():
                    file_info = await self.get_file_info(file_path)
                    file_list.append(file_info)
            
            return file_list
            
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}")
            return []
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        try:
            stats = {}
            
            for name, path in [
                ('storage', self.storage_path),
                ('temp', self.temp_path),
                ('downloads', self.downloads_path),
                ('results', self.results_path)
            ]:
                if path.exists():
                    files = list(path.rglob('*'))
                    total_size = sum(f.stat().st_size for f in files if f.is_file())
                    
                    stats[name] = {
                        'path': str(path),
                        'total_files': len([f for f in files if f.is_file()]),
                        'total_size_bytes': total_size,
                        'total_size_mb': round(total_size / (1024 * 1024), 2)
                    }
                else:
                    stats[name] = {
                        'path': str(path),
                        'total_files': 0,
                        'total_size_bytes': 0,
                        'total_size_mb': 0
                    }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting storage stats: {str(e)}")
            return {'error': str(e)}
