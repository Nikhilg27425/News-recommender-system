# News Recommender System

A complete news recommendation system with machine learning classification, user interaction tracking, and a modern web interface.

🔗 **Live Demo**: [Deployed Link](https://newssphere-zvsv.onrender.com)

## 🚀 Features

- **Machine Learning Classification** - Multi-label news classification using scikit-learn
- **User Authentication** - Secure login and registration system
- **Live News Feed** - Fetch and display news from GNews API
- **Personalized Recommendations** - AI-powered recommendations based on user behavior
- **Database System** - SQLite database for news items and user interactions
- **Modern Web UI** - Beautiful, responsive web interface
- **Category Filtering** - Filter news by categories
- **Reading History** - Track all articles you've read
- **User Statistics** - View your reading patterns and preferences

## 📁 Project Structure

```
recommendor_model/
├── backend/                    # Backend Python application
│   ├── ai_models/             # AI/ML models
│   │   └── news_classifier_model.pkl
│   ├── app.py                 # Main Flask application
│   ├── database.py            # Database operations
│   ├── database_integration.py # API integration
│   ├── user_interaction_helper.py # User interaction management
│   ├── example_usage.py       # Usage examples
│   ├── *.ipynb               # Jupyter notebooks
│   ├── sports_classified_news.csv # Training data
│   └── news_recommender.db    # SQLite database
│
├── frontend/                   # Frontend assets
│   ├── static/                # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── dashboard.js
│   │       └── main.js
│   └── templates/             # HTML templates
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       └── register.html
│
├── deployment/                 # Deployment documentation
│   └── DEPLOYMENT.md          # Deployment instructions
│
├── requirements.txt           # Python dependencies
├── Procfile                   # Heroku/Render deployment
├── render.yaml               # Render deployment config
├── runtime.txt               # Python version specification
├── run.sh                    # Local development script
├── LICENSE                   # MIT License
└── README.md                 # This documentation
```

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd recommendor_model
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

1. **Start the web application:**
```bash
./run.sh
```

2. **Open your browser:**
   - Navigate to `http://localhost:5001`
   - Register a new account
   - Start exploring!

3. **Fetch news:**
   - Click "Fetch Latest News" button
   - Enter a topic (e.g., "technology", "sports")
   - Articles will be classified and saved automatically

## 🗄️ Database Schema

The system uses two main databases:

1. **news_items** - Stores news articles with classifications
2. **user_interactions** - Tracks user clicks and preferences

The database is automatically initialized when you first run the application.

## 🔧 Configuration

### API Key
Update the `API_KEY` in `backend/app.py` with your GNews API key:
```python
API_KEY = "your-api-key-here"
```

### Port
The default port is 5001. To change it, edit `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📊 Model Training

The news classification model is trained using:
- Multi-label classification
- TF-IDF vectorization
- Random Forest classifier
- Top-K prediction strategy

See `backend/News_classifier.ipynb` for training details.

## 🎯 Usage Examples

### Fetch and Classify News
```python
from backend.database_integration import fetch_and_save_news

fetch_and_save_news(
    api_key="your-api-key",
    query="technology",
    max_results=10
)
```

### Record User Interaction
```python
from backend.database import NewsDatabase

db = NewsDatabase()
db.record_user_interaction("user_123", "news_id_456", "click")
db.close()
```

### Get Recommendations
```python
from backend.user_interaction_helper import UserInteractionManager

manager = UserInteractionManager()
recommendations = manager.get_recommendations_for_user("user_123", limit=10)
manager.close()
```

## 🧪 Testing

Run the example script to test the system:
```bash
cd backend
python example_usage.py
```

## 📝 API Endpoints

- `GET /` - Home page
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /dashboard` - Main dashboard
- `GET /api/news/feed` - Get news feed
- `GET /api/news/recommendations` - Get recommendations
- `POST /api/news/click` - Record click
- `GET /api/user/stats` - User statistics
- `GET /api/user/history` - Reading history

## 🔒 Security Notes

⚠️ **Before deploying to production:**
- Change the `SECRET_KEY` in `backend/app.py`
- Use environment variables for sensitive data
- Consider using a production WSGI server (Gunicorn)
- Enable HTTPS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the **MIT License**.

## 🙏 Acknowledgments

- GNews API for news data
- scikit-learn for machine learning
- Flask for web framework

## 📧 Contact

For any inquiries or collaborations, reach out to:
📧 Email: 23UCS752@lnmiit.ac.com
📌 GitHub: [Nikhil Gupta](https://github.com/Nikhilg27425)

---

**Happy News Reading! 📰**

