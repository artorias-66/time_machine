import os
import logging
from datetime import datetime
from typing import List, Dict
from PIL import Image, ImageDraw, ImageFont
import imageio
import numpy as np
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
            for i, img_data in enumerate(images):
                frame = img_data['image']
                
                # Verify frame is valid
                if not isinstance(frame, Image.Image):
                    logger.error(f"Frame {i} is not a PIL Image: {type(frame)}")
                    continue
                
                logger.info(f"Processing frame {i+1}/{len(images)}: size={frame.size}, mode={frame.mode}")
                
                # Make a copy to avoid modifying original
                frame = frame.copy()
                
                # Add timestamp if requested
                if add_timestamps:
                    try:
                        frame = self._add_timestamp(
                            frame,
                            img_data['date'],
                            visualization
                        )
                    except Exception as e:
                        logger.warning(f"Failed to add timestamp to frame {i}: {str(e)}")
                        # Continue without timestamp
                
                frames.append(frame)
            
            if not frames:
                raise ValueError("No valid frames to create timelapse")
            
            # Don't normalize - keep original sizes and let GIF handle it
            # frames = self._normalize_frames(frames)
            
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
        try:
            # Create a copy to avoid modifying original
            img = image.copy()
            
            # Ensure RGB mode
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            draw = ImageDraw.Draw(img)
            
            # Parse and format date
            try:
                date = datetime.fromisoformat(date_str)
                date_text = date.strftime("%B %Y")
            except:
                date_text = date_str[:10] if len(date_str) >= 10 else date_str
            
            # Use default font (most compatible)
            font = ImageFont.load_default()
            
            # Simple text overlay at top-left
            padding = 10
            x, y = padding, padding
            
            # Draw semi-transparent background box
            text_bbox = draw.textbbox((x, y), date_text, font=font)
            draw.rectangle(
                [text_bbox[0] - 5, text_bbox[1] - 5, text_bbox[2] + 5, text_bbox[3] + 5],
                fill=(0, 0, 0)
            )
            
            # Draw text
            draw.text((x, y), date_text, fill=(255, 255, 255), font=font)
            
            # Return the modified image
            return img
            
        except Exception as e:
            logger.error(f"Error adding timestamp: {str(e)}")
            # Return original image if timestamp fails
            return image
    
    def _create_gif(self, frames: List[Image.Image], output_path: str):
        """Create an animated GIF from frames."""
        try:
            if not frames:
                raise ValueError("No frames provided for GIF creation")
            
            logger.info(f"Creating GIF from {len(frames)} frames")
            logger.info(f"First frame: type={type(frames[0])}, size={frames[0].size if hasattr(frames[0], 'size') else 'N/A'}, mode={frames[0].mode if hasattr(frames[0], 'mode') else 'N/A'}")
            
            # Use EXACT same method as working test_download.py
            # All frames should already be RGB from satellite_service
            
            # Save directly as GIF (same as test)
            frames[0].save(
                output_path,
                format='GIF',
                save_all=True,
                append_images=frames[1:],
                duration=500,  # milliseconds per frame
                loop=0  # infinite loop
            )
            
            # Verify the file was created and has size
            import os
            file_size = os.path.getsize(output_path)
            logger.info(f"GIF created successfully at {output_path}, size: {file_size} bytes")
            
        except Exception as e:
            logger.error(f"Error creating GIF: {str(e)}", exc_info=True)
            raise
    
    def _create_mp4(self, frames: List[Image.Image], output_path: str):
        """Create an MP4 video from frames."""
        try:
            # Resize frames to dimensions divisible by 16 for MP4 encoding
            target_width = 800
            target_height = 608  # 608 is divisible by 16
            
            # Convert PIL images to numpy arrays (ensure RGB format and correct size)
            frame_arrays = []
            for i, frame in enumerate(frames):
                # Ensure frame is in RGB mode
                if frame.mode != 'RGB':
                    frame = frame.convert('RGB')
                
                # Resize if needed
                if frame.size != (target_width, target_height):
                    frame = frame.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                frame_array = np.array(frame, dtype=np.uint8)
                frame_arrays.append(frame_array)
                
                if i == 0:
                    logger.info(f"Frame shape: {frame_array.shape}, dtype: {frame_array.dtype}")
            
            # Create MP4 video using imageio
            writer = imageio.get_writer(
                output_path,
                fps=2,
                codec='libx264',
                pixelformat='yuv420p',
                quality=7,
                macro_block_size=16
            )
            
            try:
                for frame_array in frame_arrays:
                    writer.append_data(frame_array)
            finally:
                writer.close()
                
            logger.info(f"MP4 created successfully with {len(frame_arrays)} frames at {target_width}x{target_height}")
            
        except Exception as e:
            logger.error(f"Error creating MP4: {str(e)}", exc_info=True)
            raise


