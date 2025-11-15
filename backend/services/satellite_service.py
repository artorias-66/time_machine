import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import httpx
import base64
from config import settings

logger = logging.getLogger(__name__)


class SatelliteService:
    """
    Service for fetching satellite imagery from free APIs.
    
    This implementation uses synthetic data generation as a demonstration.
    In production, this would integrate with real APIs like:
    - Arlula Archive API
    - USGS Landsat
    - Sentinel Hub (with free tier)
    - NASA GIBS
    """
    
    def __init__(self):
        self.cache_dir = "cache"
        self.use_real_apis = bool(settings.arlula_key and settings.arlula_secret)
        # Tracks whether the last fetch used synthetic (dummy) data
        self.last_fetch_dummy_used = False
        if self.use_real_apis:
            logger.info("Real satellite APIs enabled")
        else:
            logger.info("Running in demo mode with synthetic imagery")
        
    async def fetch_images(
        self,
        bounds: Dict[str, float],
        start_date: str,
        end_date: str,
        cloud_cover: int = 30,
        visualization: str = "true-color"
    ) -> List[Dict]:
        """
        Fetch satellite images for the specified parameters.
        
        Tries real APIs first if credentials are available, otherwise uses demo mode.
        """
        try:
            # Try real satellite APIs first
            if self.use_real_apis:
                try:
                    logger.info("Attempting to fetch from Arlula API...")
                    images = await self.fetch_from_arlula(
                        bounds=bounds,
                        start_date=start_date,
                        end_date=end_date,
                        cloud_cover=cloud_cover,
                        visualization=visualization
                    )
                    if images:
                        logger.info(f"Successfully fetched {len(images)} images from Arlula")
                        # Mark as real data used
                        self.last_fetch_dummy_used = False
                        return images
                except Exception as e:
                    logger.warning(f"Arlula API failed, falling back to demo mode: {str(e)}")
            
            # Fall back to demo mode with synthetic imagery
            logger.info("Using demo mode with synthetic imagery")
            self.last_fetch_dummy_used = True
            return await self._fetch_synthetic_images(
                bounds=bounds,
                start_date=start_date,
                end_date=end_date,
                cloud_cover=cloud_cover,
                visualization=visualization
            )
            
        except Exception as e:
            logger.error(f"Error fetching images: {str(e)}")
            raise
    
    async def _fetch_synthetic_images(
        self,
        bounds: Dict[str, float],
        start_date: str,
        end_date: str,
        cloud_cover: int = 30,
        visualization: str = "true-color"
    ) -> List[Dict]:
        """Generate synthetic satellite imagery for demonstration."""
        try:
            # Parse dates
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            
            # Calculate number of images (roughly one per month)
            delta = end - start
            num_images = min(max(delta.days // 30, 3), 12)
            
            images = []
            
            # Generate images at regular intervals
            for i in range(num_images):
                # Calculate date for this image
                progress = i / (num_images - 1) if num_images > 1 else 0
                image_date = start + timedelta(days=delta.days * progress)
                
                # Generate synthetic image
                image_data = self._generate_synthetic_image(
                    bounds=bounds,
                    date=image_date,
                    visualization=visualization,
                    cloud_cover=cloud_cover,
                    frame_index=i,
                    total_frames=num_images
                )
                
                images.append({
                    'date': image_date.isoformat(),
                    'image': image_data,
                    'cloud_cover': random.randint(0, cloud_cover),
                    'bounds': bounds,
                    'source': 'synthetic'
                })
                
                # Simulate API delay
                await asyncio.sleep(0.1)
            
            return images
            
        except Exception as e:
            logger.error(f"Error fetching images: {str(e)}")
            raise
    
    def _generate_synthetic_image(
        self,
        bounds: Dict[str, float],
        date: datetime,
        visualization: str,
        cloud_cover: int,
        frame_index: int,
        total_frames: int
    ) -> Image.Image:
        """
        Generate a synthetic satellite image for demonstration.
        
        In production, this would be replaced with actual satellite data processing.
        """
        width, height = 800, 600
        
        # Create base image with varying colors based on visualization type
        if visualization == "ndvi":
            # NDVI: Green scale representing vegetation
            progress = frame_index / max(total_frames - 1, 1)
            base_color = int(100 + 100 * np.sin(progress * np.pi))
            img = Image.new('RGB', (width, height), (0, base_color, 0))
        elif visualization == "false-color":
            # False color: More vibrant, shifted spectrum
            progress = frame_index / max(total_frames - 1, 1)
            r = int(150 + 50 * np.sin(progress * np.pi))
            g = int(100 + 50 * np.cos(progress * np.pi))
            b = int(180 + 50 * np.sin(progress * np.pi * 2))
            img = Image.new('RGB', (width, height), (r, g, b))
        else:
            # True color: Earth-like colors
            progress = frame_index / max(total_frames - 1, 1)
            # Simulate seasonal changes
            green = int(100 + 100 * np.sin(progress * np.pi))
            brown = int(140 - 40 * np.sin(progress * np.pi))
            img = Image.new('RGB', (width, height), (brown, green, 80))
        
        # Add some texture/noise
        pixels = np.array(img)
        noise = np.random.randint(-20, 20, pixels.shape, dtype=np.int16)
        pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(pixels)
        
        # Add some geometric patterns to simulate landscape features
        draw = ImageDraw.Draw(img)
        
        # Simulate rivers, roads, or field boundaries
        for _ in range(random.randint(3, 8)):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            color = tuple(np.clip(np.array([random.randint(50, 150) for _ in range(3)]), 0, 255))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=random.randint(2, 5))
        
        # Add rectangular patches (fields, buildings)
        for _ in range(random.randint(5, 15)):
            x = random.randint(0, width - 100)
            y = random.randint(0, height - 100)
            w = random.randint(30, 100)
            h = random.randint(30, 100)
            
            # Color varies with season/frame
            base = pixels[y:y+h, x:x+w].mean(axis=(0, 1)).astype(int)
            variation = random.randint(-30, 30)
            color = tuple(np.clip(base + variation, 0, 255))
            
            draw.rectangle([x, y, x+w, y+h], fill=color, outline=None)
        
        # Add clouds based on cloud_cover parameter
        if random.randint(0, 100) < cloud_cover:
            for _ in range(random.randint(1, 3)):
                x = random.randint(0, width)
                y = random.randint(0, height)
                radius = random.randint(50, 150)
                # Semi-transparent white clouds
                cloud_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                cloud_draw = ImageDraw.Draw(cloud_overlay)
                cloud_draw.ellipse(
                    [x-radius, y-radius, x+radius, y+radius],
                    fill=(255, 255, 255, 150)
                )
                img = Image.alpha_composite(img.convert('RGBA'), cloud_overlay).convert('RGB')
        
        return img
    
    async def fetch_from_arlula(
        self,
        bounds: Dict[str, float],
        start_date: str,
        end_date: str,
        cloud_cover: int = 30,
        visualization: str = "true-color"
    ) -> List[Dict]:
        """
        Fetch satellite imagery from Arlula Archive API.
        
        Uses Landsat-8 data from Arlula's archive.
        """
        try:
            # Create authentication header
            auth_string = f"{settings.arlula_key}:{settings.arlula_secret}"
            auth_bytes = auth_string.encode('ascii')
            base64_bytes = base64.b64encode(auth_bytes)
            base64_auth = base64_bytes.decode('ascii')
            
            headers = {
                "Authorization": f"Basic {base64_auth}",
                "Content-Type": "application/json"
            }
            
            # Arlula API endpoint
            search_url = "https://api.arlula.com/api/archive/search"
            
            # Build search request with polygon (Arlula format)
            # Convert bounds to polygon format: [[west,south], [east,south], [east,north], [west,north], [west,south]]
            polygon = [
                [
                    [bounds["west"], bounds["south"]],
                    [bounds["east"], bounds["south"]],
                    [bounds["east"], bounds["north"]],
                    [bounds["west"], bounds["north"]],
                    [bounds["west"], bounds["south"]]
                ]
            ]
            
            search_payload = {
                "start": start_date,
                "end": end_date,
                "polygon": polygon,
                "cloud": cloud_cover,
                "gsd": 30,  # Ground Sample Distance in meters (Landsat ~30m)
                "offNadir": 10
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Search for available imagery
                logger.info(f"Searching Arlula for imagery: {search_payload}")
                search_response = await client.post(
                    search_url,
                    headers=headers,
                    json=search_payload
                )
                
                if search_response.status_code != 200:
                    logger.error(f"Arlula search failed: {search_response.text}")
                    return []
                
                search_results = search_response.json()
                logger.info(f"Arlula returned {len(search_results.get('results', []))} results")
                
                if not search_results.get('results'):
                    logger.warning("No Arlula results found, using demo mode")
                    return []
                
                # Filter for Landsat scenes only (like in working test)
                landsat_scenes = [r for r in search_results['results'] if r.get('supplier') == 'landsat']
                logger.info(f"Filtered to {len(landsat_scenes)} Landsat scenes (from {len(search_results['results'])} total)")
                
                # Process results into images - DOWNLOAD REAL THUMBNAILS
                images = []
                # Respect max images per request from settings
                cfg_value = getattr(settings, 'max_images_per_request', 20)
                try:
                    max_images = int(cfg_value) if cfg_value is not None else 20
                except Exception:
                    max_images = 20

                # If max_images <= 0, treat as unlimited (no slicing)
                iterable = landsat_scenes if max_images <= 0 else landsat_scenes[:max_images]
                for result in iterable:
                    try:
                        scene_date = result.get('date', start_date)
                        cloud_pct = result.get('cloud', 0)
                        scene_id = result.get('id', 'unknown')
                        thumbnail_url = result.get('thumbnail')
                        
                        if not thumbnail_url:
                            logger.warning(f"No thumbnail URL for scene {scene_id}")
                            continue
                        
                        # Download actual satellite thumbnail (with auth and follow redirects)
                        logger.info(f"Downloading thumbnail for scene {scene_id}...")
                        thumb_response = await client.get(
                            thumbnail_url,
                            timeout=30.0,
                            headers={
                                'Authorization': headers['Authorization'],  # Use same auth
                                'User-Agent': 'Mozilla/5.0'
                            },
                            follow_redirects=True  # Follow 303 redirects
                        )
                        
                        if thumb_response.status_code != 200:
                            logger.warning(f"Failed to download thumbnail: {thumb_response.status_code}")
                            continue
                        
                        if len(thumb_response.content) < 100:
                            logger.warning(f"Thumbnail too small, likely empty")
                            continue
                        
                        # Load image from bytes (same as working test)
                        image_data = Image.open(io.BytesIO(thumb_response.content))
                        logger.info(f"   Loaded image: {image_data.size}, mode: {image_data.mode}")
                        
                        # Keep original size (don't resize yet - let timelapse service handle it)
                        # Just ensure RGB mode
                        if image_data.mode != 'RGB':
                            image_data = image_data.convert('RGB')
                            logger.info(f"   Converted to RGB mode")
                        
                        images.append({
                            'date': scene_date.split('T')[0],
                            'image': image_data,
                            'cloud_cover': int(cloud_pct),
                            'bounds': bounds,
                            'source': 'arlula',
                            'scene_id': scene_id
                        })
                        
                        logger.info(f"✓ Downloaded real satellite image: {scene_id} from {scene_date.split('T')[0]}")
                        
                    except Exception as e:
                        logger.warning(f"Failed to process Arlula result: {str(e)}")
                        continue
                
                return images
                
        except httpx.TimeoutException:
            logger.error("Arlula API timeout")
            return []
        except Exception as e:
            logger.error(f"Arlula API error: {str(e)}")
            return []
    
    async def fetch_from_usgs(self, bounds: Dict, start_date: str, end_date: str):
        """
        Placeholder for USGS Landsat API integration.
        
        To implement:
        1. Use USGS Earth Explorer API
        2. Or use landsatxplore Python package
        """
        pass


