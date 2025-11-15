# 🚀 Quick Deployment Guide - Render.com

## Step-by-Step Deployment

### Step 1: Sign Up/Login
1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account** (recommended)

### Step 2: Create Web Service
1. Once logged in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Find and select: **`Nikhilg27425/News-recommender-system`**

### Step 3: Configure Service
Fill in these settings:

- **Name:** `news-recommender` (or your choice)
- **Region:** Choose closest to you (e.g., `Oregon (US West)`)
- **Branch:** `main`
- **Root Directory:** (leave empty)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

### Step 4: Set Environment Variables
Click **"Advanced"** → Scroll to **"Environment Variables"** → Click **"Add Environment Variable"**

Add these two:

1. **SECRET_KEY:**
   ```
   f981698a6892721ff183f054eb57311dcf2e75def66b6ae71bb68259c834b5fd
   ```
   (Or generate your own: `python -c "import secrets; print(secrets.token_hex(32))"`)

2. **API_KEY:**
   ```
   172285a1b5b6f981c517e59461b31a9a
   ```
   (Your GNews API key)

### Step 5: Deploy
1. Scroll down and click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Watch the build logs - it will show progress

### Step 6: Access Your App
Once deployed, your app will be live at:
```
https://news-recommender.onrender.com
```
(Or whatever name you chose)

---

## ✅ That's It!

Your News Recommender System is now live on the internet!

**Note:** 
- Free tier may take 30-60 seconds to wake up on first request
- Free tier spins down after 15 minutes of inactivity
- Upgrade to paid plan for always-on service

---

## 🔄 Updating Your App

After making changes:
```bash
git add .
git commit -m "Your changes"
git push
```

Render will automatically redeploy!

---

## 🆘 Need Help?

- Check build logs in Render dashboard
- Review `DEPLOYMENT.md` for detailed info
- Render docs: https://render.com/docs

