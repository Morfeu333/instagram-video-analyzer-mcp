"""
Job management API routes.
"""
import logging
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel

from ...core.database import get_db
from ...models import VideoJob, JobStatus
from ...services import FileManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Pydantic models
class JobSummary(BaseModel):
    job_id: str
    instagram_url: str
    status: str
    created_at: Optional[str]
    completed_at: Optional[str]
    video_filename: Optional[str]
    error_message: Optional[str]

class JobListResponse(BaseModel):
    jobs: List[JobSummary]
    total: int
    page: int
    per_page: int

class SystemStatsResponse(BaseModel):
    total_jobs: int
    pending_jobs: int
    processing_jobs: int
    completed_jobs: int
    failed_jobs: int
    disk_usage: dict

# Global service instances
file_manager = FileManager()


@router.get("/", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """
    List video processing jobs with pagination.
    
    Args:
        page: Page number (1-based)
        per_page: Number of items per page
        status: Optional status filter
        db: Database session
        
    Returns:
        Paginated list of jobs
    """
    try:
        # Build query
        query = db.query(VideoJob)
        
        # Apply status filter if provided
        if status:
            try:
                status_enum = JobStatus(status.lower())
                query = query.filter(VideoJob.status == status_enum)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        jobs = query.order_by(desc(VideoJob.created_at)).offset((page - 1) * per_page).limit(per_page).all()
        
        # Convert to response format
        job_summaries = [
            JobSummary(
                job_id=job.job_id,
                instagram_url=job.instagram_url,
                status=job.status.value,
                created_at=job.created_at.isoformat() if job.created_at else None,
                completed_at=job.completed_at.isoformat() if job.completed_at else None,
                video_filename=job.video_filename,
                error_message=job.error_message
            )
            for job in jobs
        ]
        
        return JobListResponse(
            jobs=job_summaries,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    cleanup_files: bool = Query(True, description="Whether to cleanup associated files"),
    db: Session = Depends(get_db)
):
    """
    Delete a video processing job.
    
    Args:
        job_id: Unique job identifier
        cleanup_files: Whether to cleanup associated files
        db: Database session
        
    Returns:
        Success message
    """
    try:
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Cleanup files if requested
        if cleanup_files:
            file_manager.cleanup_job_files(job_id, keep_results=False)
        
        # Delete job from database
        db.delete(job)
        db.commit()
        
        logger.info(f"Deleted job: {job_id}")
        
        return {"message": "Job deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(db: Session = Depends(get_db)):
    """
    Get system statistics.
    
    Args:
        db: Database session
        
    Returns:
        System statistics
    """
    try:
        # Get job counts by status
        total_jobs = db.query(VideoJob).count()
        pending_jobs = db.query(VideoJob).filter(VideoJob.status == JobStatus.PENDING).count()
        processing_jobs = db.query(VideoJob).filter(VideoJob.status == JobStatus.PROCESSING).count()
        completed_jobs = db.query(VideoJob).filter(VideoJob.status == JobStatus.COMPLETED).count()
        failed_jobs = db.query(VideoJob).filter(VideoJob.status == JobStatus.FAILED).count()
        
        # Get disk usage
        disk_usage = file_manager.get_disk_usage()
        
        return SystemStatsResponse(
            total_jobs=total_jobs,
            pending_jobs=pending_jobs,
            processing_jobs=processing_jobs,
            completed_jobs=completed_jobs,
            failed_jobs=failed_jobs,
            disk_usage=disk_usage
        )
        
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{job_id}/cancel")
async def cancel_job(job_id: str, db: Session = Depends(get_db)):
    """
    Cancel a pending or processing job.
    
    Args:
        job_id: Unique job identifier
        db: Database session
        
    Returns:
        Success message
    """
    try:
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.status not in [JobStatus.PENDING, JobStatus.PROCESSING]:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot cancel job with status: {job.status.value}"
            )
        
        # Update job status
        job.status = JobStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Cancelled job: {job_id}")
        
        return {"message": "Job cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
