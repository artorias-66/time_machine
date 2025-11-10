# 🚀 Deploying to Render - Step by Step

## ✅ Pre-Deployment Checklist

Your app is now ready for deployment! Here's what's configured:

- ✅ **Dockerfile** - Multi-stage build for frontend + backend
- ✅ **render.yaml** - Render auto-configuration
- ✅ **Real Arlula API** - Working satellite integration
- ✅ **Working GIF generation** - Tested and verified
- ✅ **Production-ready code** - All features functional

## 🎯 Deployment Steps

### Step 1: Push to GitHub

```bash
# Make sure you're in the project root
cd C:\projects\time_machine

# Add all files
git add .

# Commit
git commit -m "Complete Time Machine for Earth - Ready for deployment"

# Push to GitHub
git push origin main
```

**Important**: Your `.env` file won't be pushed (it's in `.gitignore`) ✅

---

### Step 2: Sign Up on Render

1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Sign up with your **GitHub account** (easiest)
4. Authorize Render to access your repositories

---

### Step 3: Create Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if not connected
4. Find and select your **`time_machine`** repository
5. Click **"Connect"**

---

### Step 4: Configure Service

Render should **auto-detect** your `render.yaml`, but verify these settings:

**Basic Settings:**
- **Name**: `time-machine-earth` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Environment**: `Docker` ✅ (Should auto-select)
- **Dockerfile Path**: `./Dockerfile` ✅

**Instance Type:**
- Select **"Free"** ✅

---

### Step 5: Add Environment Variables

⚠️ **CRITICAL STEP** - Add your API keys:

Click on **"Environment"** tab and add:

```
ARLULA_KEY=iGa6pvvVfi1FLjFnSCAMuRPRr8vKyeQogph5nfH6eO4TysnaFD7r55mjtjAm
ARLULA_SECRET=IOfu9rgWbeJ7jZhvSbPynQN2nZq9qfQm9gaNFYYkSC2hRrTVONDgnge8bQ8M
USGS_USERNAME=Artoriass
USGS_TOKEN=rW9peoRVv_C2kPovKtHyLNqVnb@wzXyrCzzq!q2PlJT6AZU6PzYND0tKBh0ALApN
```

Click **"Add"** for each one.

---

### Step 6: Deploy!

1. Click **"Create Web Service"** button
2. Wait for deployment (takes 5-10 minutes)
3. Watch the logs as it builds

**Build Process:**
```
Building Dockerfile...
[+] Building frontend...
[+] Installing Python dependencies...
[+] Creating directories...
✅ Build complete!
```

---

### Step 7: Get Your URL!

Once deployed, you'll see:
```
✅ Live at https://time-machine-earth.onrender.com
```

Click the URL to visit your deployed app! 🎉

---

## 🧪 Testing Your Deployed App

1. Open your Render URL
2. Draw an area on the map
3. Generate a timelapse
4. Download and verify it works!

---

## ⚠️ Important Notes

### Free Tier Limitations

**Render Free Tier:**
- ✅ 750 hours/month (plenty!)
- ⚠️ **Spins down after 15 mins of inactivity**
- ⚠️ First request after sleep takes ~30-60 seconds (cold start)
- ✅ Auto-deploys on git push

### Keeping It Awake (Optional)

If you want to prevent sleep, use a service like:
- **UptimeRobot** (free) - Ping your app every 5 minutes
- **Cron-job.org** (free) - Schedule health checks

---

## 🔧 Troubleshooting

### Build Fails

**Check:**
- Docker configuration is correct
- All dependencies in requirements.txt
- No syntax errors in Python files

**Solution:**
```bash
# Test Docker build locally first
docker build -t time-machine-test .
docker run -p 8000:8000 time-machine-test
```

### App Doesn't Load

**Check:**
- Environment variables are set correctly
- Health check endpoint `/api/health` responds
- Check Render logs for errors

### GIF Generation Fails

**Check Render logs** for:
- `Real satellite APIs enabled` ✅
- API key errors
- Download failures

---

## 📊 Monitoring Your App

### Health Check

Render automatically uses: `GET /api/health`

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-10T12:00:00"
}
```

### Logs

In Render dashboard:
- Click on your service
- Go to **"Logs"** tab
- Watch real-time application logs

---

## 🔄 Updating Your Deployment

After deployment, any time you push to GitHub:

```bash
git add .
git commit -m "Update feature X"
git push origin main
```

Render will **automatically redeploy**! 🚀

---

## 💡 Pro Tips

1. **Test locally first** with Docker before deploying
2. **Check logs immediately** after deployment
3. **Save your environment variables** somewhere safe
4. **Monitor first few requests** to ensure everything works
5. **Share your URL** once confirmed working!

---

## 🎉 After Deployment

Once live, you'll have:
- ✅ Publicly accessible app
- ✅ Real satellite imagery
- ✅ Working timelapse generation
- ✅ Professional portfolio piece!

**Your deployed URL will be:**
```
https://time-machine-earth.onrender.com
```
(or whatever name you choose)

---

## 🆘 Need Help?

**Render Documentation:**
- https://render.com/docs
- https://render.com/docs/docker

**Check:**
- Render dashboard logs
- GitHub Actions (if configured)
- Your terminal for local testing

---

**Ready to deploy?** Follow the steps above! 🚀🌍

**Estimated time: 15 minutes** (5 min setup + 10 min build)

