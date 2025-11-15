# News Recommender Database System

This system provides two main databases for the news recommender pipeline:

1. **News Items Database** - Stores news articles fetched from the API
2. **User Interactions Database** - Stores user clicks and interactions with news items

## Database Schema

### 1. `news_items` Table
Stores news articles with the following fields:
- `news_id` (PRIMARY KEY) - Unique identifier for each news item
- `title` - News article title
- `description` - Article description
- `content` - Full article content
- `url` - Article URL
- `image_url` - Article image URL
- `published_at` - Publication timestamp
- `source_name` - News source name
- `source_url` - News source URL
- `language` - Article language (default: 'en')
- `country` - Country code (default: 'us')
- `predicted_labels` - JSON array of predicted categories
- `top_3_labels` - JSON array of top 3 predicted categories
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### 2. `user_interactions` Table
Stores user interactions with news items:
- `interaction_id` (PRIMARY KEY) - Auto-incrementing ID
- `user_id` - User identifier
- `news_id` - Foreign key to news_items table
- `interaction_type` - Type of interaction (default: 'click')
- `timestamp` - When the interaction occurred

## Installation

No additional installation required. The system uses SQLite (built into Python) and standard libraries:
- `sqlite3` (built-in)
- `pandas`
- `json` (built-in)

## Usage

### 1. Fetch and Save News from API

```python
from database_integration import fetch_and_save_news

API_KEY = "your_api_key_here"

# Fetch news for a topic and save to database
fetch_and_save_news(
    api_key=API_KEY,
    query="technology",
    max_results=10,
    db_path="news_recommender.db"
)
```

### 2. Record User Interactions

```python
from database import NewsDatabase

db = NewsDatabase("news_recommender.db")

# Record a user click
db.record_user_interaction(
    user_id="user_123",
    news_id="abc123def456",
    interaction_type="click"
)

db.close()
```

### 3. Get User History

```python
from database import NewsDatabase

db = NewsDatabase("news_recommender.db")

# Get all interactions for a user
user_history = db.get_user_interactions("user_123", limit=50)
print(user_history)

db.close()
```

### 4. Get Recommendations

```python
from user_interaction_helper import UserInteractionManager

manager = UserInteractionManager("news_recommender.db")

# Get recommendations based on user's click history
recommendations = manager.get_recommendations_for_user("user_123", limit=10)
print(recommendations)

manager.close()
```

### 5. Query News Items

```python
from database import NewsDatabase

db = NewsDatabase("news_recommender.db")

# Get all news items
all_news = db.get_all_news_items(limit=100)

# Get news by category
sports_news = db.get_news_by_category("sports")

# Get popular news
popular = db.get_popular_news(limit=10)

db.close()
```

## Main Classes and Functions

### `NewsDatabase` Class

Main database handler with methods:

**News Items Operations:**
- `insert_news_item(news_data)` - Insert a single news item
- `insert_news_items_batch(news_items)` - Insert multiple news items
- `get_news_item(news_id)` - Get a single news item by ID
- `get_all_news_items(limit, order_by)` - Get all news items
- `get_news_by_category(category)` - Get news by category
- `news_item_exists(news_id)` - Check if news item exists

**User Interactions Operations:**
- `record_user_interaction(user_id, news_id, interaction_type)` - Record interaction
- `get_user_interactions(user_id, limit)` - Get user's interaction history
- `get_user_clicked_news_ids(user_id)` - Get list of clicked news IDs
- `get_news_interaction_count(news_id)` - Get click count for a news item
- `get_popular_news(limit)` - Get most popular news items
- `get_user_statistics(user_id)` - Get user statistics

**Utility Methods:**
- `get_database_stats()` - Get overall database statistics
- `clear_old_news(days)` - Delete old news items

### `UserInteractionManager` Class

High-level manager for user interactions:

- `record_click(user_id, news_id)` - Record a click
- `get_user_history(user_id, limit)` - Get user history
- `get_user_preferences(user_id)` - Analyze user preferences
- `get_recommendations_for_user(user_id, limit)` - Get recommendations
- `get_user_statistics(user_id)` - Get user statistics

## Running Examples

Run the example script to see the system in action:

```bash
python example_usage.py
```

## Database File

The database is stored as a SQLite file: `news_recommender.db`

This file will be created automatically when you first use the `NewsDatabase` class.

## Integration with Existing Pipeline

To integrate with your existing notebooks:

1. **In your news fetching notebook**, add:
```python
from database_integration import save_news_to_database, classify_news_articles

# After classifying articles
df_classified = classify_news_articles(df_articles, "news_classifier_model.pkl")

# Save to database
save_news_to_database(df_classified, "news_recommender.db")
```

2. **For user interactions**, add:
```python
from user_interaction_helper import record_user_click

# When user clicks on a news item
record_user_click(user_id="user_123", news_id=news_id)
```

## Scheduled Updates

You can set up a cron job or scheduled task to periodically fetch and save news:

```python
# Example: Run every hour
import schedule
import time
from database_integration import fetch_and_save_news

def update_news():
    API_KEY = "your_api_key"
    topics = ["technology", "sports", "finance", "health"]
    for topic in topics:
        fetch_and_save_news(API_KEY, query=topic, max_results=10)

schedule.every().hour.do(update_news)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Notes

- The database uses SQLite, which is file-based and doesn't require a separate server
- News IDs are automatically generated from URLs if not provided
- The system handles duplicate news items (uses INSERT OR REPLACE)
- User interactions are linked to news items via foreign keys
- All timestamps are stored in ISO format

