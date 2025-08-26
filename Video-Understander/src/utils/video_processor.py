"""
Video processing utilities.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import cv2
import ffmpeg

from config.settings import settings


class VideoProcessor:
    """Video processing utilities."""
    
    def __init__(self):
        """Initialize the video processor."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("VideoProcessor initialized")
    
    async def get_video_metadata(self, video_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get video metadata using ffmpeg.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Video metadata dictionary
        """
        try:
            video_path = Path(video_path)
            
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Use ffmpeg to get metadata
            probe = await asyncio.to_thread(
                ffmpeg.probe, str(video_path)
            )
            
            video_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                None
            )
            
            audio_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'audio'),
                None
            )
            
            format_info = probe.get('format', {})
            
            metadata = {
                'filename': video_path.name,
                'filepath': str(video_path),
                'filesize': int(format_info.get('size', 0)),
                'filesize_mb': round(int(format_info.get('size', 0)) / (1024 * 1024), 2),
                'duration': float(format_info.get('duration', 0)),
                'duration_formatted': self._format_duration(float(format_info.get('duration', 0))),
                'bitrate': int(format_info.get('bit_rate', 0)),
                'format_name': format_info.get('format_name', ''),
                'format_long_name': format_info.get('format_long_name', ''),
            }
            
            if video_stream:
                metadata.update({
                    'video_codec': video_stream.get('codec_name', ''),
                    'video_width': int(video_stream.get('width', 0)),
                    'video_height': int(video_stream.get('height', 0)),
                    'video_fps': self._parse_fps(video_stream.get('r_frame_rate', '0/1')),
                    'video_bitrate': int(video_stream.get('bit_rate', 0)),
                    'pixel_format': video_stream.get('pix_fmt', ''),
                    'aspect_ratio': video_stream.get('display_aspect_ratio', ''),
                })
            
            if audio_stream:
                metadata.update({
                    'audio_codec': audio_stream.get('codec_name', ''),
                    'audio_sample_rate': int(audio_stream.get('sample_rate', 0)),
                    'audio_channels': int(audio_stream.get('channels', 0)),
                    'audio_bitrate': int(audio_stream.get('bit_rate', 0)),
                })
            
            # Additional computed fields
            metadata['has_video'] = video_stream is not None
            metadata['has_audio'] = audio_stream is not None
            metadata['is_valid'] = self._validate_video_metadata(metadata)
            
            self.logger.info(f"Video metadata extracted: {video_path.name}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error getting video metadata: {str(e)}")
            return {
                'filename': video_path.name if isinstance(video_path, Path) else str(video_path),
                'error': str(e),
                'is_valid': False
            }
    
    async def extract_frames(
        self,
        video_path: Union[str, Path],
        output_dir: Union[str, Path],
        fps: float = 1.0,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> List[str]:
        """
        Extract frames from video.
        
        Args:
            video_path: Path to video file
            output_dir: Directory to save frames
            fps: Frames per second to extract
            start_time: Start time in seconds
            end_time: End time in seconds
            
        Returns:
            List of frame file paths
        """
        try:
            video_path = Path(video_path)
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Build ffmpeg command
            input_stream = ffmpeg.input(str(video_path))
            
            # Apply time filters if specified
            if start_time is not None:
                input_stream = input_stream.filter('ss', start_time)
            
            if end_time is not None:
                duration = end_time - (start_time or 0)
                input_stream = input_stream.filter('t', duration)
            
            # Extract frames
            output_pattern = str(output_dir / f"{video_path.stem}_frame_%04d.jpg")
            
            stream = input_stream.filter('fps', fps=fps)
            stream = ffmpeg.output(stream, output_pattern)
            
            await asyncio.to_thread(ffmpeg.run, stream, overwrite_output=True, quiet=True)
            
            # Get list of extracted frames
            frame_files = sorted(output_dir.glob(f"{video_path.stem}_frame_*.jpg"))
            frame_paths = [str(f) for f in frame_files]
            
            self.logger.info(f"Extracted {len(frame_paths)} frames from {video_path.name}")
            return frame_paths
            
        except Exception as e:
            self.logger.error(f"Error extracting frames: {str(e)}")
            return []
    
    async def get_video_thumbnail(
        self,
        video_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        timestamp: float = 1.0
    ) -> Optional[str]:
        """
        Extract thumbnail from video.
        
        Args:
            video_path: Path to video file
            output_path: Output path for thumbnail
            timestamp: Time in seconds to extract thumbnail
            
        Returns:
            Path to thumbnail file
        """
        try:
            video_path = Path(video_path)
            
            if not output_path:
                output_path = video_path.parent / f"{video_path.stem}_thumbnail.jpg"
            else:
                output_path = Path(output_path)
            
            # Extract thumbnail using ffmpeg
            stream = ffmpeg.input(str(video_path), ss=timestamp)
            stream = ffmpeg.output(stream, str(output_path), vframes=1)
            
            await asyncio.to_thread(ffmpeg.run, stream, overwrite_output=True, quiet=True)
            
            if output_path.exists():
                self.logger.info(f"Thumbnail extracted: {output_path}")
                return str(output_path)
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error extracting thumbnail: {str(e)}")
            return None
    
    async def trim_video(
        self,
        video_path: Union[str, Path],
        output_path: Union[str, Path],
        start_time: float,
        end_time: float
    ) -> bool:
        """
        Trim video to specified time range.
        
        Args:
            video_path: Path to input video
            output_path: Path to output video
            start_time: Start time in seconds
            end_time: End time in seconds
            
        Returns:
            True if successful
        """
        try:
            video_path = Path(video_path)
            output_path = Path(output_path)
            
            duration = end_time - start_time
            
            stream = ffmpeg.input(str(video_path), ss=start_time, t=duration)
            stream = ffmpeg.output(stream, str(output_path))
            
            await asyncio.to_thread(ffmpeg.run, stream, overwrite_output=True, quiet=True)
            
            if output_path.exists():
                self.logger.info(f"Video trimmed: {output_path}")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error trimming video: {str(e)}")
            return False
    
    async def convert_video_format(
        self,
        video_path: Union[str, Path],
        output_path: Union[str, Path],
        output_format: str = 'mp4',
        video_codec: str = 'libx264',
        audio_codec: str = 'aac'
    ) -> bool:
        """
        Convert video to different format.
        
        Args:
            video_path: Path to input video
            output_path: Path to output video
            output_format: Output format
            video_codec: Video codec
            audio_codec: Audio codec
            
        Returns:
            True if successful
        """
        try:
            video_path = Path(video_path)
            output_path = Path(output_path)
            
            stream = ffmpeg.input(str(video_path))
            stream = ffmpeg.output(
                stream,
                str(output_path),
                vcodec=video_codec,
                acodec=audio_codec,
                format=output_format
            )
            
            await asyncio.to_thread(ffmpeg.run, stream, overwrite_output=True, quiet=True)
            
            if output_path.exists():
                self.logger.info(f"Video converted: {output_path}")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error converting video: {str(e)}")
            return False
    
    def _parse_fps(self, fps_string: str) -> float:
        """Parse FPS from string format like '30/1'."""
        try:
            if '/' in fps_string:
                num, den = fps_string.split('/')
                return float(num) / float(den)
            else:
                return float(fps_string)
        except:
            return 0.0
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to HH:MM:SS format."""
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{secs:02d}"
            else:
                return f"{minutes:02d}:{secs:02d}"
        except:
            return "00:00"
    
    def _validate_video_metadata(self, metadata: Dict[str, Any]) -> bool:
        """Validate video metadata."""
        try:
            # Check required fields
            required_fields = ['duration', 'filesize', 'has_video']
            for field in required_fields:
                if field not in metadata:
                    return False
            
            # Check if it's actually a video
            if not metadata.get('has_video', False):
                return False
            
            # Check duration
            if metadata.get('duration', 0) <= 0:
                return False
            
            # Check file size
            if metadata.get('filesize', 0) <= 0:
                return False
            
            # Check if duration exceeds limits
            if metadata.get('duration', 0) > settings.max_video_duration:
                self.logger.warning(f"Video duration exceeds limit: {metadata.get('duration')}s")
                return False
            
            # Check if file size exceeds limits
            if metadata.get('filesize', 0) > settings.max_video_size:
                self.logger.warning(f"Video file size exceeds limit: {metadata.get('filesize')} bytes")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating metadata: {str(e)}")
            return False
    
    async def get_video_info_opencv(self, video_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get basic video info using OpenCV (fallback method).
        
        Args:
            video_path: Path to video file
            
        Returns:
            Video information dictionary
        """
        try:
            video_path = str(video_path)
            
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video: {video_path}")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                'width': width,
                'height': height,
                'fps': fps,
                'frame_count': frame_count,
                'duration': duration,
                'duration_formatted': self._format_duration(duration)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting video info with OpenCV: {str(e)}")
            return {'error': str(e)}
