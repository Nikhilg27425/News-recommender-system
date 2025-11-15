"""
Flask Web Application for News Recommender System
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import NewsDatabase
from database_integration import fetch_news_from_api, classify_news_articles, save_news_to_database
from user_interaction_helper import UserInteractionManager
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configuration
DB_PATH = "news_recommender.db"
API_KEY = "172285a1b5b6f981c517e59461b31a9a"  # Replace with your API key
MODEL_PATH = "news_classifier_model.pkl"

# Initialize database for user management
def init_user_db():
    """Initialize user authentication database"""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize on startup
init_user_db()


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password', 'error')
            return render_template('login.html')
        
        db = NewsDatabase(DB_PATH)
        conn = db._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, username, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            
            # Update last login
            cursor.execute("UPDATE users SET last_login = ? WHERE user_id = ?", 
                         (datetime.now().isoformat(), user[0]))
            conn.commit()
            
            db.close()
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            db.close()
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        db = NewsDatabase(DB_PATH)
        conn = db._get_connection()
        cursor = conn.cursor()
        
        # Check if username exists
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            db.close()
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        # Check if email exists
        if email:
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                db.close()
                flash('Email already registered', 'error')
                return render_template('register.html')
        
        # Create new user
        user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        password_hash = generate_password_hash(password)
        created_at = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO users (user_id, username, email, password_hash, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, email, password_hash, created_at))
        
        conn.commit()
        db.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session.get('username'))


@app.route('/api/news/feed')
def news_feed():
    """Get news feed for the user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    category = request.args.get('category', 'all')
    limit = int(request.args.get('limit', 20))
    
    db = NewsDatabase(DB_PATH)
    
    if category == 'all':
        news_df = db.get_all_news_items(limit=limit)
    else:
        news_df = db.get_news_by_category(category)
        news_df = news_df.head(limit)
    
    # Convert to JSON
    news_list = []
    for _, row in news_df.iterrows():
        news_list.append({
            'news_id': row['news_id'],
            'title': row['title'],
            'description': row['description'][:200] + '...' if len(str(row['description'])) > 200 else row['description'],
            'url': row['url'],
            'image_url': row.get('image_url', ''),
            'published_at': row['published_at'],
            'source_name': row.get('source_name', 'Unknown'),
            'top_3_labels': row.get('top_3_labels', []) if isinstance(row.get('top_3_labels'), list) else json.loads(row.get('top_3_labels', '[]')),
            'predicted_labels': row.get('predicted_labels', []) if isinstance(row.get('predicted_labels'), list) else json.loads(row.get('predicted_labels', '[]'))
        })
    
    db.close()
    
    return jsonify({'news': news_list})


@app.route('/api/news/recommendations')
def recommendations():
    """Get personalized recommendations for the user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    limit = int(request.args.get('limit', 10))
    
    manager = UserInteractionManager(DB_PATH)
    recommendations_df = manager.get_recommendations_for_user(user_id, limit=limit)
    manager.close()
    
    news_list = []
    for _, row in recommendations_df.iterrows():
        news_list.append({
            'news_id': row['news_id'],
            'title': row['title'],
            'description': row['description'][:200] + '...' if len(str(row['description'])) > 200 else row['description'],
            'url': row['url'],
            'image_url': row.get('image_url', ''),
            'published_at': row['published_at'],
            'source_name': row.get('source_name', 'Unknown'),
            'top_3_labels': row.get('top_3_labels', []) if isinstance(row.get('top_3_labels'), list) else json.loads(row.get('top_3_labels', '[]'))
        })
    
    return jsonify({'news': news_list})


@app.route('/api/news/click', methods=['POST'])
def record_click():
    """Record a user click on a news item"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    news_id = data.get('news_id')
    
    if not news_id:
        return jsonify({'error': 'news_id required'}), 400
    
    user_id = session['user_id']
    db = NewsDatabase(DB_PATH)
    
    success = db.record_user_interaction(user_id, news_id, 'click')
    db.close()
    
    if success:
        return jsonify({'success': True, 'message': 'Click recorded'})
    else:
        return jsonify({'error': 'Failed to record click'}), 500


@app.route('/api/user/stats')
def user_stats():
    """Get user statistics"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    manager = UserInteractionManager(DB_PATH)
    stats = manager.get_user_statistics(user_id)
    preferences = manager.get_user_preferences(user_id)
    manager.close()
    
    return jsonify({
        'stats': stats,
        'preferences': preferences
    })


@app.route('/api/user/history')
def user_history():
    """Get user click history"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    limit = int(request.args.get('limit', 50))
    
    db = NewsDatabase(DB_PATH)
    history_df = db.get_user_interactions(user_id, limit=limit)
    db.close()
    
    history_list = []
    for _, row in history_df.iterrows():
        history_list.append({
            'news_id': row['news_id'],
            'title': row.get('title', 'N/A'),
            'url': row.get('url', ''),
            'timestamp': row['timestamp'],
            'top_3_labels': row.get('top_3_labels', []) if isinstance(row.get('top_3_labels'), list) else json.loads(row.get('top_3_labels', '[]'))
        })
    
    return jsonify({'history': history_list})


# ==================== ADMIN ROUTES ====================

@app.route('/admin/fetch-news', methods=['POST'])
def admin_fetch_news():
    """Admin endpoint to fetch and save news from API"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    query = data.get('query', 'technology')
    max_results = int(data.get('max_results', 10))
    
    try:
        # Fetch news from API
        df = fetch_news_from_api(API_KEY, query, max_results)
        
        if df.empty:
            return jsonify({'error': 'No news found'}), 404
        
        # Classify articles
        df = classify_news_articles(df, MODEL_PATH)
        
        # Save to database
        count = save_news_to_database(df, DB_PATH)
        
        return jsonify({
            'success': True,
            'message': f'Successfully fetched and saved {count} news items',
            'count': count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories')
def get_categories():
    """Get list of available news categories"""
    categories = [
        'all', 'technology', 'sports', 'finance', 'health', 
        'entertainment', 'news', 'travel', 'lifestyle', 'foodanddrink',
        'autos', 'movies', 'music', 'tv', 'video', 'weather'
    ]
    return jsonify({'categories': categories})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

