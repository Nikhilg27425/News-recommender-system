# News Recommender Web Application

A modern web application for the News Recommender System with user authentication, live news feed, and personalized recommendations.

## Features

- 🔐 **User Authentication** - Login and registration system
- 📰 **Live News Feed** - Display news articles fetched from GNews API
- ⭐ **Personalized Recommendations** - News recommendations based on user click history
- 📊 **User Statistics** - Track clicks, reading history, and preferences
- 🎯 **Category Filtering** - Filter news by categories
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🔄 **Real-time Updates** - Fetch latest news directly from the API

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Ensure you have the model file:**
   - Make sure `news_classifier_model.pkl` is in the project directory

3. **Update API key (optional):**
   - Edit `app.py` and replace the `API_KEY` variable with your GNews API key

## Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser:**
   - Navigate to `http://localhost:5000`
   - The app will redirect to the login page

3. **Create an account:**
   - Click "Register here" on the login page
   - Fill in username, email (optional), and password
   - Click "Create Account"

4. **Login:**
   - Use your username and password to login

## Usage

### Dashboard

Once logged in, you'll see:

1. **Statistics Cards:**
   - Total Clicks
   - News Read
   - Favorite Category

2. **Controls:**
   - Category filter dropdown
   - "Fetch Latest News" button

3. **Personalized Recommendations:**
   - News articles recommended based on your reading history
   - Updates automatically as you click on articles

4. **News Feed:**
   - All available news articles
   - Filterable by category
   - Click any article to open it and record your interaction

5. **Reading History:**
   - List of all articles you've clicked on
   - Shows timestamp and categories

### Fetching News

1. Click the "Fetch Latest News" button
2. Enter a search query (e.g., "technology", "sports", "finance")
3. Set the number of articles to fetch (1-50)
4. Click "Fetch News"
5. The news will be classified and saved to the database
6. The feed will update automatically

### Interacting with News

- **Click any news card** to:
  - Open the article in a new tab
  - Record your click/interaction
  - Update your recommendations
  - Update your statistics

## API Endpoints

### Authentication
- `GET /` - Home page (redirects to login or dashboard)
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### News
- `GET /api/news/feed` - Get news feed (supports `category` and `limit` query params)
- `GET /api/news/recommendations` - Get personalized recommendations
- `POST /api/news/click` - Record a user click on a news item

### User
- `GET /api/user/stats` - Get user statistics
- `GET /api/user/history` - Get user click history

### Admin
- `POST /admin/fetch-news` - Fetch and save news from API

## Project Structure

```
recommendor_model/
├── app.py                      # Flask application
├── database.py                 # Database operations
├── database_integration.py     # API integration
├── user_interaction_helper.py  # User interaction management
├── requirements.txt           # Python dependencies
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/                    # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       └── dashboard.js
└── news_recommender.db        # SQLite database (created automatically)
```

## Database Schema

The application uses two main tables:

1. **users** - User accounts
   - user_id, username, email, password_hash, created_at, last_login

2. **news_items** - News articles
   - news_id, title, description, content, url, image_url, published_at, etc.

3. **user_interactions** - User clicks
   - interaction_id, user_id, news_id, interaction_type, timestamp

## Security Notes

⚠️ **Important:** Before deploying to production:

1. Change the `SECRET_KEY` in `app.py`:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
```

2. Use environment variables for sensitive data:
```bash
export SECRET_KEY='your-secret-key-here'
export API_KEY='your-api-key-here'
```

3. Consider using a production WSGI server (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Database not found
- The database will be created automatically on first run
- Make sure the directory is writable

### Model file not found
- Ensure `news_classifier_model.pkl` is in the project root
- The app will still work but won't be able to classify new articles

### API errors
- Check your GNews API key
- Verify you have API credits remaining
- Check your internet connection

## Development

To run in development mode with auto-reload:

```bash
export FLASK_ENV=development
python app.py
```

## License

This project is part of the News Recommender System.

