# Alexandria Library - Complete Design & Architecture Plan

## 🎯 Vision Statement

A **Python-native desktop application** that provides a seamless, beautiful end-to-end pipeline for managing a personal digital library. From pasting book lists to intelligent PDF discovery, automatic downloading, smart renaming, and elegant library browsing - all in one cohesive, modern interface inspired by the Alexandria Library aesthetic.

**Core Principle**: Zero JavaScript. Pure Python desktop application with native performance and beautiful UI.

---

## 🏛️ Alexandria UI Aesthetic

### Design Philosophy
- **Classical Elegance**: Inspired by the Great Library of Alexandria - knowledge, beauty, order
- **Modern Minimalism**: Clean lines, generous whitespace, typography-focused
- **Card-Based Layout**: Books as beautiful cards with rich metadata
- **Warm Color Palette**: Creams, deep blues, gold accents, parchment tones
- **Smooth Animations**: Subtle transitions, not jarring
- **Information Hierarchy**: Clear visual organization of knowledge

### Visual Elements
- **Typography**: Serif for book titles (classical), sans-serif for UI (modern)
- **Icons**: Minimalist, line-based icons
- **Spacing**: Generous padding, breathing room
- **Shadows**: Soft, subtle depth
- **Grid Layout**: Masonry-style book grid (like a real library shelf)

---

## 🏗️ Technical Architecture

### Tech Stack (Python-Native)

#### UI Framework: **PyQt6 / PySide6**
- **Why**: Most mature, powerful, native desktop framework
- **QML for Modern UI**: Use QML for declarative, modern UI design
- **Python Backend**: All logic in Python, QML for presentation
- **Native Performance**: True desktop app, no browser overhead
- **Cross-Platform**: Windows, macOS, Linux

#### Alternative Consideration: **Flet**
- Modern Flutter-like syntax
- BUT: Compiles to web tech (violates "no JS" requirement)
- **Decision**: PyQt6 chosen for true native experience

#### Core Libraries
```python
# UI & Framework
PyQt6 / PySide6          # Main UI framework
QML                      # Modern declarative UI

# PDF & Document Processing
PyPDF2 / pdfplumber      # PDF text extraction
Pillow                   # Image processing (covers, thumbnails)

# Search & Web
ddgs                     # DuckDuckGo search
requests                 # HTTP requests
beautifulsoup4          # HTML parsing

# Data & Storage
SQLite                   # Local database (books, metadata, state)
JSON                     # Configuration, lists
pathlib                  # File system operations

# Async & Concurrency
asyncio                  # Async operations
aiohttp                  # Async HTTP
concurrent.futures       # Parallel processing

# Utilities
watchdog                 # File system monitoring (auto-detect new PDFs)
keyring                  # Secure credential storage (if needed)
```

---

## 📐 Application Architecture

### High-Level Structure

```
Alexandria Library Application
├── Core Engine (Backend)
│   ├── Book Database Manager
│   ├── PDF Discovery Engine
│   ├── Download Manager
│   ├── Renaming Engine
│   └── Library Scanner
│
├── UI Layer (Frontend)
│   ├── Main Window (QML)
│   ├── Book List View
│   ├── Book Detail View
│   ├── Search & Discovery Panel
│   ├── Download Queue
│   └── Settings Panel
│
└── Data Layer
    ├── SQLite Database (books.db)
    ├── Configuration (config.json)
    ├── Book Lists (lists/)
    └── PDF Storage (pdf/)
```

### Component Breakdown

#### 1. **Core Engine** (`core/`)

**Book Database Manager** (`core/database.py`)
- SQLite database schema
- CRUD operations for books
- Metadata storage (title, author, ISBN, cover, etc.)
- Tagging and categorization
- Search and filtering

**PDF Discovery Engine** (`core/discovery.py`)
- Multi-source search (DuckDuckGo, Archive.org, etc.)
- Intelligent scoring system
- Link validation
- Rate limiting and retry logic
- Progress tracking

