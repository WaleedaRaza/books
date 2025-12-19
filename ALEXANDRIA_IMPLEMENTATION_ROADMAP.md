# Alexandria Library - Implementation Roadmap

## 🎯 Quick Start Guide

### Prerequisites
```bash
# Install PyQt6
pip install PyQt6 PyQt6-Qt6

# Or PySide6 (Qt official Python bindings - recommended)
pip install PySide6

# Core dependencies
pip install requests beautifulsoup4 ddgs aiohttp watchdog
```

### Project Setup
```bash
# Create project structure
mkdir -p alexandria_library/{core,models,ui/components,utils,data,tests}
cd alexandria_library

# Initialize
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

---

## 📋 Phase-by-Phase Implementation Checklist

### ✅ Phase 1: Foundation (Weeks 1-2)

#### Database & Models
- [ ] Create `core/database.py` with SQLite schema
- [ ] Implement `Book` dataclass in `models/book.py`
- [ ] Implement `PDFLink` dataclass
- [ ] Create database initialization function
- [ ] Write unit tests for database operations

#### Basic UI Shell
- [ ] Create `main.py` entry point
- [ ] Set up QML application structure
- [ ] Create `ui/main.qml` root file
- [ ] Create `ui/MainWindow.qml` with sidebar navigation
- [ ] Implement basic theme system (`ui/Theme.qml`)
- [ ] Add application icon and branding

#### Configuration System
- [ ] Create `config.json` template
- [ ] Implement config loader/saver
- [ ] Add PDF directory configuration
- [ ] Add database path configuration

**Deliverable**: Working app shell with database, can display empty library view

---

### ✅ Phase 2: Discovery Engine (Weeks 3-4)

#### PDF Discovery Core
- [ ] Create `core/discovery.py`
- [ ] Implement DuckDuckGo search integration
- [ ] Implement scoring algorithm
- [ ] Add link validation
- [ ] Implement rate limiting
- [ ] Add progress tracking

#### Discovery UI
- [ ] Create `ui/DiscoveryPanel.qml`
- [ ] Add book list input (text area)
- [ ] Implement book list parser (`utils/parsers.py`)
- [ ] Add search progress display
- [ ] Create results display component
- [ ] Add "Start Discovery" button and logic

#### Integration
- [ ] Connect discovery engine to UI
- [ ] Implement async search (non-blocking UI)
- [ ] Add error handling and display
- [ ] Test with sample book list

**Deliverable**: Can paste book list, search for PDFs, see results

---

### ✅ Phase 3: Download & Rename (Weeks 5-6)

#### Download Manager
- [ ] Create `core/downloader.py`
- [ ] Implement download queue system
- [ ] Add progress tracking
- [ ] Implement resume capability
- [ ] Add error handling and retries
- [ ] Integrate with file system

#### Download UI
- [ ] Create `ui/DownloadQueue.qml`
- [ ] Display active downloads
- [ ] Show progress bars
- [ ] Add pause/resume controls
- [ ] Display download errors

#### Renaming Integration
- [ ] Integrate existing `rename_pdfs_intelligent.py` logic
- [ ] Create `core/renamer.py` wrapper
- [ ] Implement auto-rename on download completion
- [ ] Add manual rename option in UI
- [ ] Update database when files renamed

**Deliverable**: Can download PDFs, auto-rename, track progress

---

### ✅ Phase 4: Library Features (Weeks 7-8)

#### Book Display
- [ ] Create `ui/BookListView.qml`
- [ ] Implement grid layout (masonry-style)
- [ ] Create `ui/BookCard.qml` component
- [ ] Add list view toggle
- [ ] Implement pagination or virtual scrolling

#### Book Details
- [ ] Create `ui/BookDetailView.qml`
- [ ] Display full book metadata
- [ ] Show PDF links and sources
- [ ] Add action buttons (open, download, rename)
- [ ] Implement cover image display

#### Search & Filter
- [ ] Add search bar component
- [ ] Implement full-text search
- [ ] Add filter by author, tag, status
- [ ] Implement sorting (title, author, date)
- [ ] Add tag management UI

#### Collections
- [ ] Implement book list creation
- [ ] Add book to list functionality
- [ ] Display lists in sidebar
- [ ] Add list management (create, edit, delete)

**Deliverable**: Beautiful library browsing with search, filter, and organization

---

### ✅ Phase 5: Polish & Refinement (Weeks 9-10)

#### UI Polish
- [ ] Refine Alexandria color palette
- [ ] Add smooth animations
- [ ] Improve typography
- [ ] Add loading states
- [ ] Improve error messages
- [ ] Add tooltips and help text

#### Settings Panel
- [ ] Create `ui/SettingsPanel.qml`
- [ ] Add PDF directory picker
- [ ] Add search preferences
- [ ] Add renaming rules configuration
- [ ] Add appearance settings (theme, view preferences)

#### Performance
- [ ] Optimize database queries
- [ ] Implement lazy loading for book cards
- [ ] Add caching for covers
- [ ] Optimize QML rendering

#### Error Handling
- [ ] Improve error messages
- [ ] Add retry mechanisms
- [ ] Implement graceful degradation
- [ ] Add logging system

**Deliverable**: Polished, production-ready application

---

### ✅ Phase 6: Advanced Features (Weeks 11+)

#### Auto-Scan
- [ ] Create `core/scanner.py`
- [ ] Implement file system watching
- [ ] Auto-detect new PDFs
- [ ] Auto-match and rename
- [ ] Background processing

#### Batch Operations
- [ ] Add bulk download
- [ ] Add bulk rename
- [ ] Add bulk tagging
- [ ] Add export functionality

#### Statistics
- [ ] Create statistics dashboard
- [ ] Show library stats (total books, by author, etc.)
- [ ] Show discovery success rate
- [ ] Show download statistics

#### Export
- [ ] Export to CSV
- [ ] Export to JSON
- [ ] Export to Markdown
- [ ] Generate bibliography

**Deliverable**: Feature-complete library management system

---

## 🛠️ Key Implementation Details

### QML Application Structure

```python
# main.py
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot

