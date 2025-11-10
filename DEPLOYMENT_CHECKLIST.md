# ✅ Render Deployment Checklist

## Before You Deploy

- [ ] Code is pushed to GitHub
- [ ] `.env` file is NOT in git (check: `git status`)
- [ ] Dockerfile builds locally (optional test)
- [ ] You have your API credentials ready

## Deployment Steps

### 1. Push to GitHub ⬆️

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Go to Render 🌐

Visit: [render.com](https://render.com)

### 3. Sign Up/Login

- Click "Get Started" or "Login"
- Choose "Sign in with GitHub"
- Authorize Render

### 4. Create New Web Service

- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select `time_machine`

### 5. Configure (Auto-Detected) ⚙️

Render should auto-detect from `render.yaml`:
- ✅ Name: time-machine-earth
- ✅ Environment: Docker
- ✅ Branch: main
- ✅ Plan: Free

### 6. Add Environment Variables 🔐

**CRITICAL**: Add these in Render dashboard:

| Key | Value |
|-----|-------|
| `ARLULA_KEY` | `iGa6pvvVfi1FLjFnSCAMuRPRr8vKyeQogph5nfH6eO4TysnaFD7r55mjtjAm` |
| `ARLULA_SECRET` | `IOfu9rgWbeJ7jZhvSbPynQN2nZq9qfQm9gaNFYYkSC2hRrTVONDgnge8bQ8M` |
| `USGS_USERNAME` | `Artoriass` |
| `USGS_TOKEN` | `rW9peoRVv_C2kPovKtHyLNqVnb@wzXyrCzzq!q2PlJT6AZU6PzYND0tKBh0ALApN` |

### 7. Deploy! 🚀

- Click "Create Web Service"
- Wait 5-10 minutes
- Watch build logs

### 8. Test Your App ✅

Once deployed:
- [ ] Visit your Render URL
- [ ] Draw an area on the map
- [ ] Generate a timelapse
- [ ] Verify it shows real satellite imagery
- [ ] Download the GIF and verify it works

## Your App Will Be Live At:

```
https://time-machine-earth.onrender.com
```
(or your custom name)

## After Deployment

### Auto-Deploy Setup ✅

Every time you push to GitHub:
```bash
git push origin main
```

Render will **automatically redeploy**!

### Check Logs

In Render dashboard:
- Click your service
- Go to "Logs" tab
- Watch for:
  - `Real satellite APIs enabled` ✅
  - `Application startup complete` ✅
  - Any errors ❌

### Monitor Health

Your health check: `https://your-app.onrender.com/api/health`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-10T12:00:00"
}
```

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ App loads at Render URL
- ✅ Map displays correctly
- ✅ Can draw AOI
- ✅ Timelapse generates
- ✅ Shows real Landsat imagery
- ✅ GIF downloads and plays correctly
- ✅ Dark mode works

## 📝 Share Your App

Once deployed:
- Share URL with friends
- Submit assignment with deployed link
- Add to your portfolio!

---

**Ready? Start with Step 1!** 🚀

