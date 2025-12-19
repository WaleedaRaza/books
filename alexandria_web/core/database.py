"""
Book Database Manager
SQLite database for storing books, PDF links, and metadata
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class BookDatabase:
    """Manages book database operations"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                year INTEGER,
                cover_path TEXT,
                pdf_path TEXT,
                status TEXT NOT NULL DEFAULT 'SEARCHING',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # PDF Links table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pdf_links (
                id TEXT PRIMARY KEY,
                book_id TEXT NOT NULL,
                url TEXT NOT NULL,
                source TEXT,
                confidence REAL,
                score REAL,
                verified BOOLEAN DEFAULT 0,
                broken BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)
        
        # Tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        """)
        
        # Book-Tag junction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_tags (
                book_id TEXT,
                tag_id TEXT,
                PRIMARY KEY (book_id, tag_id),
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        """)
        
        # Book Lists table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_lists (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Book-List junction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_list_items (
                list_id TEXT,
                book_id TEXT,
                order_index INTEGER,
                PRIMARY KEY (list_id, book_id),
                FOREIGN KEY (list_id) REFERENCES book_lists(id) ON DELETE CASCADE,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_book(self, title: str, author: str, isbn: Optional[str] = None, 
                 year: Optional[int] = None, status: str = 'SEARCHING') -> str:
        """Add a book to the database"""
        book_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO books (id, title, author, isbn, year, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (book_id, title, author, isbn, year, status))
        
        conn.commit()
        conn.close()
        return book_id
    
    def get_book(self, book_id: str) -> Optional[Dict]:
        """Get a book by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def search_books(self, query: str) -> List[Dict]:
        """Quick search by title"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f"%{query}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_all_books(self, search: str = '', filter_status: str = '', 
                     sort_by: str = 'title') -> List[Dict]:
        """Get all books with optional search and filter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM books WHERE 1=1"
        params = []
        
        if search:
            query += " AND (title LIKE ? OR author LIKE ?)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        if filter_status:
            query += " AND status = ?"
            params.append(filter_status.upper())
        
        # Sorting
        valid_sorts = {'title', 'author', 'created_at', 'updated_at'}
        if sort_by in valid_sorts:
            query += f" ORDER BY {sort_by} ASC"
        else:
            query += " ORDER BY title ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_book(self, book_id: str, **kwargs):
        """Update book fields"""
        if not kwargs:
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build update query
        updates = []
        params = []
        for key, value in kwargs.items():
            if key in ['title', 'author', 'isbn', 'year', 'cover_path', 'pdf_path', 'status']:
                updates.append(f"{key} = ?")
                params.append(value)
        
        if updates:
            params.append(book_id)
            query = f"UPDATE books SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def add_pdf_link(self, book_id: str, url: str, source: str = '', 
                     confidence: float = 0.0, score: float = 0.0) -> str:
        """Add a PDF link for a book"""
        link_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO pdf_links (id, book_id, url, source, confidence, score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (link_id, book_id, url, source, confidence, score))
        
        conn.commit()
        conn.close()
        return link_id
    
    def get_pdf_links(self, book_id: str) -> List[Dict]:
        """Get all PDF links for a book"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM pdf_links 
            WHERE book_id = ? AND broken = 0
            ORDER BY score DESC, confidence DESC
        """, (book_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict:
        """Get library statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM books")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as ready FROM books WHERE status = 'READY'")
        ready = cursor.fetchone()['ready']
        
        cursor.execute("SELECT COUNT(*) as downloading FROM books WHERE status = 'DOWNLOADING'")
        downloading = cursor.fetchone()['downloading']
        
        cursor.execute("SELECT COUNT(*) as searching FROM books WHERE status = 'SEARCHING'")
        searching = cursor.fetchone()['searching']
        
        cursor.execute("SELECT COUNT(*) as not_found FROM books WHERE status = 'NOT_FOUND'")
        not_found = cursor.fetchone()['not_found']
        
        conn.close()
        
        return {
            'total': total,
            'ready': ready,
            'downloading': downloading,
            'searching': searching,
            'not_found': not_found
        }

