# 🚀 Deploying to Vercel + Render

Since Vercel is optimized for frontend and doesn't support full Python backends, we'll use:

- **Frontend (React)** → Vercel
- **Backend (FastAPI)** → Render

## 📋 Deployment Order

**Deploy Backend FIRST, then Frontend!**

---

## Part 1: Deploy Backend to Render 🔧

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy Backend on Render

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Select your `time_machine` repository
5. Configure:
   - **Name**: `time-machine-backend`
   - **Environment**: Docker
   - **Branch**: main
6. **Add Environment Variables**:
   ```
   ARLULA_KEY=iGa6pvvVfi1FLjFnSCAMuRPRr8vKyeQogph5nfH6eO4TysnaFD7r55mjtjAm
   ARLULA_SECRET=IOfu9rgWbeJ7jZhvSbPynQN2nZq9qfQm9gaNFYYkSC2hRrTVONDgnge8bQ8M
   USGS_USERNAME=Artoriass
   USGS_TOKEN=rW9peoRVv_C2kPovKtHyLNqVnb@wzXyrCzzq!q2PlJT6AZU6PzYND0tKBh0ALApN
   ```
7. Click "Create Web Service"
8. Wait ~10 minutes
9. **Copy your backend URL** (e.g., `https://time-machine-backend.onrender.com`)

---

## Part 2: Deploy Frontend to Vercel 🎨

### Step 3: Update Frontend Config

**Edit `frontend/.env.production`** and replace with YOUR backend URL:

```env
VITE_API_URL=https://time-machine-backend.onrender.com
```

(Use the URL you got from Render step!)

### Step 4: Commit Changes

```bash
git add frontend/.env.production
git commit -m "Add production backend URL"
git push origin main
```

### Step 5: Deploy to Vercel

**Option A: Vercel CLI (Recommended)**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel

# Follow prompts:
# ? Set up and deploy? Yes
# ? Which scope? (your account)
# ? Link to existing project? No
# ? What's your project's name? time-machine-earth
# ? In which directory is your code located? ./
# ? Auto-detected settings. Continue? Yes

# Deploy to production
vercel --prod
```

**Option B: Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "Add New..." → "Project"
4. Import your `time_machine` repository
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. **Add Environment Variable**:
   - Key: `VITE_API_URL`
   - Value: `https://time-machine-backend.onrender.com` (your Render URL)
7. Click "Deploy"
8. Wait ~2-3 minutes
9. Get your Vercel URL! 🎉

---

## ✅ Verification

### Test Backend (Render)

Visit: `https://time-machine-backend.onrender.com/api/health`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-10T12:00:00"
}
```

### Test Frontend (Vercel)

Visit: `https://time-machine-earth.vercel.app`

1. Should show the map
2. Draw an area
3. Generate timelapse
4. Verify it downloads real satellite imagery

---

## 🔧 CORS Configuration

The backend needs to allow requests from Vercel. I'll update it:

**Backend is already configured with:**
```python
allow_origins=["*"]
```

This allows all origins, which is fine for this project. ✅

---

## 📊 Summary

**Backend URL** (Render):
```
https://time-machine-backend.onrender.com
```

**Frontend URL** (Vercel):
```
https://time-machine-earth.vercel.app
```

**Flow**:
```
User → Vercel Frontend → Render Backend API → Arlula/USGS → GIF
```

---

## 💡 Alternative: Deploy Both on Render

If Vercel is too complex, you can deploy BOTH on Render using your existing `render.yaml` configuration!

Just:
1. Go to Render
2. Create Web Service
3. It serves both frontend AND backend together
4. One URL for everything

**Which do you prefer?**
- **Vercel + Render** (frontend separate)
- **Just Render** (everything together - easier!)

Let me know and I'll guide you! 🚀

