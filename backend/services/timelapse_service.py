import os
import logging
from datetime import datetime
from typing import List, Dict
from PIL import Image, ImageDraw, ImageFont
import imageio
from pathlib import Path

logger = logging.getLogger(__name__)


class TimelapseService:
    """Service for creating timelapse animations from satellite images."""
    
    def __init__(self):
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def create_timelapse(
        self,
        images: List[Dict],
        output_format: str = "gif",
        add_timestamps: bool = True,
        visualization: str = "true-color"
    ) -> Dict:
        """
        Create a timelapse animation from a list of satellite images.
        
        Args:
            images: List of image dictionaries with 'image' and 'date' keys
            output_format: Output format ('gif' or 'mp4')
            add_timestamps: Whether to overlay timestamps on frames
            visualization: Type of visualization used
            
        Returns:
            Dictionary with filename, frame_count, and other metadata
        """
        try:
            # Process images
            frames = []
            for img_data in images:
                frame = img_data['image']
                
                # Add timestamp if requested
                if add_timestamps:
                    frame = self._add_timestamp(
                        frame,
                        img_data['date'],
                        visualization
                    )
                
                frames.append(frame)
            
            # Normalize frame sizes
            frames = self._normalize_frames(frames)
            
            # Generate output filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"timelapse_{timestamp}.{output_format}"
            output_path = os.path.join(self.output_dir, filename)
            
            # Create animation
            if output_format == "gif":
                self._create_gif(frames, output_path)
            elif output_format == "mp4":
                self._create_mp4(frames, output_path)
            else:
                raise ValueError(f"Unsupported format: {output_format}")
            
            logger.info(f"Timelapse created: {output_path}")
            
            return {
                'filename': filename,
                'frame_count': len(frames),
                'path': output_path
            }
            
        except Exception as e:
            logger.error(f"Error creating timelapse: {str(e)}")
            raise
    
    def _normalize_frames(self, frames: List[Image.Image]) -> List[Image.Image]:
        """Ensure all frames have the same size."""
        if not frames:
            return frames
        
        # Find the most common size or use the first frame's size
        target_size = frames[0].size
        
        normalized = []
        for frame in frames:
            if frame.size != target_size:
                # Resize frame to target size
                frame = frame.resize(target_size, Image.Resampling.LANCZOS)
            normalized.append(frame)
        
        return normalized
    
    def _add_timestamp(
        self,
        image: Image.Image,
        date_str: str,
        visualization: str
    ) -> Image.Image:
        """Add a timestamp overlay to the image."""
        # Create a copy to avoid modifying original
        img = image.copy()
        draw = ImageDraw.Draw(img)
        
        # Parse and format date
        try:
            date = datetime.fromisoformat(date_str)
            date_text = date.strftime("%B %Y")
        except:
            date_text = date_str[:10]
        
        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except:
                font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), date_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position at top-left with padding
        padding = 20
        x, y = padding, padding
        
        # Draw background rectangle
        background_padding = 10
        draw.rectangle(
            [
                x - background_padding,
                y - background_padding,
                x + text_width + background_padding,
                y + text_height + background_padding
            ],
            fill=(0, 0, 0, 180)
        )
        
        # Draw text
        draw.text((x, y), date_text, fill=(255, 255, 255), font=font)
        
        # Add visualization type label
        viz_label = visualization.replace('-', ' ').title()
        try:
            small_font = ImageFont.truetype("arial.ttf", 20)
        except:
            try:
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            except:
                small_font = font
        
        viz_bbox = draw.textbbox((0, 0), viz_label, font=small_font)
        viz_width = viz_bbox[2] - viz_bbox[0]
        viz_height = viz_bbox[3] - viz_bbox[1]
        
        viz_x = img.width - viz_width - padding - background_padding
        viz_y = padding
        
        draw.rectangle(
            [
                viz_x - background_padding,
                viz_y - background_padding,
                viz_x + viz_width + background_padding,
                viz_y + viz_height + background_padding
            ],
            fill=(0, 0, 0, 180)
        )
        
        draw.text((viz_x, viz_y), viz_label, fill=(255, 255, 255), font=small_font)
        
        return img
    
    def _create_gif(self, frames: List[Image.Image], output_path: str):
        """Create an animated GIF from frames."""
        # Convert PIL images to numpy arrays for imageio
        frame_arrays = [imageio.core.util.Array(frame) for frame in frames]
        
        # Create GIF with optimization
        imageio.mimsave(
            output_path,
            frame_arrays,
            duration=0.5,  # Duration per frame in seconds
            loop=0  # Infinite loop
        )
    
    def _create_mp4(self, frames: List[Image.Image], output_path: str):
        """Create an MP4 video from frames."""
        # Convert PIL images to numpy arrays
        frame_arrays = [imageio.core.util.Array(frame) for frame in frames]
        
        # Create MP4 video
        writer = imageio.get_writer(
            output_path,
            fps=2,  # 2 frames per second
            codec='libx264',
            pixelformat='yuv420p',
            quality=8
        )
        
        try:
            for frame in frame_arrays:
                writer.append_data(frame)
        finally:
            writer.close()


