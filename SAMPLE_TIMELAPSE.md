# Sample Timelapse

This document describes how to generate your first timelapse with Time Machine for Earth.

## Quick Start Example

Once the application is running, follow these steps to create a sample timelapse:

### 1. Launch the Application

```bash
# Option A: Docker
docker-compose up

# Option B: Local Development
# Terminal 1:
cd backend && python -m uvicorn main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

### 2. Select an Area of Interest

1. Open the application in your browser
2. Use the drawing tools (right side of map):
   - **Rectangle tool**: Click and drag to draw a rectangular area
   - **Polygon tool**: Click multiple points to draw a custom shape
   
**Sample Locations to Try:**

| Location | Coordinates | Why Interesting |
|----------|-------------|----------------|
| Mumbai, India | ~19.0°N, 72.8°E | Urban development, coastal changes |
| Amazon Rainforest | ~3.0°S, 60.0°W | Deforestation patterns |
| Dubai, UAE | ~25.2°N, 55.2°E | Rapid urban expansion |
| Iceland | ~64.1°N, 21.9°W | Seasonal changes, vegetation |
| California Central Valley | ~36.7°N, 119.7°W | Agricultural cycles |

### 3. Configure Parameters

**Recommended Settings for First Try:**
```
Start Date: 2023-01-01
End Date: 2023-12-31
Cloud Cover: 30%
Visualization: True Color (RGB)
Output Format: GIF
Add Timestamps: ✓ (checked)
```

### 4. Generate Timelapse

1. Click "Generate Timelapse" button
2. Wait for processing (typically 10-30 seconds for demo data)
3. Progress bar will show generation status

### 5. View and Download

Once complete:
- Preview will appear in the result panel
- Click "Download" to save the file
- Click "Copy Link" to share the URL

## Expected Output

### What You'll See

**Demo Mode (No API Keys):**
- Synthetic satellite-style imagery
- Gradual seasonal color changes
- Simulated landscape features
- Overlaid timestamps (if enabled)

**With Real API Keys:**
- Actual satellite imagery from Landsat or Sentinel
- True Earth changes over time
- Real cloud patterns and seasonal shifts
- Authentic vegetation and urban changes

## Example Configurations

### Urban Development Timelapse
```json
{
  "location": "Dubai, UAE",
  "start_date": "2020-01-01",
  "end_date": "2023-12-31",
  "cloud_cover": 20,
  "visualization": "true-color",
  "format": "mp4",
  "add_timestamps": true
}
```
**Expected Result:** Shows rapid urban expansion in the desert

### Agricultural Cycles
```json
{
  "location": "Iowa, USA",
  "start_date": "2023-03-01",
  "end_date": "2023-10-31",
  "cloud_cover": 30,
  "visualization": "ndvi",
  "format": "gif",
  "add_timestamps": true
}
```
**Expected Result:** Green-up and harvest cycles in NDVI

### Seasonal Changes
```json
{
  "location": "New England, USA",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "cloud_cover": 40,
  "visualization": "true-color",
  "format": "mp4",
  "add_timestamps": true
}
```
**Expected Result:** Four-season color changes from snow to fall foliage

## Visualization Types Explained

### True Color (RGB)
- **Bands**: Red, Green, Blue
- **Use Case**: Natural Earth appearance
- **Best For**: Urban areas, water bodies, general observation

### False Color (NIR)
- **Bands**: Near-Infrared, Red, Green
- **Use Case**: Enhanced vegetation contrast
- **Best For**: Agriculture, forests, vegetation health

### NDVI (Normalized Difference Vegetation Index)
- **Formula**: (NIR - Red) / (NIR + Red)
- **Scale**: -1 to +1
- **Use Case**: Vegetation health and density
- **Best For**: Agricultural monitoring, forest health, drought assessment
- **Color**: Darker = less vegetation, Brighter green = healthy vegetation

## Tips for Best Results

### 1. Area Size
- **Too Small** (< 1 km²): May not show significant changes
- **Optimal** (10-100 km²): Good balance of detail and coverage
- **Too Large** (> 1000 km²): Slow processing, large files

### 2. Date Range
- **Minimum**: 3 months (to see changes)
- **Optimal**: 6-12 months (seasonal cycles)
- **Maximum**: 5 years (long-term trends)

### 3. Cloud Cover
- **0-20%**: Very clear, but fewer images available
- **20-40%**: Good balance (recommended)
- **40-60%**: More images, some may be hazy
- **60-100%**: Many images, quality may suffer

### 4. Output Format
- **GIF**: 
  - Pros: Universal compatibility, auto-plays, smaller file size
  - Cons: Limited to 256 colors, lower quality
  - Best for: Sharing on social media, web embeds

- **MP4**:
  - Pros: Better quality, smoother playback, millions of colors
  - Cons: Slightly larger file, needs player controls
  - Best for: Presentations, high-quality archival

## Troubleshooting Sample Generation

### Issue: No images found

**Possible Causes:**
- Date range too narrow
- Cloud cover threshold too strict
- Area over ocean or poles

**Solutions:**
- Expand date range
- Increase cloud cover to 50%
- Select land area

### Issue: Timelapse looks choppy

**Causes:**
- Too few images in date range
- Inconsistent image availability

**Solutions:**
- Expand date range
- Increase cloud cover threshold
- Choose area with better satellite coverage

### Issue: Generation takes too long

**Causes:**
- Area too large
- Too many frames

**Solutions:**
- Reduce area size
- Shorter date range
- Use demo mode first

## Next Steps

After creating your first timelapse:

1. **Experiment** with different locations
2. **Try different visualizations** (True Color vs NDVI)
3. **Compare seasons** (Winter vs Summer)
4. **Add real API keys** for authentic satellite data
5. **Share your results** on social media

## Sample API Request

For developers who want to test the API directly:

```bash
curl -X POST http://localhost:8000/api/generate-timelapse \
  -H "Content-Type: application/json" \
  -d '{
    "aoi": {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[72.8, 19.0], [72.9, 19.0], [72.9, 19.1], [72.8, 19.1], [72.8, 19.0]]]
      },
      "properties": {
        "bounds": {
          "north": 19.1,
          "south": 19.0,
          "east": 72.9,
          "west": 72.8
        }
      }
    },
    "start_date": "2023-01-01",
    "end_date": "2023-06-01",
    "cloud_cover": 30,
    "output_format": "gif",
    "add_timestamps": true,
    "visualization": "true-color"
  }'
```

## Real World Examples

Check the `examples/` directory (if available) for:
- Pre-generated timelapses
- Sample GeoJSON AOIs
- Configuration templates
- Interesting location coordinates

---

**Ready to create Earth's visual history? Start drawing on the map!** 🌍✨