**Download Manager** (`core/downloader.py`)
- Queue-based downloading
- Resume capability
- Progress tracking
- Error handling and retries
- Automatic organization

**Renaming Engine** (`core/renamer.py`)
- Intelligent title/author extraction
- Database matching
- Consistent formatting
- Duplicate handling

**Library Scanner** (`core/scanner.py`)
- Watch PDF directory for new files
- Auto-import and match
- Background processing

#### 2. **UI Layer** (`ui/`)

**Main Window** (`ui/main_window.py` + `ui/main.qml`)
- Application shell
- Navigation sidebar
- Status bar
- Menu bar

**Book List View** (`ui/book_list.qml`)
- Grid/masonry layout
- Book cards with covers
- Filtering and sorting
- Search bar

**Book Detail View** (`ui/book_detail.qml`)
- Full book information
- PDF links and sources
- Metadata display
- Actions (open, download, rename)

**Search & Discovery Panel** (`ui/discovery_panel.qml`)
- Book list input (paste/import)
- Search progress
- Results display
- Batch operations

**Download Queue** (`ui/download_queue.qml`)
- Active downloads
- Progress bars
- Pause/resume
- Error handling

**Settings Panel** (`ui/settings.qml`)
- PDF directory configuration
- Search preferences
- Renaming rules
- Appearance settings

#### 3. **Data Models** (`models/`)

```python
# models/book.py
@dataclass
class Book:
    id: str
    title: str
    author: str
    isbn: Optional[str]
    year: Optional[int]
    cover_path: Optional[str]
    pdf_path: Optional[str]
    pdf_links: List[PDFLink]
    tags: List[str]
    status: BookStatus  # FOUND, SEARCHING, NOT_FOUND, DOWNLOADING, READY
    created_at: datetime
    updated_at: datetime

@dataclass
class PDFLink:
    url: str
    source: str  # archive.org, libgen, direct, etc.
    confidence: float
    score: float
    verified: bool
    broken: bool

@dataclass
class BookList:
    id: str
    name: str
    books: List[Book]
    created_at: datetime
```

---

## 🔄 End-to-End Pipeline

### Flow 1: Paste Book List → Discovery → Download → Rename

```
1. USER INPUT
   └─> Paste book list (text, markdown, CSV)
       └─> Parse into Book objects
           └─> Store in database

2. DISCOVERY PHASE
   └─> For each book:
       ├─> Generate search queries
       ├─> Search DuckDuckGo (with rate limiting)
       ├─> Score and filter results
       ├─> Validate PDF links
       └─> Store top 3-5 PDF links per book
       
3. USER REVIEW (Optional)
   └─> Display results in UI
       └─> User can:
           ├─> Select preferred PDF per book
           ├─> Mark links as broken
           └─> Start download

4. DOWNLOAD PHASE
   └─> Queue selected PDFs
       └─> Download with progress tracking
           └─> Save to pdf/ directory
               └─> Trigger auto-rename

5. RENAMING PHASE
   └─> Watch for new PDFs
       └─> Extract title/author from filename or PDF metadata
           └─> Match against database
               └─> Rename to "Title - Author.pdf"
                   └─> Update database

6. LIBRARY UPDATE
   └─> Refresh UI
       └─> Display newly added books
```

### Flow 2: Auto-Scan Existing PDFs

```
1. SCAN DIRECTORY
   └─> Watch pdf/ directory
       └─> Detect new/changed files
           └─> Extract metadata
               └─> Match against database
                   └─> If match: Update record
                   └─> If no match: Create new book entry
```

---

