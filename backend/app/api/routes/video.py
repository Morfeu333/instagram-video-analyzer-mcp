"""
Video processing API routes.
"""
import uuid
import asyncio
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl

from ...core.database import get_db
from ...models import VideoJob, JobStatus
from ...services import InstagramDownloader, VideoAnalyzer, FileManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/video", tags=["video"])

# Pydantic models for request/response
class VideoAnalysisRequest(BaseModel):
    instagram_url: str
    analysis_type: str = "comprehensive"

class VideoAnalysisResponse(BaseModel):
    job_id: str
    status: str
    message: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    created_at: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str]
    analysis_result: Optional[dict]


# Global service instances
instagram_downloader = InstagramDownloader()
video_analyzer = VideoAnalyzer()
file_manager = FileManager()


async def process_video_job(job_id: str, instagram_url: str, analysis_type: str, db: Session):
    """
    Background task to process video analysis job.
    
    Args:
        job_id: Unique job identifier
        instagram_url: Instagram post URL
        analysis_type: Type of analysis to perform
        db: Database session
    """
    try:
        # Get job from database
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if not job:
            logger.error(f"Job not found: {job_id}")
            return
        
        # Update job status to processing
        job.status = JobStatus.PROCESSING
        job.started_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Starting video processing for job: {job_id}")
        
        # Create job directory
        job_dir = file_manager.get_job_directory(job_id)
        
        # Download video
        def download_progress(progress: float):
            job.download_progress = progress
            db.commit()
        
        success, video_path, error_msg = instagram_downloader.download_video(
            instagram_url, 
            str(job_dir),
            progress_callback=download_progress
        )
        
        if not success:
            job.status = JobStatus.FAILED
            job.error_message = error_msg
            job.completed_at = datetime.utcnow()
            db.commit()
            logger.error(f"Video download failed for job {job_id}: {error_msg}")
            return
        
        # Update job with video info
        job.video_path = video_path
        video_info = file_manager.get_video_info(video_path)
        job.video_size = video_info.get("size", 0)
        job.video_filename = video_info.get("filename", "")
        db.commit()
        
        # Analyze video
        def analysis_progress(progress: float):
            job.analysis_progress = progress
            db.commit()
        
        analysis_result = video_analyzer.analyze_video(
            video_path,
            analysis_type,
            progress_callback=analysis_progress
        )
        
        # Save analysis result
        result_path = file_manager.save_analysis_result(job_id, analysis_result)
        
        # Update job with results
        job.status = JobStatus.COMPLETED
        job.analysis_result = analysis_result.get("raw_response", "")
        job.result_path = result_path
        job.completed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Video processing completed for job: {job_id}")
        
    except Exception as e:
        logger.error(f"Error processing video job {job_id}: {e}")
        
        # Update job with error
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()


@router.post("/analyze", response_model=VideoAnalysisResponse)
async def analyze_video(
    request: VideoAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start video analysis job.
    
    Args:
        request: Video analysis request
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Job information
    """
    try:
        # Validate Instagram URL
        if "instagram.com" not in request.instagram_url:
            raise HTTPException(status_code=400, detail="Invalid Instagram URL")
        
        # Check if URL contains video
        post_info = instagram_downloader.get_post_info(request.instagram_url)
        if not post_info:
            raise HTTPException(status_code=400, detail="Could not access Instagram post")
        
        if not post_info.get("is_video", False):
            raise HTTPException(status_code=400, detail="Instagram post does not contain a video")
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Create job record
        job = VideoJob(
            job_id=job_id,
            instagram_url=request.instagram_url,
            status=JobStatus.PENDING
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Start background processing
        background_tasks.add_task(
            process_video_job,
            job_id,
            request.instagram_url,
            request.analysis_type,
            db
        )
        
        logger.info(f"Created video analysis job: {job_id}")
        
        return VideoAnalysisResponse(
            job_id=job_id,
            status="pending",
            message="Video analysis job started successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating video analysis job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Get job status and results.
    
    Args:
        job_id: Unique job identifier
        db: Database session
        
    Returns:
        Job status information
    """
    try:
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Calculate overall progress
        if job.status == JobStatus.PENDING:
            progress = 0.0
        elif job.status == JobStatus.PROCESSING:
            progress = (job.download_progress + job.analysis_progress) / 2
        elif job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
            progress = 1.0
        else:
            progress = 0.0
        
        # Load full analysis result if completed
        analysis_result = None
        if job.status == JobStatus.COMPLETED and job.result_path:
            analysis_result = file_manager.load_analysis_result(job_id)
        
        return JobStatusResponse(
            job_id=job.job_id,
            status=job.status.value,
            progress=progress,
            created_at=job.created_at.isoformat() if job.created_at else None,
            started_at=job.started_at.isoformat() if job.started_at else None,
            completed_at=job.completed_at.isoformat() if job.completed_at else None,
            error_message=job.error_message,
            analysis_result=analysis_result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
