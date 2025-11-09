from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # API Configuration
    api_title: str = "Time Machine for Earth"
    api_version: str = "1.0.0"
    
    # CORS
    cors_origins: list = ["*"]
    
    # Satellite API Keys (add your keys here)
    arlula_api_key: Optional[str] = None
    usgs_username: Optional[str] = None
    usgs_password: Optional[str] = None
    sentinel_hub_client_id: Optional[str] = None
    sentinel_hub_client_secret: Optional[str] = None
    
    # Processing
    max_images_per_request: int = 20
    max_aoi_size_km2: int = 10000
    
    # Storage
    output_dir: str = "output"
    cache_dir: str = "cache"
    max_cache_size_mb: int = 1000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