## 🎨 UI/UX Design Details

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Alexandria Library                    [🔍] [⚙️] [👤]        │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│  📚      │  ┌──────────────────────────────────────────┐   │
│ Library  │  │  Search your library...                  │   │
│          │  └──────────────────────────────────────────┘   │
│  🔍      │                                                  │
│ Discover │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│          │  │ 📖   │ │ 📖   │ │ 📖   │ │ 📖   │          │
│  ⬇️      │  │Title │ │Title │ │Title │ │Title │          │
│ Downloads│  │Author│ │Author│ │Author│ │Author│          │
│          │  └──────┘ └──────┘ └──────┘ └──────┘          │
│  ⚙️      │                                                  │
│ Settings │  [Grid View] [List View] [Sort: Title ▼]       │
│          │                                                  │
│          │  Showing 142 books                              │
└──────────┴──────────────────────────────────────────────────┘
```

### Book Card Design

```
┌─────────────────────┐
│   [Book Cover]      │  ← If available, else placeholder icon
│                     │
│                     │
└─────────────────────┘
      Title Name
      Author Name
      
      [📄 PDF] [⭐] [🏷️]
      
      Status: ✅ Ready
```

### Discovery Panel

```
┌─────────────────────────────────────────────────┐
│ Discover Books                                  │
├─────────────────────────────────────────────────┤
│                                                 │
│ Paste your book list:                           │
│ ┌─────────────────────────────────────────────┐ │
│ │ The 48 Laws of Power - Robert Greene       │ │
│ │ Meditations - Marcus Aurelius              │ │
│ │ ...                                         │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ [📋 Import from File] [🔍 Start Discovery]     │
│                                                 │
│ Progress: ████████░░ 8/10 books                │
│                                                 │
│ Results:                                        │
│ ┌─────────────────────────────────────────────┐ │
│ │ ✅ The 48 Laws of Power                    │ │
│ │    3 PDFs found                            │ │
│ │    [View] [Download Best]                  │ │
│ └─────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────┐ │
│ │ ⏳ Meditations - Searching...              │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### SQLite Tables

```sql
-- Books table
CREATE TABLE books (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT,
    year INTEGER,
    cover_path TEXT,
    pdf_path TEXT,
    status TEXT NOT NULL,  -- SEARCHING, FOUND, DOWNLOADING, READY, NOT_FOUND
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PDF Links table
CREATE TABLE pdf_links (
    id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL,
    url TEXT NOT NULL,
    source TEXT,  -- archive.org, libgen, direct, etc.
    confidence REAL,
    score REAL,
    verified BOOLEAN DEFAULT 0,
    broken BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Tags table
CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Book-Tag junction table
CREATE TABLE book_tags (
    book_id TEXT,
    tag_id TEXT,
    PRIMARY KEY (book_id, tag_id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

-- Book Lists table
CREATE TABLE book_lists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book-List junction table
CREATE TABLE book_list_items (
    list_id TEXT,
    book_id TEXT,
    order_index INTEGER,
    PRIMARY KEY (list_id, book_id),
    FOREIGN KEY (list_id) REFERENCES book_lists(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Search History table
CREATE TABLE search_history (
    id TEXT PRIMARY KEY,
    book_id TEXT,
    query TEXT,
    results_count INTEGER,
    success BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id)
);
```

---

## 🔧 Key Features & Functionality

### 1. Book List Import
- **Paste Text**: Multi-line text parsing
- **File Import**: CSV, TXT, Markdown, JSON
- **Smart Parsing**: Handle various formats
  - "Title - Author"
  - "Title by Author"
  - "Title — Author" (em dash)
  - Markdown lists
  - CSV columns

### 2. Intelligent PDF Discovery
- **Multi-Source Search**:
  - DuckDuckGo (primary)
  - Archive.org API
  - LibGen (if available)
  - Google Books (metadata)
- **Scoring System**:
  - Direct PDF links: +50
  - Archive.org/LibGen: +30
  - Title match: +20
  - Author match: +15
  - Paywall/broken: -100
- **Validation**:
  - Check URL accessibility
  - Verify PDF format
  - Size estimation

### 3. Download Management
- **Queue System**: Prioritized download queue
- **Progress Tracking**: Real-time progress bars
- **Resume Capability**: Handle interruptions
- **Rate Limiting**: Respect source limits
- **Error Handling**: Retry logic, error reporting

### 4. Smart Renaming
- **Database Matching**: Match against known books
- **PDF Metadata Extraction**: Read title/author from PDF
- **Filename Parsing**: Intelligent pattern recognition
- **Consistent Format**: "Title - Author.pdf"
- **Duplicate Handling**: Numbered suffixes

