# Alexandria Library - Web Edition (Pure Python)

## 🎯 Revised Vision

**Pure Python web application** with server-side rendering. No JavaScript frameworks. Deployable to Railway/Render/Fly.io (not Vercel - Vercel requires JS).

**Aesthetic**: Oregon Trail meets Library of Alexandria meets Wikipedia meets Google Docs meets Dashboard Pipeline Tool. 8-bit retro vibes welcome.

---

## 🏗️ Technical Stack (Pure Python)

### Backend Framework: **Flask** or **FastAPI**
- **Flask**: Simpler, more Pythonic, great for server-side rendering
- **FastAPI**: Modern, async, but more complex
- **Decision**: **Flask** for simplicity and server-side rendering

### Template Engine: **Jinja2** (comes with Flask)
- Server-side HTML generation
- No client-side JS needed for basic interactivity
- Can add minimal vanilla JS for enhanced UX (but not required)

### Styling: **Pure CSS** (with 8-bit retro theme)
- Custom CSS framework
- Retro pixel fonts
- ASCII art elements
- Terminal/command-line aesthetic

### Deployment: **Railway** or **Render**
- Both support Python apps perfectly
- Easy deployment
- Free tier available
- Better than Vercel for Python

---

## 🎨 Design Aesthetic: "Oregon Trail + Library of Alexandria"

### Visual Style
- **8-bit retro fonts** (Press Start 2P, VT323, Courier)
- **Terminal/command-line** aesthetic
- **ASCII art** headers and dividers
- **Retro color palette**: Green on black, amber on dark, classic terminal colors
- **Grid-based layouts** (like old games)
- **Text-heavy** (like Wikipedia)
- **Dashboard-style** metrics and progress bars
- **Library card catalog** feel

### UI Elements
```
┌─────────────────────────────────────────────────────────┐
│  ╔═══════════════════════════════════════════════════╗  │
│  ║   ALEXANDRIA LIBRARY v1.0                        ║  │
│  ║   [████████████░░░░░░] 67% Complete              ║  │
│  ╚═══════════════════════════════════════════════════╝  │
│                                                          │
│  > LIBRARY (142 books) | DISCOVER | DOWNLOADS | SETTINGS│
│  ────────────────────────────────────────────────────── │
│                                                          │
│  [SEARCH: _______________] [FILTER ▼] [SORT: Title ▼]  │
│                                                          │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                 │
│  │ 📖   │ │ 📖   │ │ 📖   │ │ 📖   │                 │
│  │Title │ │Title │ │Title │ │Title │                 │
│  │Author│ │Author│ │Author│ │Author│                 │
│  │[PDF] │ │[PDF] │ │[PDF] │ │[PDF] │                 │
│  └──────┘ └──────┘ └──────┘ └──────┘                 │
│                                                          │
│  STATUS: 142 READY | 8 DOWNLOADING | 3 SEARCHING       │
└─────────────────────────────────────────────────────────┘
```

### Color Palette (Retro Terminal)
```css
--bg-dark: #0a0a0a;        /* Deep black */
--bg-darker: #1a1a1a;      /* Slightly lighter */
--text-green: #00ff41;     /* Terminal green */
--text-amber: #ffb000;     /* Amber/orange */
--text-white: #ffffff;     /* White */
--accent-blue: #0080ff;    /* Bright blue */
--border-gray: #404040;    /* Gray borders */
--success-green: #00ff00;  /* Success green */
--warning-yellow: #ffff00; /* Warning yellow */
```

---

## 🏛️ Architecture (Flask Server-Side)

### Project Structure
```
alexandria_library_web/
├── app.py                  # Flask application entry
├── config.py              # Configuration
├── requirements.txt        # Dependencies
│
├── core/                   # Core engine (same as before)
│   ├── database.py
│   ├── discovery.py
│   ├── downloader.py
│   └── renamer.py
│
├── models/                 # Data models
│   └── book.py
│
├── routes/                 # Flask routes
│   ├── __init__.py
│   ├── library.py         # Library view routes
│   ├── discover.py        # Discovery routes
│   ├── download.py        # Download routes
│   └── api.py             # API endpoints (if needed)
│
├── templates/              # Jinja2 templates
│   ├── base.html          # Base template
│   ├── library.html       # Library view
│   ├── discover.html      # Discovery panel
│   ├── download.html      # Download queue
│   └── book_detail.html   # Book details
│
├── static/                 # Static files
│   ├── css/
│   │   ├── main.css       # Main stylesheet
│   │   └── retro.css      # 8-bit retro theme
│   ├── fonts/             # Retro fonts
│   └── images/            # Images, icons
│
└── utils/                  # Utilities
    ├── parsers.py
    └── helpers.py
```

