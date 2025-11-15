# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Application
```bash
python app.py
```

Or use the startup script:
```bash
./run.sh
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## 📝 First Time Setup

1. **Register a new account:**
   - Click "Register here" on the login page
   - Enter username and password
   - Click "Create Account"

2. **Login:**
   - Use your username and password

3. **Fetch some news:**
   - Click "Fetch Latest News" button
   - Enter a topic (e.g., "technology", "sports", "finance")
   - Set number of articles (e.g., 10)
   - Click "Fetch News"

4. **Start exploring:**
   - Click on news articles to read them
   - Your clicks are automatically tracked
   - Recommendations will appear based on your reading history

## 🎯 Key Features

- **Live News Feed** - See all available news articles
- **Personalized Recommendations** - Get news tailored to your interests
- **Category Filtering** - Filter news by category
- **Reading History** - Track all articles you've read
- **User Statistics** - See your reading patterns

## 💡 Tips

- Click on different categories of news to improve recommendations
- Use the "Fetch Latest News" feature to add fresh articles
- Check your statistics to see your reading preferences
- Recommendations update automatically as you click on articles

## 🐛 Troubleshooting

**Port already in use?**
- Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

**Database errors?**
- Delete `news_recommender.db` and restart the app (you'll need to re-register)

**Model not found?**
- The app will work but won't classify new articles
- Make sure `news_classifier_model.pkl` is in the project directory

**API errors?**
- Check your GNews API key in `app.py`
- Verify you have API credits remaining

## 📚 Next Steps

- Read `README_WEBAPP.md` for detailed documentation
- Check `README_DATABASE.md` for database information
- Explore the code to customize the application

Enjoy your News Recommender! 🎉

