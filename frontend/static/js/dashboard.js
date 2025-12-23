// Dashboard JavaScript

let currentCategory = 'all';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    loadUserStats();
    loadRecommendations();
    loadNewsFeed();
    loadHistory();
    
    // Category filter change
    const categorySelect = document.getElementById('category-select');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            currentCategory = this.value;
            loadNewsFeed();
        });
    }
});

// Load categories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();
        
        const select = document.getElementById('category-select');
        if (select) {
            data.categories.forEach(cat => {
                if (cat !== 'all') {
                    const option = document.createElement('option');
                    option.value = cat;
                    option.textContent = cat.charAt(0).toUpperCase() + cat.slice(1);
                    select.appendChild(option);
                }
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load user statistics
async function loadUserStats() {
    try {
        const response = await fetch('/api/user/stats');
        const data = await response.json();
        
        if (data.stats) {
            document.getElementById('total-clicks').textContent = data.stats.total_clicks || 0;
            document.getElementById('unique-news').textContent = data.stats.unique_news_items || 0;
            document.getElementById('favorite-category').textContent = 
                data.preferences.favorite_category || '-';
        }
    } catch (error) {
        console.error('Error loading user stats:', error);
    }
}

// Load recommendations
async function loadRecommendations() {
    const grid = document.getElementById('recommendations-grid');
    if (!grid) return;
    
    grid.innerHTML = '<div class="loading">Loading recommendations...</div>';
    
    try {
        const response = await fetch('/api/news/recommendations?limit=6');
        const data = await response.json();
        
        if (data.news && data.news.length > 0) {
            grid.innerHTML = '';
            data.news.forEach(news => {
                grid.appendChild(createNewsCard(news));
            });
        } else {
            grid.innerHTML = '<div class="loading">No recommendations available. Start clicking on news to get personalized recommendations!</div>';
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
        grid.innerHTML = '<div class="loading">Error loading recommendations</div>';
    }
}

// Load news feed
async function loadNewsFeed() {
    const grid = document.getElementById('news-grid');
    if (!grid) return;
    
    grid.innerHTML = '<div class="loading">Loading news...</div>';
    
    try {
        const url = `/api/news/feed?category=${currentCategory}&limit=20`;
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.news && data.news.length > 0) {
            grid.innerHTML = '';
            data.news.forEach(news => {
                grid.appendChild(createNewsCard(news));
            });
        } else {
            grid.innerHTML = '<div class="loading">No news available. Click "Fetch Latest News" to load articles!</div>';
        }
    } catch (error) {
        console.error('Error loading news feed:', error);
        grid.innerHTML = '<div class="loading">Error loading news</div>';
    }
}

// Load history
async function loadHistory() {
    const list = document.getElementById('history-list');
    if (!list) return;
    
    list.innerHTML = '<div class="loading">Loading history...</div>';
    
    try {
        const response = await fetch('/api/user/history?limit=20');
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            list.innerHTML = '';
            data.history.forEach(item => {
                list.appendChild(createHistoryItem(item));
            });
        } else {
            list.innerHTML = '<div class="loading">No reading history yet. Start clicking on news articles!</div>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
        list.innerHTML = '<div class="loading">Error loading history</div>';
    }
}

// Create news card element
function createNewsCard(news) {
    const card = document.createElement('div');
    card.className = 'news-card';
    card.onclick = () => handleNewsClick(news.news_id, news.url);
    
    const imageUrl = news.image_url || 'https://via.placeholder.com/400x200?text=News';
    
    const tags = Array.isArray(news.top_3_labels) ? news.top_3_labels : [];
    const tagsHtml = tags.slice(0, 3).map(tag => 
        `<span class="news-tag">${tag}</span>`
    ).join('');
    
    card.innerHTML = `
        <img src="${imageUrl}" alt="${news.title}" class="news-card-image" onerror="this.src='https://via.placeholder.com/400x200?text=News'">
        <div class="news-card-content">
            <h3 class="news-card-title">${news.title}</h3>
            <p class="news-card-description">${news.description || ''}</p>
            <div class="news-card-footer">
                <div class="news-card-source">
                    <i class="fas fa-newspaper"></i>
                    <span>${news.source_name || 'Unknown Source'}</span>
                </div>
                <div class="news-card-tags">
                    ${tagsHtml}
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Create history item element
function createHistoryItem(item) {
    const listItem = document.createElement('div');
    listItem.className = 'news-list-item';
    listItem.onclick = () => window.open(item.url, '_blank');
    
    const tags = Array.isArray(item.top_3_labels) ? item.top_3_labels : [];
    const tagsHtml = tags.slice(0, 3).map(tag => 
        `<span class="news-tag">${tag}</span>`
    ).join('');
    
    listItem.innerHTML = `
        <div class="news-list-item-content">
            <h3 class="news-list-item-title">${item.title}</h3>
            <div class="news-list-item-meta">
                <span><i class="fas fa-clock"></i> ${formatDate(item.timestamp)}</span>
                <div class="news-card-tags">${tagsHtml}</div>
            </div>
        </div>
        <i class="fas fa-external-link-alt" style="color: var(--text-secondary);"></i>
    `;
    
    return listItem;
}

// Handle news click
async function handleNewsClick(newsId, url) {
    // Record click
    try {
        await fetch('/api/news/click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ news_id: newsId })
        });
        
        // Update stats
        loadUserStats();
        loadHistory();
        loadRecommendations();
    } catch (error) {
        console.error('Error recording click:', error);
    }
    
    // Open article in new tab
    window.open(url, '_blank');
}

// Fetch latest news modal
function fetchLatestNews() {
    const modal = document.getElementById('fetch-modal');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeFetchModal() {
    const modal = document.getElementById('fetch-modal');
    if (modal) {
        modal.classList.remove('active');
        document.getElementById('fetch-status').classList.remove('success', 'error');
        document.getElementById('fetch-status').style.display = 'none';
    }
}

async function submitFetchNews() {
    const query = document.getElementById('news-query').value;
    const count = parseInt(document.getElementById('news-count').value);
    const statusDiv = document.getElementById('fetch-status');
    
    if (!query) {
        statusDiv.textContent = 'Please enter a search query';
        statusDiv.className = 'fetch-status error';
        statusDiv.style.display = 'block';
        return;
    }
    
    statusDiv.textContent = 'Fetching news...';
    statusDiv.className = 'fetch-status';
    statusDiv.style.display = 'block';
    
    try {
        const response = await fetch('/admin/fetch-news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                max_results: count
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            statusDiv.textContent = `Successfully fetched ${data.count} news items!`;
            statusDiv.className = 'fetch-status success';
            
            // Reload news feed after a short delay
            setTimeout(() => {
                loadNewsFeed();
                loadRecommendations();
                closeFetchModal();
            }, 1500);
        } else {
            statusDiv.textContent = data.error || 'Error fetching news';
            statusDiv.className = 'fetch-status error';
        }
    } catch (error) {
        statusDiv.textContent = 'Error: ' + error.message;
        statusDiv.className = 'fetch-status error';
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const modal = document.getElementById('fetch-modal');
    if (modal && event.target === modal) {
        closeFetchModal();
    }
});

