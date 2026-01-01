"""
Book Database Knowledge Base - Integrated from book_database_generated.py
This is the PROVEN database for intelligent book matching and renaming.
"""

import sys
from pathlib import Path

# Import the generated database
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from book_database_generated import BOOK_DATABASE as GENERATED_DB
except ImportError:
    GENERATED_DB = {}

try:
    from rename_pdfs_intelligent import BOOK_DATABASE as RENAMER_DB
except ImportError:
    RENAMER_DB = {}

try:
    from smart_book_matcher import BOOK_KNOWLEDGE
except ImportError:
    BOOK_KNOWLEDGE = {}


# Merge all databases
BOOK_DATABASE = {}
BOOK_DATABASE.update(GENERATED_DB)
BOOK_DATABASE.update(RENAMER_DB)


def normalize_for_lookup(text):
    """Normalize text for database lookup."""
    if not text:
        return ""
    
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def lookup_book(title_fragment):
    """Look up a book in the database by title fragment."""
    normalized = normalize_for_lookup(title_fragment)
    
    # Direct match
    if normalized in BOOK_DATABASE:
        return BOOK_DATABASE[normalized]
    
    # Partial match
    for key, value in BOOK_DATABASE.items():
        if normalized in key or key in normalized:
            return value
    
    return None


def get_canonical_title(filename):
    """Get canonical title and author from a filename."""
    # Remove .pdf extension
    if filename.lower().endswith('.pdf'):
        filename = filename[:-4]
    
    normalized = normalize_for_lookup(filename)
    
    # Try progressively shorter fragments
    words = normalized.split()
    for length in range(len(words), 0, -1):
        fragment = ' '.join(words[:length])
        result = lookup_book(fragment)
        if result:
            return result
    
    return None


def get_all_books():
    """Get all books in the database."""
    unique_books = {}
    for key, value in BOOK_DATABASE.items():
        title = value['title']
        if title not in unique_books:
            unique_books[title] = value
    return list(unique_books.values())


def get_book_count():
    """Get count of unique books in the database."""
    return len(get_all_books())








