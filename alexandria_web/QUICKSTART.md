# Alexandria Library - Quick Start Guide

## ✅ What's Built

**Complete Flask web application** with:
- ✅ Database system (SQLite)
- ✅ PDF discovery engine (DuckDuckGo integration)
- ✅ Download manager with queue
- ✅ Intelligent renaming system
- ✅ Retro 8-bit terminal UI
- ✅ All templates and styling
- ✅ Ready for Railway/Render deployment

## 🚀 Local Testing

```bash
# Install dependencies
cd h:\Books\alexandria_web
pip install -r requirements.txt

# Run the app
python app.py

# Visit http://localhost:5000
```

## 🌐 Deploy to Railway (Recommended)

1. **Push to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Go to Railway.app** → New Project → Deploy from GitHub

3. **Select your repo** → Railway auto-detects Python

4. **Add environment variables** (optional):
   - `PDF_DIRECTORY`: `/app/pdf` (or leave default)
   - `DATABASE_PATH`: `/app/data/books.db` (or leave default)
   - `SECRET_KEY`: Generate a random string

5. **Deploy!** Railway handles everything

6. **Share URL** with friends 🎉

## 🎨 Features

### Library View
- Browse all books in grid layout
- Search and filter
- Sort by title/author/date
- Status indicators (READY, DOWNLOADING, SEARCHING)

### Discovery Panel
- Paste book list (any format)
- Automatic PDF search
- Progress tracking
- Results display with scoring

### Download Queue
- Queue management
- Progress bars
- Auto-refresh
- Error handling

### Book Details
- Full metadata
- PDF links with sources
- Confidence scores
- Direct PDF access

## 🎯 Next Steps

1. **Test locally** first
2. **Deploy to Railway**
3. **Share with friends**
4. **Iterate based on feedback**

## 🐛 Troubleshooting

**Import errors**: Install dependencies with `pip install -r requirements.txt`

**Database errors**: Ensure `data/` directory exists (auto-created)

**Download fails**: Check PDF directory permissions

**Search slow**: Intentional rate limiting (respects sources)

## 📝 Notes

- **No JavaScript**: Pure Python + server-side rendering
- **Retro aesthetic**: 8-bit terminal style throughout
- **Auto-refresh**: Progress pages refresh automatically
- **Background processing**: Discovery/downloads run in threads

---

**Ready to deploy!** 🚀

