# Architecture Documentation

## System Overview

Time Machine for Earth is a full-stack geospatial application that generates timelapse visualizations from satellite imagery. The system follows a client-server architecture with clear separation between frontend, backend, and data processing layers.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                         (Web Browser)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS / WebSocket
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Frontend Application                          │
│                        (React + Vite)                            │
│  ┌──────────────┐ ┌───────────────┐ ┌────────────────────┐    │
│  │   MapView    │ │ ControlPanel  │ │  ResultDisplay     │    │
│  │  Component   │ │   Component   │ │    Component       │    │
│  │              │ │               │ │                    │    │
│  │  - Leaflet   │ │ - Date Range  │ │ - Preview          │    │
│  │  - Drawing   │ │ - Cloud Cover │ │ - Download         │    │
│  │  - AOI       │ │ - Viz Type    │ │ - Metadata         │    │
│  └──────────────┘ └───────────────┘ └────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API (JSON)
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Backend Application                           │
│                        (FastAPI)                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                   API Layer                             │    │
│  │  - /api/generate-timelapse                             │    │
│  │  - /api/health                                         │    │
│  │  - /api/cache/clear                                    │    │
│  └───────────────────────┬────────────────────────────────┘    │
│                          │                                       │
│  ┌───────────────────────┴────────────────────────────────┐    │
│  │                  Service Layer                          │    │
│  │  ┌──────────────────────┐  ┌──────────────────────┐  │    │
│  │  │ SatelliteService     │  │ TimelapseService     │  │    │
│  │  │                      │  │                      │  │    │
│  │  │ - Fetch Images       │  │ - Process Frames     │  │    │
│  │  │ - Filter Cloud Cover │  │ - Add Timestamps     │  │    │
│  │  │ - Normalize Data     │  │ - Create GIF/MP4     │  │    │
│  │  │ - Cache Management   │  │ - Output Management  │  │    │
│  │  └──────────────────────┘  └──────────────────────┘  │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   ┌─────────┴──────────┐
                   │                    │
┌──────────────────┴──────┐  ┌─────────┴──────────────┐
│   External APIs          │  │  Image Processing      │
│                          │  │                        │
│  - Arlula Archive        │  │  - PIL/Pillow          │
│  - USGS Landsat          │  │  - NumPy               │
│  - Sentinel Hub          │  │  - ImageIO             │
│  - AgroMonitoring        │  │  - FFmpeg (via imageio)│
└──────────────────────────┘  └────────────────────────┘
```

## Component Details

### Frontend Layer

#### Technology Stack
- **React 18**: Component-based UI framework
- **Vite**: Fast build tool and dev server
- **Leaflet**: Open-source mapping library
- **Leaflet Draw**: Drawing and editing tools
- **Axios**: HTTP client for API communication

#### Key Components

**1. App Component (`App.jsx`)**
- Root component managing global state
- Handles theme (dark mode)
- Coordinates communication between child components
- Manages API responses and errors

**2. MapView Component (`MapView.jsx`)**
- Renders interactive Leaflet map
- Enables AOI selection via drawing tools
- Calculates and displays area size
- Emits AOI geometry to parent

**3. ControlPanel Component (`ControlPanel.jsx`)**
- Collects user input parameters
- Validates date ranges
- Manages cloud cover slider
- Triggers timelapse generation
- Displays progress bar during processing

**4. ResultDisplay Component (`ResultDisplay.jsx`)**
- Shows generated timelapse preview
- Provides download functionality
- Displays metadata (frame count, date range)
- Copy-to-clipboard for sharing

**5. Header Component (`Header.jsx`)**
- Application branding
- Dark mode toggle
- Responsive navigation

### Backend Layer

#### Technology Stack
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **PIL (Pillow)**: Image manipulation
- **ImageIO**: Media file handling
- **NumPy**: Numerical computations

#### API Endpoints

**POST /api/generate-timelapse**
```python
Request:
{
    "aoi": GeoJSON Feature,
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "cloud_cover": int (0-100),
    "output_format": "gif" | "mp4",
    "add_timestamps": bool,
    "visualization": "true-color" | "false-color" | "ndvi"
}

Response:
{
    "url": "/output/timelapse_xxx.gif",
    "frame_count": int,
    "date_range": string,
    "format": string,
    "visualization": string,
    "timestamp": ISO-8601
}
```

**GET /api/health**
- Returns service health status
- Used for monitoring and health checks

**DELETE /api/cache/clear**
- Clears cached imagery and temp files
- Helps manage disk space

#### Service Layer

**1. SatelliteService (`satellite_service.py`)**

Purpose: Fetch and process satellite imagery

Methods:
- `fetch_images()`: Main method to retrieve imagery
- `fetch_from_arlula()`: Arlula API integration (placeholder)
- `fetch_from_usgs()`: USGS Landsat integration (placeholder)
- `_generate_synthetic_image()`: Demo data generator

Process Flow:
1. Parse date range and calculate intervals
2. Query satellite APIs for imagery
3. Filter by cloud cover
4. Download and cache images
5. Normalize to common format
6. Return processed image list

**2. TimelapseService (`timelapse_service.py`)**

Purpose: Create timelapse animations from image sequences

Methods:
- `create_timelapse()`: Main generation method
- `_normalize_frames()`: Ensure consistent dimensions
- `_add_timestamp()`: Overlay date/time on frames
- `_create_gif()`: Generate animated GIF
- `_create_mp4()`: Generate MP4 video

Process Flow:
1. Receive processed images
2. Add timestamps if requested
3. Normalize frame sizes
4. Apply color corrections
5. Generate output file
6. Return metadata and URL

## Data Flow

### Timelapse Generation Flow

```
User Draws AOI
      │
      ├─→ MapView captures coordinates
      │
      ├─→ User sets parameters in ControlPanel
      │
      ├─→ POST request to /api/generate-timelapse
      │
      ├─→ Backend validates request
      │
      ├─→ SatelliteService.fetch_images()
      │   │
      │   ├─→ Calculate date intervals
      │   ├─→ Query satellite APIs
      │   ├─→ Filter by cloud cover
      │   └─→ Return image list
      │
      ├─→ TimelapseService.create_timelapse()
      │   │
      │   ├─→ Normalize frames
      │   ├─→ Add timestamps
      │   ├─→ Generate GIF or MP4
      │   └─→ Save to output directory
      │
      ├─→ Return response with URL
      │
      └─→ ResultDisplay shows preview & download