### 5. Library Management
- **Grid/List Views**: Toggle between views
- **Search & Filter**: Full-text search, filters by author, tag, status
- **Sorting**: Title, author, date added, year
- **Tagging**: Custom tags for organization
- **Collections**: Create custom book lists

### 6. Book Details
- **Metadata Display**: Full book information
- **Cover Images**: Display book covers (if available)
- **PDF Links**: List all found PDF sources
- **Actions**: Open PDF, download, rename, tag, delete

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal**: Basic application structure and core engine

- [ ] Set up PyQt6 project structure
- [ ] Create database schema and models
- [ ] Implement Book Database Manager
- [ ] Basic QML main window
- [ ] Simple book list view
- [ ] Configuration system

### Phase 2: Discovery Engine (Week 3-4)
**Goal**: PDF discovery functionality

- [ ] Implement PDF Discovery Engine
- [ ] DuckDuckGo integration
- [ ] Scoring system
- [ ] Link validation
- [ ] Discovery UI panel
- [ ] Progress tracking

### Phase 3: Download & Rename (Week 5-6)
**Goal**: Complete download and renaming pipeline

- [ ] Download Manager implementation
- [ ] Queue system
- [ ] Progress tracking UI
- [ ] Renaming Engine integration
- [ ] Auto-rename on download
- [ ] Error handling

### Phase 4: Library Features (Week 7-8)
**Goal**: Rich library management

- [ ] Book detail view
- [ ] Search and filtering
- [ ] Tagging system
- [ ] Collections/lists
- [ ] Cover image handling
- [ ] Grid/List view toggle

### Phase 5: Polish & Refinement (Week 9-10)
**Goal**: UI polish and robustness

- [ ] Alexandria UI styling
- [ ] Animations and transitions
- [ ] Error handling improvements
- [ ] Performance optimization
- [ ] Settings panel
- [ ] Documentation

### Phase 6: Advanced Features (Week 11+)
**Goal**: Enhanced functionality

- [ ] Auto-scan existing PDFs
- [ ] Batch operations
- [ ] Export functionality
- [ ] Statistics dashboard
- [ ] Backup/restore
- [ ] Advanced search

---

## 🎨 QML UI Structure

### Main QML Files

```
ui/
├── main.qml                 # Root application window
├── MainWindow.qml           # Main window shell
├── BookListView.qml         # Grid/list view of books
├── BookCard.qml             # Individual book card component
├── BookDetailView.qml       # Detailed book information
├── DiscoveryPanel.qml       # PDF discovery interface
├── DownloadQueue.qml        # Download management
├── SettingsPanel.qml        # Application settings
└── components/
    ├── SearchBar.qml        # Reusable search component
    ├── ProgressBar.qml      # Custom progress indicator
    └── TagChip.qml          # Tag display component
```

### QML Theme/Styling

```qml
// Theme.qml - Alexandria color palette
pragma Singleton

QtObject {
    // Colors
    readonly property color parchment: "#F5F1E8"
    readonly property color deepBlue: "#1A3A52"
    readonly property color gold: "#D4AF37"
    readonly property color cream: "#FAF8F3"
    readonly property color darkText: "#2C2C2C"
    readonly property color lightText: "#6B6B6B"
    
    // Typography
    readonly property string titleFont: "Georgia, serif"
    readonly property string bodyFont: "Segoe UI, sans-serif"
    
    // Spacing
    readonly property int spacingSmall: 8
    readonly property int spacingMedium: 16
    readonly property int spacingLarge: 24
}
```

---

## 🔐 Configuration & Data

### Configuration File (`config.json`)

```json
{
    "pdf_directory": "h:/Books/pdf",
    "database_path": "h:/Books/alexandria_library/books.db",
    "search": {
        "max_results_per_book": 5,
        "rate_limit_delay": 2.0,
        "extended_delay_interval": 5
    },
    "download": {
        "max_concurrent": 3,
        "retry_attempts": 3,
        "timeout_seconds": 30
    },
    "renaming": {
        "auto_rename": true,
        "format": "{title} - {author}.pdf",
        "handle_duplicates": true
    },
    "ui": {
        "theme": "alexandria",
        "default_view": "grid",
        "books_per_page": 50
    }
}
```

