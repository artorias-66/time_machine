# Deployment Guide

Complete guide for deploying Time Machine for Earth to various platforms.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Render](#render)
4. [Railway](#railway)
5. [Vercel + Backend](#vercel--backend)
6. [Manual Server Deployment](#manual-server-deployment)

---

## Local Development

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/time-machine-earth.git
cd time-machine-earth
```

2. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

3. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
# Or use virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

4. **Set up environment variables** (optional)
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

5. **Run the application**

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

6. **Open browser**
Navigate to `http://localhost:3000`

---

## Docker Deployment

### Prerequisites
- Docker 20+
- Docker Compose 2+

### Using Docker Compose (Recommended)

1. **Build and run**
```bash
docker-compose up --build
```

2. **Access application**
Open `http://localhost:8000`

3. **Stop containers**
```bash
docker-compose down
```

### Using Docker only

```bash
# Build image
docker build -t time-machine-earth .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/cache:/app/cache \
  time-machine-earth
```

---

## Render

Deploy to Render's free tier in minutes.

### Steps

1. **Fork this repository** on GitHub

2. **Sign up** at [render.com](https://render.com)

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your forked repository

4. **Configuration**
   - Render will auto-detect `render.yaml`
   - Alternatively, manual settings:
     - **Name**: `time-machine-earth`
     - **Environment**: `Docker`
     - **Region**: Choose closest to you
     - **Branch**: `main`
     - **Docker Command**: (leave default)

5. **Environment Variables** (optional)
   - Add any API keys:
     - `ARLULA_API_KEY`
     - `USGS_USERNAME`
     - `USGS_PASSWORD`

6. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Access your app at: `https://time-machine-earth.onrender.com`

### Notes
- Free tier spins down after inactivity
- First request after sleep takes 30-60 seconds
- Automatic deploys on git push

---

## Railway

Deploy to Railway with one command.

### Steps

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
# or
brew install railway
```

2. **Login**
```bash
railway login
```

3. **Initialize project**
```bash
railway init
```

4. **Deploy**
```bash
railway up
```

5. **Set environment variables** (optional)
```bash
railway variables set ARLULA_API_KEY=your_key_here
```

6. **Get URL**
```bash
railway domain
```

### Alternative: GitHub Integration

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway auto-detects configuration
6. Click "Deploy"

---

## Vercel + Backend

Deploy frontend to Vercel, backend separately.

### Frontend (Vercel)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy frontend**
```bash
cd frontend
npm run build
vercel --prod
```

3. **Configure**
   - Vercel will ask for project settings
   - Set build command: `npm run build`
   - Set output directory: `dist`

### Backend (Render/Railway)

Deploy backend separately using Render or Railway (see above), then:

1. **Update frontend API URL**
Edit `frontend/vite.config.js`:
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://your-backend-url.onrender.com',
        changeOrigin: true,
      }
    }
  }
})
```

2. **Redeploy frontend**
```bash
vercel --prod
```

---

## Manual Server Deployment

Deploy to your own VPS (Ubuntu 22.04).

### Prerequisites
- Ubuntu 22.04 server
- Sudo access
- Domain name (optional)

### Steps

1. **Update system**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install dependencies**
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install FFmpeg and GDAL
sudo apt install -y ffmpeg gdal-bin libgdal-dev

# Install Nginx
sudo apt install -y nginx

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

3. **Clone repository**
```bash
cd /opt
sudo git clone https://github.com/yourusername/time-machine-earth.git
cd time-machine-earth
sudo chown -R $USER:$USER .
```

4. **Install application dependencies**
```bash
# Frontend
cd frontend
npm install
npm run build
cd ..

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

5. **Create systemd service**
```bash
sudo nano /etc/systemd/system/time-machine.service
```

Add content:
```ini
[Unit]
Description=Time Machine for Earth API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/time-machine-earth/backend
Environment="PATH=/opt/time-machine-earth/backend/venv/bin"
ExecStart=/opt/time-machine-earth/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/time-machine
```

Add content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Change this

    # Frontend
    location / {
        root /opt/time-machine-earth/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Output files
    location /output {
        proxy_pass http://localhost:8000/output;
    }
}
```

7. **Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/time-machine /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

8. **Start service**
```bash
sudo systemctl enable time-machine
sudo systemctl start time-machine
sudo systemctl status time-machine
```

9. **Set up HTTPS with Let's Encrypt** (optional)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

10. **Configure firewall**
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## Environment Variables

For all deployment methods, you may need these environment variables:

```env
# Satellite API Keys (optional for demo)
ARLULA_API_KEY=your_key_here
USGS_USERNAME=your_username
USGS_PASSWORD=your_password
SENTINEL_HUB_CLIENT_ID=your_client_id
SENTINEL_HUB_CLIENT_SECRET=your_client_secret

# Application Settings
MAX_IMAGES_PER_REQUEST=20
MAX_AOI_SIZE_KM2=10000
MAX_CACHE_SIZE_MB=1000
```

---

## Troubleshooting

### Issue: Docker build fails

**Solution:**
```bash
# Clear Docker cache
docker system prune -a
docker-compose build --no-cache
```

### Issue: Frontend can't connect to backend

**Solution:**
Check CORS settings in `backend/main.py` and ensure API proxy is configured correctly.

### Issue: Out of memory during build

**Solution:**
Increase Docker memory limit or deploy frontend/backend separately.

### Issue: FFmpeg not found

**Solution:**
```bash
# Install FFmpeg
sudo apt install ffmpeg
# Or in Docker, ensure it's in Dockerfile
```

### Issue: Permission denied on output directory

**Solution:**
```bash
mkdir -p output cache
chmod 755 output cache
```

---

## Monitoring

### Health Check

```bash
curl http://your-domain.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2023-11-09T12:00:00"
}
```

### Logs

**Docker:**
```bash
docker-compose logs -f
```

**Systemd:**
```bash
sudo journalctl -u time-machine -f
```

---

## Updating

### Local Development
```bash
git pull origin main
cd frontend && npm install && cd ..
cd backend && pip install -r requirements.txt && cd ..
```

### Docker
```bash
git pull origin main
docker-compose up --build -d
```

### Manual Server
```bash
cd /opt/time-machine-earth
git pull origin main
cd frontend && npm install && npm run build && cd ..
cd backend && source venv/bin/activate && pip install -r requirements.txt && cd ..
sudo systemctl restart time-machine
```

---

**Need help?** Open an issue on GitHub or consult the README.md for more information.