---

## 🔄 End-to-End Flow (Web Version)

### Flow 1: Paste List → Discover → Download → Rename

```
1. USER VISITS SITE
   └─> Flask serves library.html
       └─> Shows current library (if any)

2. USER CLICKS "DISCOVER"
   └─> Flask serves discover.html
       └─> User pastes book list in <textarea>
           └─> Submits form (POST to /discover/start)

3. SERVER PROCESSES LIST
   └─> Flask route parses book list
       └─> Stores in database
           └─> Starts background discovery (Celery or threading)
               └─> Redirects to /discover/progress

4. PROGRESS PAGE (Auto-refresh)
   └─> Flask serves progress.html
       └─> Shows discovery status
           └─> Auto-refreshes every 2 seconds (meta refresh or form)
               └─> When complete, redirects to results

5. RESULTS PAGE
   └─> Flask serves discover_results.html
       └─> Shows found PDFs per book
           └─> User selects PDFs to download
               └─> Submits form (POST to /download/queue)

6. DOWNLOAD QUEUE
   └─> Flask serves download.html
       └─> Shows download progress
           └─> Auto-refreshes to show progress
               └─> Downloads happen server-side
                   └─> Files saved to server storage

7. AUTO-RENAME
   └─> After download completes
       └─> Server triggers rename engine
           └─> Updates database
               └─> Redirects to library view

8. LIBRARY VIEW
   └─> Flask serves library.html
       └─> Shows all books with status
           └─> User can browse, search, filter
```

---

## 🎨 Flask Application Structure

### Main App (`app.py`)

```python
from flask import Flask, render_template, request, redirect, url_for, jsonify
from core.database import BookDatabase
from core.discovery import PDFDiscoveryEngine
from core.downloader import DownloadManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Initialize core components
db = BookDatabase('data/books.db')
discovery = PDFDiscoveryEngine()
downloader = DownloadManager()

@app.route('/')
def index():
    """Main library view"""
    books = db.get_all_books()
    stats = db.get_statistics()
    return render_template('library.html', books=books, stats=stats)

@app.route('/discover', methods=['GET', 'POST'])
def discover():
    """Discovery panel"""
    if request.method == 'POST':
        book_list_text = request.form.get('book_list', '')
        # Parse and start discovery
        books = parse_book_list(book_list_text)
        discovery.start_discovery(books)
        return redirect(url_for('discover_progress'))
    return render_template('discover.html')

@app.route('/discover/progress')
def discover_progress():
    """Show discovery progress"""
    progress = discovery.get_progress()
    return render_template('discover_progress.html', progress=progress)

@app.route('/download/queue', methods=['POST'])
def queue_downloads():
    """Queue selected PDFs for download"""
    selected_pdfs = request.form.getlist('pdf_urls')
    downloader.queue_downloads(selected_pdfs)
    return redirect(url_for('download_queue'))

@app.route('/download/queue')
def download_queue():
    """Show download queue"""
    queue = downloader.get_queue_status()
    return render_template('download.html', queue=queue)

# ... more routes
```

### Base Template (`templates/base.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Alexandria Library{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/retro.css') }}">
</head>
<body>
    <div class="container">
        <header class="header">
            <pre class="ascii-art">
╔═══════════════════════════════════════════════════╗
║   ALEXANDRIA LIBRARY v1.0                        ║
╚═══════════════════════════════════════════════════╝
            </pre>
            <nav class="nav">
                <a href="{{ url_for('index') }}">LIBRARY</a> |
                <a href="{{ url_for('discover') }}">DISCOVER</a> |
                <a href="{{ url_for('download_queue') }}">DOWNLOADS</a> |
                <a href="{{ url_for('settings') }}">SETTINGS</a>
            </nav>
        </header>
        
        <main class="main">
            {% block content %}{% endblock %}
        </main>
        
        <footer class="footer">
            STATUS: {{ stats.ready }} READY | {{ stats.downloading }} DOWNLOADING | {{ stats.searching }} SEARCHING
        </footer>
    </div>
