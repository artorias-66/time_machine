# Getting Started with Time Machine for Earth

Quick guide to get the application running in 5 minutes!

## Prerequisites

Choose one option:

### Option A: Docker (Easiest)
- Docker Desktop installed
- That's it!

### Option B: Local Development
- Node.js 18+ and npm
- Python 3.11+
- Git

## Quick Start with Docker (Recommended)

### 1. Clone and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/time-machine-earth.git
cd time-machine-earth

# Start the application
docker-compose up --build
```

### 2. Open in Browser

Navigate to: **http://localhost:8000**

That's it! 🎉

## Quick Start with Local Development

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/time-machine-earth.git
cd time-machine-earth
```

### 2. Install Dependencies

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

### 3. Run Application

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

### 4. Open in Browser

Navigate to: **http://localhost:3000**

## Your First Timelapse

### Step 1: Draw an Area
1. Look for drawing tools on the right side of the map
2. Click the **rectangle** or **polygon** tool
3. Draw a shape on the map (try drawing over a city!)

### Step 2: Set Parameters
- **Start Date**: `2023-01-01`
- **End Date**: `2023-12-31`
- **Cloud Cover**: `30%` (use the slider)
- **Visualization**: `True Color`
- **Format**: `GIF`
- ✅ Check "Add timestamps"

### Step 3: Generate
Click the **"🚀 Generate Timelapse"** button

### Step 4: Wait & Enjoy
- Watch the progress bar
- Preview appears in ~10-30 seconds
- Click **"⬇️ Download"** to save

## Recommended Test Locations

Try these interesting locations:

### 🏙️ Urban Development
**Dubai, UAE**: `25.2°N, 55.2°E`
- Draw a rectangle around the city
- Shows rapid urban expansion

### 🌳 Seasonal Changes
**New England, USA**: `44.3°N, 72.6°W`
- Beautiful fall colors
- Four-season changes

### 🌾 Agriculture
**Iowa, USA**: `42.0°N, 93.5°W`
- Use NDVI visualization
- Shows planting and harvest cycles

### 🏝️ Coastal Areas
**Mumbai, India**: `19.0°N, 72.8°E`
- Urban + coastal changes
- Monsoon patterns

## Tips for Best Results

### ✅ Do's
- Start with small areas (10-50 km²)
- Use 6-12 month date ranges
- Set cloud cover to 20-40%
- Try different visualizations

### ❌ Don'ts
- Don't select ocean-only areas
- Don't use very short date ranges (< 2 months)
- Don't set cloud cover too low (< 10%)
- Don't make the area too large initially

## Understanding Visualizations

### True Color (RGB)
- Natural Earth colors
- What you'd see from space
- Best for: Urban, water, general use

### False Color (NIR)
- Enhanced vegetation in red
- Water appears blue/black
- Best for: Agriculture, forests

### NDVI (Vegetation Index)
- Green = healthy vegetation
- Brown = bare soil or dead plants
- Best for: Monitoring crop health

## What You're Seeing

### In Demo Mode (Current)
The application generates **synthetic satellite-style images** that simulate:
- Seasonal color changes
- Landscape features
- Cloud patterns
- Temporal variations

This allows you to test the full application without API keys.

### With Real APIs (Future)
After adding API keys, you'll see:
- Actual satellite imagery from Landsat or Sentinel
- Real Earth changes over time
- Authentic vegetation cycles
- True cloud patterns

## Troubleshooting

### Issue: Docker won't start
```bash
# Check if Docker is running
docker --version

# Check if port 8000 is available
# On Windows:
netstat -ano | findstr :8000
# On Mac/Linux:
lsof -i :8000

# If port is busy, stop that service or change port in docker-compose.yml
```

### Issue: "No images found"
**Solution**: 
- Increase cloud cover to 50%
- Expand date range to 1 year
- Make sure you drew over land, not ocean

### Issue: Slow generation
**Solution**:
- Reduce area size
- Shorter date range
- This is normal for first run (Docker building images)

### Issue: Frontend won't connect to backend
**Solution**:
- Make sure backend is running on port 8000
- Check console for errors
- Verify proxy settings in `vite.config.js`

## Next Steps

### 1. Explore Features
- Try all three visualization types
- Compare GIF vs MP4 output
- Test dark mode toggle
- Try on mobile device

### 2. Read Documentation
- [README.md](README.md) - Full documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy to cloud

### 3. Add Real Data
- Sign up for satellite APIs (Arlula, USGS, Sentinel Hub)
- Add API keys to `.env` file
- See [README.md](README.md) for integration guide

### 4. Customize
- Modify colors in CSS files
- Adjust frame rates in `timelapse_service.py`
- Add new visualization types

## Common Questions

**Q: Do I need API keys to test?**
A: No! The app works in demo mode with synthetic data.

**Q: How much does it cost?**
A: The app is free. Satellite APIs have free tiers (Landsat, Sentinel are completely free).

**Q: Can I deploy this?**
A: Yes! See [DEPLOYMENT.md](DEPLOYMENT.md) for guides to Render, Railway, and more.

**Q: Can I use real satellite data?**
A: Yes! Add API keys in `.env` and implement the integration in `satellite_service.py`.

**Q: Is this production-ready?**
A: The structure is production-ready, but you should add tests, monitoring, and real APIs for production use.

## Support

- 📖 Check [README.md](README.md) for detailed docs
- 🐛 Found a bug? Open an issue on GitHub
- 💡 Have an idea? See [CONTRIBUTING.md](CONTRIBUTING.md)
- ❓ Questions? Check existing GitHub issues

## Quick Reference

### Keyboard Shortcuts
- None currently, but you could add them!

### Default Ports
- Frontend (dev): `3000`
- Backend: `8000`
- Docker: `8000`

### Important Files
- Frontend entry: `frontend/src/App.jsx`
- Backend entry: `backend/main.py`
- Config: `backend/config.py`
- Docker: `docker-compose.yml`

---

## Ready? Let's Go! 🚀

```bash
# Docker users:
docker-compose up

# Local development:
cd backend && python -m uvicorn main:app --reload
# (in another terminal)
cd frontend && npm run dev
```

**Open http://localhost:8000 (Docker) or http://localhost:3000 (local) and start creating timelapses!**

---

Need help? Start with the [README.md](README.md) or open an issue! 🌍✨