class BookManager(QObject):
    @Slot(str)
    def pasteBookList(self, text):
        # Parse and add books
        pass

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Register Python objects
    book_manager = BookManager()
    engine.rootContext().setContextProperty("bookManager", book_manager)
    
    # Load QML
    engine.load("ui/main.qml")
    
    sys.exit(app.exec())
```

### Database Initialization

```python
# core/database.py
import sqlite3
from pathlib import Path

class BookDatabase:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                ...
            )
        """)
        
        conn.commit()
        conn.close()
```

### Discovery Engine Integration

```python
# core/discovery.py
from ddgs import DDGS
import asyncio

class PDFDiscoveryEngine:
    def __init__(self):
        self.ddgs = DDGS()
        self.rate_limit_delay = 2.0
    
    async def discover_pdfs(self, book_title, book_author):
        query = f"{book_title} {book_author} free pdf"
        results = self.ddgs.text(query, max_results=10)
        
        # Score and filter
        scored_results = self.score_results(results, book_title, book_author)
        return scored_results[:5]  # Top 5
```

---

## 🎨 QML Component Examples

### Book Card Component

```qml
// ui/components/BookCard.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: card
    width: 200
    height: 300
    
    color: Theme.cream
    radius: 8
    border.color: Theme.deepBlue
    border.width: 1
    
    Column {
        anchors.fill: parent
        anchors.margins: 12
        
        // Cover image placeholder
        Rectangle {
            width: parent.width - 24
            height: 200
            color: Theme.parchment
            radius: 4
            
            Text {
                anchors.centerIn: parent
                text: "📖"
                font.pixelSize: 48
            }
        }
        
        // Title
        Text {
            width: parent.width - 24
            text: bookTitle
            font.family: Theme.titleFont
            font.pixelSize: 14
            font.bold: true
            wrapMode: Text.Wrap
            color: Theme.darkText
        }
        
        // Author
        Text {
            width: parent.width - 24
            text: bookAuthor
            font.family: Theme.bodyFont
            font.pixelSize: 12
            color: Theme.lightText
            wrapMode: Text.Wrap
        }
        
        // Status badge
        Rectangle {
            width: 60
            height: 20
            color: status === "READY" ? "#4CAF50" : "#FFC107"
            radius: 10
            
            Text {
                anchors.centerIn: parent
                text: status
                font.pixelSize: 10
                color: "white"
            }
        }
    }
    
    MouseArea {
        anchors.fill: parent
        onClicked: {
            // Open book detail view
            bookManager.openBookDetail(bookId)
        }
    }
}
```

### Main Window Layout

```qml
// ui/MainWindow.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: window
    width: 1200
    height: 800
    visible: true
    title: "Alexandria Library"
    
    // Sidebar
    Rectangle {
        id: sidebar
        width: 200
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: Theme.deepBlue
        
        Column {
            anchors.fill: parent
            anchors.margins: 16
            
            Text {
                text: "📚 Alexandria"
                font.pixelSize: 24
                color: Theme.gold
                font.bold: true
            }
            
            Button {
                text: "📚 Library"
                width: parent.width
            }
            
            Button {
                text: "🔍 Discover"
                width: parent.width
            }
            
            Button {
                text: "⬇️ Downloads"
                width: parent.width
            }
            
            Button {
                text: "⚙️ Settings"
                width: parent.width
            }
        }
    }
    
    // Main content area
    StackView {
        id: contentStack
        anchors.left: sidebar.right
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        
        initialItem: BookListView {}
    }
}
```

---

## 🧪 Testing Strategy

### Unit Tests Structure

```python
# tests/test_database.py
import unittest
from core.database import BookDatabase

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = BookDatabase(":memory:")
    
    def test_add_book(self):
        book_id = self.db.add_book("Test Book", "Test Author")
        self.assertIsNotNone(book_id)
    
    def test_find_book(self):
        # Test search functionality
        pass
```

### Integration Tests

```python
# tests/test_pipeline.py
import unittest
from core.discovery import PDFDiscoveryEngine
from core.downloader import DownloadManager

class TestPipeline(unittest.TestCase):
    def test_end_to_end(self):
        # Test: Paste list → Discover → Download → Rename
        pass
```

---

## 📦 Dependencies

### requirements.txt

```
# UI Framework
PySide6>=6.6.0

# Core Libraries
requests>=2.31.0
beautifulsoup4>=4.12.0
ddgs>=0.1.0

# Async & Concurrency
aiohttp>=3.9.0
asyncio

# File Operations
watchdog>=3.0.0
pathlib

# PDF Processing
PyPDF2>=3.0.0
pdfplumber>=0.10.0
Pillow>=10.0.0

# Database
sqlite3  # Built-in

# Utilities
python-dateutil>=2.8.0
```

---

## 🚀 Getting Started

1. **Review Design**: Read `ALEXANDRIA_LIBRARY_DESIGN.md`
2. **Set Up Environment**: Install dependencies
3. **Create Project Structure**: Set up folders
4. **Start Phase 1**: Build foundation (database + basic UI)
5. **Iterate**: Build incrementally, test frequently

---

## 📝 Notes

- **QML vs Python**: QML for UI, Python for logic
- **Async Operations**: Use asyncio for non-blocking operations
- **Database**: SQLite for simplicity (can upgrade to PostgreSQL later if needed)
- **File Watching**: Use watchdog for auto-scanning
- **Error Handling**: Robust error handling at every layer

---

**Let's build this! 🏛️📚**


