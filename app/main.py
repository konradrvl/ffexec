from fastapi import FastAPI
from app.routers import ffmpeg, ffprobe, health

app = FastAPI(
    title="ffexec API",
    description="A FastAPI application for FFmpeg and FFprobe operations",
    version="1.0.0"
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(ffmpeg.router, tags=["ffmpeg"])
app.include_router(ffprobe.router, tags=["ffprobe"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
