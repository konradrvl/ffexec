from fastapi import APIRouter
from datetime import datetime
import subprocess
import shutil

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ffexec-api"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check that also verifies FFmpeg and FFprobe availability
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ffexec-api",
        "dependencies": {}
    }
    
    # Check FFmpeg availability
    ffmpeg_available = shutil.which("ffmpeg") is not None
    if ffmpeg_available:
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            ffmpeg_version = result.stdout.split('\n')[0] if result.returncode == 0 else "unknown"
        except Exception:
            ffmpeg_available = False
            ffmpeg_version = "unavailable"
    else:
        ffmpeg_version = "not found"
    
    # Check FFprobe availability
    ffprobe_available = shutil.which("ffprobe") is not None
    if ffprobe_available:
        try:
            result = subprocess.run(
                ["ffprobe", "-version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            ffprobe_version = result.stdout.split('\n')[0] if result.returncode == 0 else "unknown"
        except Exception:
            ffprobe_available = False
            ffprobe_version = "unavailable"
    else:
        ffprobe_version = "not found"
    
    health_status["dependencies"] = {
        "ffmpeg": {
            "available": ffmpeg_available,
            "version": ffmpeg_version
        },
        "ffprobe": {
            "available": ffprobe_available,
            "version": ffprobe_version
        }
    }
    
    # Overall status based on dependencies
    if not ffmpeg_available or not ffprobe_available:
        health_status["status"] = "degraded"
    
    return health_status