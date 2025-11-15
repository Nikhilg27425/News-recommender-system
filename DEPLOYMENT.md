# Deployment Guide

This guide will help you deploy the News Recommender System to various platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - Free Tier Available)

**Steps:**

1. **Sign up/Login to Render:**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Nikhilg27425/News-recommender-system`
   - Select the repository

3. **Configure Service:**
   - **Name:** `news-recommender` (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. **Environment Variables:**
   - Click "Advanced" → "Add Environment Variable"
   - Add:
     - `SECRET_KEY`: Generate a random string (e.g., use: `python -c "import secrets; print(secrets.token_hex(32))"`)
     - `API_KEY`: Your GNews API key
     - `PYTHON_VERSION`: `3.11.0`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://news-recommender.onrender.com`

**Note:** Free tier may spin down after inactivity. First request may take 30-60 seconds.

---

### Option 2: Railway (Easy & Fast)

**Steps:**

1. **Sign up to Railway:**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure:**
   - Railway auto-detects Python
   - Add environment variables:
     - `SECRET_KEY`: (generate random string)
     - `API_KEY`: Your GNews API key
   - Railway will auto-deploy

4. **Get URL:**
   - Your app will be at: `https://your-app-name.railway.app`

---

### Option 3: PythonAnywhere (Python-Focused)

**Steps:**

1. **Sign up:**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Files:**
   - Go to "Files" tab
   - Upload your project files
   - Or use Git: `git clone https://github.com/Nikhilg27425/News-recommender-system.git`

3. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask
   - Select Python 3.10
   - Set path to: `/home/yourusername/News-recommender-system/app.py`

4. **Configure:**
   - Set WSGI file path
   - Add environment variables in "Web" → "Environment variables"
   - Reload web app

5. **Access:**
   - Your app: `https://yourusername.pythonanywhere.com`

---

### Option 4: Heroku (Classic Option)

**Steps:**

1. **Install Heroku CLI:**
   ```bash
   brew install heroku/brew/heroku
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create App:**
   ```bash
   heroku create news-recommender-app
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   heroku config:set API_KEY=your-api-key-here
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

6. **Open:**
   ```bash
   heroku open
   ```

---

## 🔧 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All dependencies in `requirements.txt`
- [ ] `gunicorn` added to requirements
- [ ] `SECRET_KEY` set as environment variable
- [ ] `API_KEY` set as environment variable
- [ ] Database will be created automatically (SQLite)
- [ ] Port uses `os.environ.get('PORT', 5001)`
- [ ] Debug mode set to `False` in production

## 📝 Environment Variables

Required environment variables:

```bash
SECRET_KEY=your-secret-key-here
API_KEY=your-gnews-api-key
PORT=5001  # Usually set by platform
```

Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🐛 Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Ensure Python version is compatible
- Check build logs for specific errors

### App Crashes
- Check environment variables are set
- Review application logs
- Ensure database file permissions (if using SQLite)

### Database Issues
- SQLite works on most platforms
- For production, consider PostgreSQL
- Database file will be created automatically

## 🔄 Updating Deployment

After making changes:

1. Commit changes:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```

2. Platform will auto-deploy (Render, Railway)
   - Or manually trigger deployment

## 📊 Monitoring

- Check application logs in platform dashboard
- Monitor error rates
- Track database size (SQLite has limits)

## 🎯 Recommended for Production

For production use, consider:
- PostgreSQL instead of SQLite
- Redis for caching
- CDN for static files
- Environment-specific configurations

---

**Need Help?** Check platform-specific documentation or open an issue on GitHub.

