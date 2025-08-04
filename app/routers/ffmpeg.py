from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import subprocess
import shutil

router = APIRouter()

class FFmpegCommand(BaseModel):
    """
    Model for FFmpeg command execution
    """
    args: List[str]

class FFmpegResponse(BaseModel):
    """
    Response model for FFmpeg operations
    """
    success: bool
    command: str
    stdout: str
    stderr: str
    return_code: int

@router.post("/ffmpeg", response_model=FFmpegResponse)
async def execute_ffmpeg_command(command: FFmpegCommand):
    """
    Execute FFmpeg with the provided arguments
    """
    if not shutil.which("ffmpeg"):
        raise HTTPException(status_code=500, detail="FFmpeg not found on system")
    
    # Build the command
    cmd = ["ffmpeg"] + command.args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return FFmpegResponse(
            success=result.returncode == 0,
            command=" ".join(cmd),
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode
        )
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="FFmpeg command timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing FFmpeg: {str(e)}")