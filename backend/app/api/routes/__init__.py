"""
API routes package.
"""
from .video import router as video_router
from .jobs import router as jobs_router

__all__ = ["video_router", "jobs_router"]
