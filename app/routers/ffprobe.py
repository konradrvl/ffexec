from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import subprocess
import shutil

router = APIRouter()

class FFprobeCommand(BaseModel):
    """
    Model for FFprobe command execution
    """
    args: List[str]

class FFprobeResponse(BaseModel):
    """
    Response model for FFprobe operations
    """
    success: bool
    command: str
    stdout: str
    stderr: str
    return_code: int

@router.post("/ffprobe", response_model=FFprobeResponse)
async def execute_ffprobe_command(command: FFprobeCommand):
    """
    Execute FFprobe with the provided arguments
    """
    if not shutil.which("ffprobe"):
        raise HTTPException(status_code=500, detail="FFprobe not found on system")
    
    # Build the command
    cmd = ["ffprobe"] + command.args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        return FFprobeResponse(
            success=result.returncode == 0,
            command=" ".join(cmd),
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode
        )
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="FFprobe command timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing FFprobe: {str(e)}")