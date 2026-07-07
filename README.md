# NewsSphere — AI-Powered News Recommender

A full-stack MERN-style news recommendation system combining a React frontend with a Python/Flask API backend, machine learning classification, and OAuth authentication.

🔗 **Live Demo**: [newssphere-zvsv.onrender.com](https://newssphere-zvsv.onrender.com)

> **Demo credentials** — no sign-up required:
> Click **"⚡ Try Demo"** on the login page, or use `demo / demo123`

---

## ✨ What's New (MERN Rebuild)

The project has been completely rebuilt with a modern React frontend replacing the old Jinja2 templates:

- **React + Vite frontend** — 10 fully responsive pages with dark theme
- **Google OAuth & GitHub OAuth** — one-click sign-in
- **JWT authentication** — stateless, works across domains
- **Live news via GNews API** — category tabs fetch fresh articles in real time
- **AI recommendation engine** — "For You" feed learns from your click history
- **Bookmarks system** — save articles to named collections, share URLs
- **Real analytics dashboard** — daily activity chart, category affinity, top sources (all from actual data)
- **Functional profile page** — edit username/email, change password
- **Fully deployed on Render** — static site (frontend) + web service (backend)

---

## 🚀 Features

- **Machine Learning Classification** — multi-label news classification using scikit-learn (TF-IDF + Random Forest)
- **Live News Feed** — fetch fresh articles from GNews API by category (Technology, Science, Sports, Finance, Health…)
- **Personalized Recommendations** — "For You" tab serves articles based on your click history; cold-start falls back to popular news
- **Google & GitHub OAuth** — full OAuth 2.0 flow, no passwords required
- **Email/Password Auth** — traditional register/login with bcrypt hashing + JWT tokens
- **Bookmarks & Collections** — save articles, create named collections, delete, share by copying URL
- **Personal Analytics** — real charts: daily reading activity, category distribution, top sources, recent reads
- **Explore & Search** — domain filters, trend pills, recency sort, full-text search — all hit the live API
- **Responsive Design** — mobile bottom nav, tablet layout, desktop sidebar

---

## 📁 Project Structure

```
recommendor_model/
├── backend/                        # Flask API
│   ├── ai_models/
│   │   └── news_classifier_model.pkl   # Trained ML model
│   ├── app.py                      # Main Flask app (JWT, OAuth, all API routes)
│   ├── database.py                 # SQLite operations (news_items, user_interactions)
│   ├── database_integration.py     # GNews API fetch + classify + save pipeline
│   ├── user_interaction_helper.py  # Recommendation logic
│   └── News_classifier.ipynb       # Model training notebook
│
├── client/                         # React + Vite frontend
│   ├── public/
│   │   └── _redirects              # Render SPA fallback rule
│   ├── src/
│   │   ├── components/layout/      # Sidebar, Topbar, AppLayout
│   │   ├── context/AuthContext.jsx # JWT token + user state
│   │   ├── pages/                  # 10 pages (see below)
│   │   ├── services/api.js         # Centralised API service
│   │   └── index.css               # Global dark theme + responsive breakpoints
│   ├── package.json
│   └── vite.config.js
│
├── deployment/
│   └── DEPLOYMENT.md               # Render deployment guide
│
├── render.yaml                     # Render Blueprint (2 services)
├── requirements.txt                # Python dependencies
├── Procfile                        # Gunicorn start command
├── runtime.txt                     # Python 3.11
└── README.md
```

### Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Landing | Hero, trending cards, features, CTA |
| `/login` | Login | Email/password + Google + GitHub + Demo button |
| `/signup` | Sign Up | Register with email or OAuth |
| `/onboarding` | Onboarding | Category preference selection |
| `/feed` | Personalized Feed | "For You" recommendations + live category tabs |
| `/explore` | Explore | Search, domain filters, trend pills |
| `/bookmarks` | Bookmarks | Collections, save/delete/share |
| `/analytics` | Analytics | Real charts from your reading data |
| `/profile` | Profile & Settings | Edit profile, change password |
| `/auth/callback` | OAuth Callback | Handles Google/GitHub redirect |

---

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend

```bash
# Clone
git clone https://github.com/Nikhilg27425/News-recommender-system.git
cd News-recommender-system

# Python env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create backend/.env (copy and fill in)
cp backend/.env.example backend/.env   # or create manually

# Start Flask (port 5001)
cd backend && python app.py
```

### Frontend

```bash
# In a separate terminal
cd client
npm install
npm run dev   # → http://localhost:5173
```

### Environment Variables (backend/.env)

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Google OAuth (console.cloud.google.com)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:5001/api/auth/google/callback

# GitHub OAuth (github.com/settings/developers)
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
GITHUB_REDIRECT_URI=http://localhost:5001/api/auth/github/callback

FRONTEND_URL=http://localhost:5173
GNEWS_API_KEY=your-gnews-api-key
```

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Email/password registration |
| POST | `/api/auth/login` | Email/password login |
| GET  | `/api/auth/me` | Get current user (JWT required) |
| GET  | `/api/auth/google` | Get Google OAuth URL |
| GET  | `/api/auth/google/callback` | Google OAuth callback |
| GET  | `/api/auth/github` | Get GitHub OAuth URL |
| GET  | `/api/auth/github/callback` | GitHub OAuth callback |

### News
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/news/feed?category=&limit=` | Articles from DB by category |
| GET | `/api/news/live?category=&limit=` | Fresh articles from GNews API |
| GET | `/api/news/recommendations` | Personalised recommendations |
| GET | `/api/news/trending` | Most-clicked articles |
| GET | `/api/news/search?q=` | Full-text search |
| POST | `/api/news/click` | Record article click (trains recommender) |

### Bookmarks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookmarks/collections` | List user's collections |
| POST | `/api/bookmarks/collections` | Create new collection |
| DELETE | `/api/bookmarks/collections/:id` | Delete collection |
| GET | `/api/bookmarks` | Get bookmarks (optional `?collection_id=`) |
| POST | `/api/bookmarks` | Save article to collection |
| DELETE | `/api/bookmarks/:id` | Remove bookmark |
| GET | `/api/bookmarks/check/:news_id` | Check if article is bookmarked |

### User
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/analytics` | Full analytics (charts data) |
| GET | `/api/user/profile` | Get profile details |
| PUT | `/api/user/profile` | Update username/email |
| POST | `/api/user/change-password` | Change password |
| GET | `/api/user/history` | Reading history |

---

## 🗄️ Database Schema

```
news_items          — articles fetched from GNews + ML labels
user_interactions   — click tracking (drives recommendations)
users               — accounts (email/password + Google/GitHub OAuth)
bookmark_collections — named collections per user
bookmarks           — saved articles linked to collections
```

---

## 🤖 ML Model

- **Architecture**: Multi-label classifier (one estimator per class, scikit-learn)
- **Input**: TF-IDF vectorized text (title + description + content)
- **Output**: Top-3 category labels per article (news, finance, sports, health, travel…)
- **Threshold**: 0.3 probability cutoff for label assignment
- **Training**: See `backend/News_classifier.ipynb`

---

## 🚢 Deployment (Render)

Two services defined in `render.yaml`:

| Service | Type | Description |
|---------|------|-------------|
| `newssphere-api` | Web Service (Python) | Flask API backend |
| `newssphere` | Static Site | React frontend |

See [`deployment/DEPLOYMENT.md`](deployment/DEPLOYMENT.md) for full step-by-step guide.

---

## 🔒 Security

- Passwords hashed with `werkzeug.security` (bcrypt)
- JWT tokens expire after 7 days
- CORS restricted to known frontend origins
- OAuth credentials stored as environment variables only — never committed
- `.env` is in `.gitignore`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch and open a pull request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [GNews API](https://gnews.io) — news data source
- [scikit-learn](https://scikit-learn.org) — ML classification
- [Flask](https://flask.palletsprojects.com) — Python web framework
- [React](https://react.dev) + [Vite](https://vitejs.dev) — frontend stack
- [Recharts](https://recharts.org) — analytics charts
- [Render](https://render.com) — hosting

---

## 📧 Contact

For inquiries or collaborations:

📧 Email: 23UCS752@lnmiit.ac.com
📌 GitHub: [Nikhil Gupta](https://github.com/Nikhilg27425)

---

**Happy News Reading! 📰**
