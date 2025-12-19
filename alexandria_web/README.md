# Alexandria Library - Web Edition

Pure Python web application for discovering, downloading, and managing PDF books. Retro 8-bit terminal aesthetic.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit http://localhost:5000
```

### Deploy to Railway

1. **Create account** at [railway.app](https://railway.app)

2. **Connect GitHub repo** (or push code)

3. **Railway auto-detects** Python and Flask

4. **Set environment variables** (optional):
   - `PDF_DIRECTORY`: Where to store PDFs (default: `./pdf`)
   - `DATABASE_PATH`: Database location (default: `./data/books.db`)
   - `SECRET_KEY`: Flask secret key (auto-generated)

5. **Deploy!** Railway handles everything

### Deploy to Render

1. **Create account** at [render.com](https://render.com)

2. **New Web Service** → Connect GitHub repo

3. **Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

4. **Deploy!**

## 📁 Project Structure

```
alexandria_web/
├── app.py              # Flask application
├── requirements.txt    # Dependencies
├── Procfile           # Railway deployment
├── core/              # Core engine
│   ├── database.py   # SQLite database
│   ├── discovery.py  # PDF search
│   ├── downloader.py # Download manager
│   └── renamer.py    # File renaming
├── templates/         # Jinja2 templates
├── static/           # CSS, fonts, images
└── utils/            # Utilities
```

## 🎨 Features

- **Pure Python**: No JavaScript frameworks
- **Server-Side Rendering**: Fast, simple
- **Retro Aesthetic**: 8-bit terminal style
- **Intelligent Discovery**: Multi-source PDF search
- **Auto-Renaming**: Consistent file naming
- **Queue Management**: Background downloads

## 🔧 Configuration

Edit `app.py` or set environment variables:

- `PDF_DIRECTORY`: PDF storage location
- `DATABASE_PATH`: Database file path
- `SECRET_KEY`: Flask session secret

## 📝 Usage

1. **Paste book list** in Discover page
2. **Wait for discovery** to complete
3. **Select PDFs** to download
4. **View library** with all your books

## 🐛 Troubleshooting

- **Database errors**: Ensure `data/` directory exists
- **Download fails**: Check PDF directory permissions
- **Search slow**: Rate limiting is intentional (respects sources)

## 📦 Dependencies

See `requirements.txt` for full list.

Main dependencies:
- Flask (web framework)
- ddgs (DuckDuckGo search)
- requests (HTTP)
- sqlite3 (database)

## 🎯 Roadmap

- [ ] Real-time progress updates (WebSockets)
- [ ] Book cover fetching
- [ ] Advanced filtering
- [ ] Export functionality
- [ ] Multi-user support

---

**Built with pure Python. No JavaScript. Retro aesthetic. Maximum fun.** 🏛️📚

