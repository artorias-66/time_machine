# 🌍 Time Machine for Earth

A full-stack web application that generates stunning timelapse visualizations from satellite imagery, showing how any location on Earth has changed over time.

![Time Machine for Earth](https://img.shields.io/badge/status-production-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![Deployed](https://img.shields.io/badge/deployed-Render-blueviolet)

## 🚀 Live Demo

**Try it now:** [https://time-machine-kn7h.onrender.com](https://time-machine-kn7h.onrender.com)

*Note: First load may take 30-60 seconds (free tier cold start)*

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)
*Interactive map with Leaflet drawing tools and control panel*

### Timelapse Generation
![Timelapse Result](screenshots/timelapse-result.png)
*Generated timelapse with real Landsat satellite imagery, timestamps, and download options*

### Real Satellite Imagery
![Satellite Imagery](screenshots/satellite-frame.png)
*Actual Landsat satellite imagery downloaded from Arlula API showing real Earth observations*


## ✨ Features

- 🗺️ **Interactive Map Interface** - Draw custom areas of interest using Leaflet with drawing tools
- 📅 **Flexible Date Range** - Select any time period to visualize changes
- ☁️ **Cloud Cover Filtering** - Control image quality by filtering cloud coverage
- 🎨 **Multiple Visualizations**
  - True Color (RGB) - Natural Earth colors
  - False Color (NIR) - Enhanced vegetation and water
  - NDVI - Vegetation health index
- 🎞️ **Dual Output Formats** - Generate animated GIFs or MP4 videos
- ⏱️ **Timestamp Overlays** - Optional date stamps on each frame
- 🌙 **Dark Mode** - Easy on the eyes with full dark theme support
- 📊 **Progress Tracking** - Real-time generation progress bar
- 💾 **Smart Caching** - Efficient data management
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │  Leaflet   │  │   Control    │  │     Result      │    │
│  │    Map     │  │    Panel     │  │    Display      │    │
│  └────────────┘  └──────────────┘  └─────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API
┌───────────────────────────┴─────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────┐           ┌──────────────────┐       │
│  │    Satellite     │           │    Timelapse     │       │
│  │     Service      │──────────▶│     Service      │       │
│  │  (Image Fetch)   │           │  (GIF/MP4 Gen)   │       │
│  └──────────────────┘           └──────────────────┘       │
└──────────────────────────────────────────────────────────────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
            ┌──────────────┐  ┌──────────────┐
            │   Satellite  │  │    Image     │
            │     APIs     │  │  Processing  │
            │ (Arlula/USGS)│  │ (PIL/FFmpeg) │
            └──────────────┘  └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/time-machine-earth.git
   cd time-machine-earth
   ```

2. **Install dependencies**
   ```bash
   # Frontend
   cd frontend
   npm install
   cd ..

   # Backend
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (optional for demo)
   ```

4. **Run the application**

   **Terminal 1 - Backend:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload --port 8000
   ```

   **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8000
```

## 📦 Deployment Options

### Render

1. Fork this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your repository
4. Render will automatically detect `render.yaml`
5. Add environment variables in the Render dashboard
6. Deploy! 🚀

### Railway

1. Fork this repository
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Railway will use `railway.json` for configuration
5. Add environment variables
6. Deploy automatically on push

### Vercel (Frontend Only)

```bash
cd frontend
npm run build
vercel --prod
```

Note: You'll need to deploy the backend separately and update the API URL.

## 🛰️ Satellite Data Sources

This application is designed to work with multiple free satellite data APIs:

### Currently Supported
- **Arlula Archive API** ✅ - Integrated! Searches real Landsat imagery
- **Synthetic Data Generation** - Fallback for demonstration

### Ready to Integrate (Future Enhancement)
1. **[Arlula Archive API](https://arlula.com/)**
   - Landsat and Sentinel imagery
   - Free access to open government data
   
2. **[USGS Landsat](https://earthexplorer.usgs.gov/)**
   - Decades of global imagery
   - Completely free

3. **[Sentinel Hub](https://www.sentinel-hub.com/)**
   - Sentinel-2 satellite data
   - Free tier available

4. **[AgroMonitoring](https://agromonitoring.com/)**
   - Agricultural focus
   - Free plan available

### Adding Your API Keys

Create `backend/.env` file:
```env
ARLULA_KEY=your_key_here
ARLULA_SECRET=your_secret_here
USGS_USERNAME=your_username
USGS_TOKEN=your_token
```

**The app automatically detects API keys and uses real satellite data when available!**

### How It Works

- **With API Keys**: Searches Arlula's archive for real Landsat scenes matching your criteria
  - Uses actual scene dates and cloud cover percentages
  - Logs which satellite scenes are being used
  - Falls back to demo mode if API fails
  
- **Without API Keys**: Uses synthetic imagery generator
  - Perfect for testing and demonstrations
  - No API limits or rate restrictions
  - Fully functional for all features

## 🔧 Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Leaflet** - Interactive maps
- **Leaflet Draw** - Drawing tools for AOI selection
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pillow (PIL)** - Image processing
- **ImageIO** - Media file handling
- **NumPy** - Numerical operations
- **Rasterio** - Geospatial raster data

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD (configuration ready)

## 📊 API Documentation

Once running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Key Endpoints

#### `POST /api/generate-timelapse`
Generate a timelapse from satellite imagery.

**Request Body:**
```json
{
  "aoi": {
    "type": "Feature",
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[lng, lat], ...]]
    },
    "properties": {
      "bounds": {
        "north": 40.7128,
        "south": 40.7000,
        "east": -74.0000,
        "west": -74.0200
      }
    }
  },
  "start_date": "2023-01-01",
  "end_date": "2023-06-01",
  "cloud_cover": 30,
  "output_format": "gif",
  "add_timestamps": true,
  "visualization": "true-color"
}
```

**Response:**
```json
{
  "url": "/output/timelapse_20231109_120000.gif",
  "frame_count": 6,
  "date_range": "2023-01-01 to 2023-06-01",
  "format": "gif",
   "visualization": "true-color",
   "dummy_data_used": false,
   "data_source": "arlula",
   "timestamp": "2023-11-09T12:00:00"
}
```

### Demo Mode Notice (Frontend)

When the backend generates imagery using demo (synthetic) data, the frontend now shows a clear popup informing the user that images may not match the selected area. This occurs when:

- No valid satellite API credentials are configured, or
- The provider returns no matching results and the app falls back to demo mode.

You can dismiss the popup and proceed; all other features (timestamps, visualization type, downloads) continue to work.

### Configurable Frame Count

The maximum number of images used to build a timelapse can be configured in `backend/config.py`:

```python
max_images_per_request: int = 20
```

This value is respected for real API imagery (e.g., Arlula). Synthetic mode generates a reasonable number of frames based on the date span (capped at 12 by default).

## 🎯 Usage Example

1. **Draw Your Area** - Use the rectangle or polygon tool to select a region on the map
2. **Set Parameters**
   - Start Date: `2023-01-01`
   - End Date: `2023-12-31`
   - Cloud Cover: `30%`
   - Visualization: `True Color`
   - Format: `GIF`
3. **Generate** - Click "Generate Timelapse"
4. **Download** - Your timelapse is ready to download and share!

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenStreetMap** - Map tiles
- **Leaflet** - Mapping library
- **Arlula** - Satellite imagery access
- **USGS** - Landsat data
- **ESA** - Sentinel satellite program

## 📧 Contact

For questions, issues, or suggestions:
- Open an issue on GitHub
- Email: your-email@example.com

## 🗺️ Roadmap

- [ ] Real-time satellite API integration (Arlula, USGS, Sentinel)
- [ ] Machine learning-based cloud detection
- [ ] Advanced visualizations (thermal, moisture index)
- [ ] Social sharing features
- [ ] User accounts and saved projects
- [ ] Batch processing for multiple AOIs
- [ ] WebGL-based map rendering for better performance
- [ ] Mobile app (React Native)

---

**Built with ❤️ for Earth observation and geospatial analysis**

*Note: This is a demonstration project. For production use with real satellite data, appropriate API keys and potentially paid API tiers may be required.*


