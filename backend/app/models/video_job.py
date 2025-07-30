"""
Database models for video processing jobs.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, Float
from sqlalchemy.sql import func
from datetime import datetime
import enum

from ..core.database import Base


class JobStatus(str, enum.Enum):
    """Job status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VideoJob(Base):
    """Video processing job model."""
    
    __tablename__ = "video_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Job identification
    job_id = Column(String(36), unique=True, index=True, nullable=False)
    
    # Input information
    instagram_url = Column(String(500), nullable=False)
    video_filename = Column(String(255), nullable=True)
    
    # Job status and timing
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Processing information
    download_progress = Column(Float, default=0.0)
    analysis_progress = Column(Float, default=0.0)
    
    # Results
    analysis_result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # File paths
    video_path = Column(String(500), nullable=True)
    result_path = Column(String(500), nullable=True)
    
    # Metadata
    video_duration = Column(Float, nullable=True)
    video_size = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<VideoJob(id={self.id}, job_id='{self.job_id}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "job_id": self.job_id,
            "instagram_url": self.instagram_url,
            "video_filename": self.video_filename,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "download_progress": self.download_progress,
            "analysis_progress": self.analysis_progress,
            "analysis_result": self.analysis_result,
            "error_message": self.error_message,
            "video_path": self.video_path,
            "result_path": self.result_path,
            "video_duration": self.video_duration,
            "video_size": self.video_size,
        }
