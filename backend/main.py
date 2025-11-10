from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime
import logging

from services.satellite_service import SatelliteService
from services.timelapse_service import TimelapseService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Time Machine for Earth API",
    description="Generate timelapse visualizations from satellite imagery",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
os.makedirs("output", exist_ok=True)
os.makedirs("cache", exist_ok=True)

# Initialize services (BEFORE mounting static files)
satellite_service = SatelliteService()
timelapse_service = TimelapseService()


class AOIGeometry(BaseModel):
    type: str
    coordinates: List


class AOIProperties(BaseModel):
    bounds: dict


class AOI(BaseModel):
    type: str
    geometry: AOIGeometry
    properties: AOIProperties


class TimelapseRequest(BaseModel):
    aoi: AOI
    start_date: str
    end_date: str
    cloud_cover: int = 30
    output_format: str = "gif"
    add_timestamps: bool = True
    visualization: str = "true-color"


@app.get("/")
async def root():
    return {
        "message": "Time Machine for Earth API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/generate-timelapse")
async def generate_timelapse(request: TimelapseRequest):
    """
    Generate a timelapse from satellite imagery for the specified AOI and date range.
    """
    try:
        logger.info(f"Generating timelapse for date range: {request.start_date} to {request.end_date}")
        
        # Extract bounds
        bounds = request.aoi.properties.bounds
        
        # Fetch satellite images
        logger.info("Fetching satellite imagery...")
        images = await satellite_service.fetch_images(
            bounds=bounds,
            start_date=request.start_date,
            end_date=request.end_date,
            cloud_cover=request.cloud_cover,
            visualization=request.visualization
        )
        
        if not images:
            raise HTTPException(
                status_code=404,
                detail="No suitable satellite images found for the specified parameters. Try increasing cloud cover or expanding date range."
            )
        
        logger.info(f"Found {len(images)} images")
        
        # Generate timelapse
        logger.info("Generating timelapse...")
        result = await timelapse_service.create_timelapse(
            images=images,
            output_format=request.output_format,
            add_timestamps=request.add_timestamps,
            visualization=request.visualization
        )
        
        return {
            "url": f"/output/{result['filename']}",
            "frame_count": result['frame_count'],
            "date_range": f"{request.start_date} to {request.end_date}",
            "format": request.output_format,
            "visualization": request.visualization,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating timelapse: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate timelapse: {str(e)}"
        )


@app.delete("/api/cache/clear")
async def clear_cache():
    """Clear cached data and temporary files."""
    try:
        import shutil
        cache_dir = "cache"
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            os.makedirs(cache_dir)
        
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files AFTER all API routes are defined
app.mount("/output", StaticFiles(directory="output"), name="output")

# Serve frontend static files (for production) - MUST be last!
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