---

## 🧪 Testing Strategy

### Unit Tests
- Database operations
- PDF discovery logic
- Renaming algorithms
- Parsing functions

### Integration Tests
- End-to-end pipeline
- UI interactions
- File system operations

### Manual Testing
- UI/UX validation
- Cross-platform compatibility
- Performance testing

---

## 📦 Project Structure

```
alexandria_library/
├── main.py                  # Application entry point
├── config.json              # Configuration
├── requirements.txt         # Python dependencies
│
├── core/                    # Core engine
│   ├── __init__.py
│   ├── database.py          # Database manager
│   ├── discovery.py         # PDF discovery engine
│   ├── downloader.py        # Download manager
│   ├── renamer.py           # Renaming engine
│   └── scanner.py           # Library scanner
│
├── models/                  # Data models
│   ├── __init__.py
│   ├── book.py              # Book model
│   └── pdf_link.py          # PDF link model
│
├── ui/                      # UI layer
│   ├── main.qml             # Root QML
│   ├── MainWindow.qml
│   ├── BookListView.qml
│   ├── BookDetailView.qml
│   ├── DiscoveryPanel.qml
│   ├── DownloadQueue.qml
│   ├── SettingsPanel.qml
│   └── components/          # Reusable components
│
├── utils/                   # Utilities
│   ├── __init__.py
│   ├── parsers.py           # Book list parsers
│   ├── validators.py        # URL/file validators
│   └── helpers.py           # Helper functions
│
├── data/                    # Data storage
│   ├── books.db             # SQLite database
│   └── lists/               # Book lists
│
└── tests/                   # Tests
    ├── test_database.py
    ├── test_discovery.py
    └── test_renamer.py
```

---

## 🎯 Success Criteria

### Functional Requirements
- ✅ Paste book list → automatic PDF discovery
- ✅ Intelligent PDF link scoring and validation
- ✅ Queue-based downloading with progress
- ✅ Automatic intelligent renaming
- ✅ Beautiful library browsing interface
- ✅ Search, filter, and organize books

### Non-Functional Requirements
- ✅ Native desktop performance (no browser overhead)
- ✅ Responsive UI (60fps animations)
- ✅ Robust error handling
- ✅ Cross-platform compatibility
- ✅ Offline capability (works without internet for library browsing)

### User Experience
- ✅ Intuitive workflow
- ✅ Beautiful, Alexandria-inspired design
- ✅ Smooth animations and transitions
- ✅ Clear feedback and status updates
- ✅ Minimal configuration required

---

## 💡 Future Enhancements (Post-MVP)

1. **AI-Powered Features**
   - Book recommendations based on library
   - Smart categorization
   - Reading progress tracking

2. **Advanced Export**
   - Export to Kindle format
   - Generate reading lists
   - Bibliography generation

3. **Cloud Sync** (Optional)
   - Sync library across devices
   - Backup to cloud storage

4. **Community Features** (Optional)
   - Share book lists
   - Community-verified PDF links

5. **Mobile Companion** (Future)
   - View library on mobile
   - Reading progress sync

---

## 🚦 Next Steps

1. **Review & Approve**: Review this design document
2. **Set Up Project**: Initialize PyQt6 project structure
3. **Build Foundation**: Start with Phase 1 (Database + Basic UI)
4. **Iterate**: Build incrementally, test frequently
5. **Refine**: Polish UI and UX based on usage

---

## 📝 Notes

- **No JavaScript**: Pure Python + QML (QML is declarative, not JS)
- **Native Performance**: True desktop app, no browser
- **Alexandria Aesthetic**: Classical elegance meets modern minimalism
- **Robust Pipeline**: Error handling at every step
- **Extensible**: Easy to add new features

---

**Ready to build something beautiful and powerful! 🏛️📚**
