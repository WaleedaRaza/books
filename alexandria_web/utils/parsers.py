"""
Book List Parsers
Parse various book list formats into structured data
"""

import re
from typing import List, Dict


def parse_book_list(text: str) -> List[Dict]:
    """Parse book list from text into structured format"""
    books = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Try different patterns
        book_data = None
        
        # Pattern 1: "Title - Author" or "Title — Author"
        match = re.match(r'^(.+?)\s+[-—–]\s+(.+?)$', line)
        if match:
            book_data = {
                'title': match.group(1).strip(),
                'author': match.group(2).strip()
            }
        
        # Pattern 2: "Title by Author"
        if not book_data:
            match = re.match(r'^(.+?)\s+by\s+(.+?)$', line, re.IGNORECASE)
            if match:
                book_data = {
                    'title': match.group(1).strip(),
                    'author': match.group(2).strip()
                }
        
        # Pattern 3: Markdown list format "- Title — Author"
        if not book_data:
            match = re.match(r'^-\s*(.+?)\s+[-—–]\s+(.+?)$', line)
            if match:
                book_data = {
                    'title': match.group(1).strip(),
                    'author': match.group(2).strip()
                }
        
        # Pattern 4: Numbered format "001. Title — Author"
        if not book_data:
            match = re.match(r'^\d+\.\s*(.+?)\s+[-—–]\s+(.+?)$', line)
            if match:
                book_data = {
                    'title': match.group(1).strip(),
                    'author': match.group(2).strip()
                }
        
        if book_data and book_data['title'] and book_data['author']:
            books.append(book_data)
    
    return books