</body>
</html>
```

### Library Template (`templates/library.html`)

```html
{% extends "base.html" %}

{% block content %}
<div class="library-view">
    <div class="controls">
        <form method="GET" action="{{ url_for('index') }}" class="search-form">
            <input type="text" name="search" placeholder="SEARCH LIBRARY..." value="{{ request.args.get('search', '') }}">
            <select name="filter">
                <option value="">ALL BOOKS</option>
                <option value="ready">READY</option>
                <option value="downloading">DOWNLOADING</option>
            </select>
            <button type="submit">SEARCH</button>
        </form>
    </div>
    
    <div class="book-grid">
        {% for book in books %}
        <div class="book-card">
            <div class="book-cover">📖</div>
            <div class="book-title">{{ book.title }}</div>
            <div class="book-author">{{ book.author }}</div>
            <div class="book-status status-{{ book.status.lower() }}">{{ book.status }}</div>
            {% if book.pdf_path %}
            <a href="{{ url_for('view_book', book_id=book.id) }}" class="btn-view">VIEW</a>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

---

## 🎨 CSS Styling (Retro 8-bit)

### Main CSS (`static/css/main.css`)

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Courier New', monospace;
    background: #0a0a0a;
    color: #00ff41;
    line-height: 1.6;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    border: 2px solid #00ff41;
    padding: 20px;
    margin-bottom: 20px;
    background: #1a1a1a;
}

.ascii-art {
    color: #ffb000;
    font-size: 12px;
    margin: 0;
}

.nav {
    margin-top: 10px;
    font-size: 14px;
}

.nav a {
    color: #00ff41;
    text-decoration: none;
    margin: 0 10px;
}

.nav a:hover {
    color: #ffb000;
    text-decoration: underline;
}

.book-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.book-card {
    border: 1px solid #404040;
    padding: 15px;
    background: #1a1a1a;
    transition: border-color 0.2s;
}

.book-card:hover {
    border-color: #00ff41;
}

.book-cover {
    font-size: 48px;
    text-align: center;
    margin-bottom: 10px;
}

.book-title {
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 5px;
}

.book-author {
    color: #808080;
    font-size: 12px;
    margin-bottom: 10px;
}

.status-ready {
    color: #00ff00;
}

.status-downloading {
    color: #ffb000;
}

.status-searching {
    color: #0080ff;
}

.btn-view {
    display: inline-block;
    padding: 5px 10px;
    background: #00ff41;
    color: #000000;
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-family: 'Courier New', monospace;
}

.btn-view:hover {
    background: #ffb000;
}
```

---

## 🚀 Deployment (Railway/Render)

### Railway Deployment

1. **Create `Procfile`**:
```
web: gunicorn app:app
```

2. **Create `railway.json`** (optional):
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT"
  }
}
```

3. **Deploy**:
   - Connect GitHub repo to Railway
   - Railway auto-detects Python
   - Sets up environment
   - Deploys automatically

### Render Deployment

1. **Create `render.yaml`**:
```yaml
services:
  - type: web
    name: alexandria-library
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

2. **Deploy**:
   - Connect GitHub repo
   - Render auto-detects and deploys

---

## ✅ Advantages of This Approach

1. **Pure Python**: No JS frameworks needed
2. **Server-Side Rendering**: Fast, SEO-friendly
3. **Simple Deployment**: Railway/Render handle everything
4. **Retro Aesthetic**: Perfect for 8-bit theme
5. **Shareable**: Friends can access via URL
6. **No Client-Side Complexity**: All logic on server

---

## ⚠️ Limitations

1. **Page Refreshes**: For progress updates (can use meta refresh or form auto-submit)
2. **No Real-Time**: Would need WebSockets for true real-time (adds complexity)
3. **Server Resources**: Downloads happen on server (need storage)
4. **Not Vercel**: Can't use Vercel (requires JS)

---

## 🎯 Recommendation

**Go with Flask + Server-Side Rendering + Railway/Render**

- ✅ Pure Python (minimal JS if any)
- ✅ Deployable and shareable
- ✅ Perfect for retro aesthetic
- ✅ Simple and robust
- ✅ Friends can use it via URL

**Next Steps:**
1. Build Flask app structure
2. Create retro-styled templates
3. Integrate existing discovery/download/rename logic
4. Deploy to Railway
5. Share URL with friends

**Ready to build?** 🚀