```

## Storage Architecture

### Directory Structure

```
time-machine-earth/
│
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.jsx        # Root component
│   │   └── index.css      # Global styles
│   └── dist/              # Build output (generated)
│
├── backend/               # FastAPI application
│   ├── services/          # Business logic
│   │   ├── satellite_service.py
│   │   └── timelapse_service.py
│   ├── main.py            # API endpoints
│   └── config.py          # Configuration
│
├── output/                # Generated timelapses
│   └── timelapse_*.gif/mp4
│
└── cache/                 # Temporary imagery cache
    └── satellite_*.tif
```

### Caching Strategy

1. **Image Cache**: Downloaded satellite images stored temporarily
2. **Output Storage**: Generated timelapses stored in `/output`
3. **Cache Invalidation**: Manual via API or automatic after size limit
4. **TTL**: 24 hours for cached imagery

## Security Considerations

### Implemented
- ✅ CORS configuration for cross-origin requests
- ✅ Input validation using Pydantic models
- ✅ Environment variable-based configuration
- ✅ Error handling without exposing internals

### Recommended for Production
- 🔒 API rate limiting
- 🔒 Authentication and authorization
- 🔒 HTTPS enforcement
- 🔒 Input sanitization for file paths
- 🔒 Secret management (AWS Secrets Manager, Vault)
- 🔒 SQL injection prevention (not applicable currently)

## Scalability Considerations

### Current Limitations
- Synchronous image processing
- Single server instance
- Local file storage

### Scaling Recommendations

**Horizontal Scaling:**
- Deploy multiple backend instances behind load balancer
- Use shared storage (S3, GCS) for output files
- Implement message queue (RabbitMQ, Kafka) for async processing

**Vertical Scaling:**
- Increase server resources (CPU, RAM)
- Use GPU acceleration for image processing
- Optimize image compression algorithms

**Caching Strategy:**
- Redis for API response caching
- CDN for serving static output files
- Database for metadata storage

## Performance Optimization

### Current Optimizations
- Multi-stage Docker build reduces image size
- Async I/O in FastAPI
- Image normalization pipeline
- Efficient GIF/MP4 encoding

### Future Optimizations
- WebP format support for smaller files
- Lazy loading for large timelapses
- Progressive loading of video
- Worker pools for parallel image processing
- Streaming responses for large files

## Monitoring and Observability

### Health Checks
- `/api/health` endpoint
- Docker health check configuration
- Startup/readiness probes

### Logging
- Structured logging with Python logging module
- Request/response logging
- Error tracking with stack traces

### Recommended Additions
- Prometheus metrics export
- Grafana dashboards
- Sentry for error tracking
- Application performance monitoring (APM)

## Deployment Architecture

### Development
```
localhost:3000 (Vite) ←→ localhost:8000 (FastAPI)
```

### Production (Docker)
```
Port 8000 → Uvicorn → FastAPI → Static Frontend
```

### Cloud Deployment Options

**Option 1: Render**
- Single Docker container
- Automatic HTTPS
- GitHub integration

**Option 2: Railway**
- Automatic deployments
- Environment variable management
- Built-in metrics

**Option 3: Separate Frontend/Backend**
- Frontend: Vercel/Netlify
- Backend: Render/Railway/Fly.io
- CDN: CloudFlare

## Technology Decisions

### Why React?
- Component reusability
- Rich ecosystem
- Excellent mapping library support
- Fast development with hooks

### Why FastAPI?
- Native async support
- Automatic API documentation
- Type validation with Pydantic
- High performance
- Python geospatial library ecosystem

### Why Leaflet over MapBox?
- Open source and free
- No API key required
- Excellent documentation
- Extensive plugin ecosystem

### Why ImageIO over raw FFmpeg?
- Python-native interface
- Simpler API
- Automatic FFmpeg installation
- Cross-platform compatibility

## Future Enhancements

### Short Term
- Real satellite API integration
- User authentication
- Save/load projects
- More visualization types

### Long Term
- Machine learning for cloud detection
- Time series analysis
- Change detection algorithms
- Mobile app
- Batch processing
- API for third-party integrations

---

This architecture provides a solid foundation for a production-ready geospatial timelapse application while maintaining flexibility for future enhancements.


