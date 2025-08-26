"""
File management service for handling video files and results.
"""
import os
import json
import shutil
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from ..core.config import settings

logger = logging.getLogger(__name__)


class FileManager:
    """File management service."""
    
    def __init__(self):
        """Initialize file manager."""
        self.upload_dir = Path(settings.upload_dir)
        self.results_dir = Path(settings.results_dir)
        self.temp_dir = Path(settings.temp_dir)
        
        # Ensure directories exist
        for directory in [self.upload_dir, self.results_dir, self.temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_job_directory(self, job_id: str) -> Path:
        """
        Get or create directory for a specific job.
        
        Args:
            job_id: Unique job identifier
            
        Returns:
            Path to job directory
        """
        job_dir = self.upload_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        return job_dir
    
    def save_analysis_result(self, job_id: str, analysis_result: Dict[str, Any]) -> str:
        """
        Save analysis result to file.
        
        Args:
            job_id: Unique job identifier
            analysis_result: Analysis result dictionary
            
        Returns:
            Path to saved result file
        """
        try:
            result_file = self.results_dir / f"{job_id}_analysis.json"
            
            # Add metadata
            result_with_metadata = {
                "job_id": job_id,
                "timestamp": datetime.utcnow().isoformat(),
                "analysis": analysis_result
            }
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_with_metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Analysis result saved: {result_file}")
            return str(result_file)
            
        except Exception as e:
            logger.error(f"Error saving analysis result: {e}")
            raise
    
    def load_analysis_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Load analysis result from file.
        
        Args:
            job_id: Unique job identifier
            
        Returns:
            Analysis result dictionary or None if not found
        """
        try:
            result_file = self.results_dir / f"{job_id}_analysis.json"
            
            if not result_file.exists():
                return None
            
            with open(result_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Error loading analysis result: {e}")
            return None
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """
        Get basic information about a video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video information
        """
        try:
            file_path = Path(video_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            stat = file_path.stat()
            
            return {
                "filename": file_path.name,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "extension": file_path.suffix.lower(),
                "path": str(file_path.absolute())
            }
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}
    
    def cleanup_job_files(self, job_id: str, keep_results: bool = True) -> bool:
        """
        Clean up files associated with a job.
        
        Args:
            job_id: Unique job identifier
            keep_results: Whether to keep result files
            
        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            # Clean up job directory (videos and temp files)
            job_dir = self.upload_dir / job_id
            if job_dir.exists():
                shutil.rmtree(job_dir)
                logger.info(f"Cleaned up job directory: {job_dir}")
            
            # Optionally clean up results
            if not keep_results:
                result_file = self.results_dir / f"{job_id}_analysis.json"
                if result_file.exists():
                    result_file.unlink()
                    logger.info(f"Cleaned up result file: {result_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning up job files: {e}")
            return False
    
    def get_disk_usage(self) -> Dict[str, Any]:
        """
        Get disk usage information for managed directories.
        
        Returns:
            Dictionary with disk usage information
        """
        try:
            usage = {}
            
            for name, directory in [
                ("upload", self.upload_dir),
                ("results", self.results_dir),
                ("temp", self.temp_dir)
            ]:
                if directory.exists():
                    total_size = sum(
                        f.stat().st_size for f in directory.rglob('*') if f.is_file()
                    )
                    file_count = sum(1 for f in directory.rglob('*') if f.is_file())
                    
                    usage[name] = {
                        "path": str(directory),
                        "total_size": total_size,
                        "total_size_mb": round(total_size / (1024 * 1024), 2),
                        "file_count": file_count
                    }
                else:
                    usage[name] = {
                        "path": str(directory),
                        "total_size": 0,
                        "total_size_mb": 0,
                        "file_count": 0
                    }
            
            return usage
            
        except Exception as e:
            logger.error(f"Error getting disk usage: {e}")
            return {}
