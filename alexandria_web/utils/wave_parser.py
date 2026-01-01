"""
Parser for Ranked_Library_Waves.md format
Format: NUMBER. (WAVE) Title — Author
Example: 0001. (W1) The 48 Laws of Power — Robert Greene
"""

import re
from typing import List, Dict, Optional


def parse_wave_list(text: str) -> List[Dict]:
    """Parse ranked wave list into structured format"""
    books = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, headers, footers
        if not line or line.startswith('#') or line.startswith('---') or line.startswith('Legend'):
            continue
        
        # Pattern: NUMBER. (WAVE) Title — Author
        # Also handles: NUMBER. ✅ (WAVE) Title — Author
        match = re.match(r'^(\d+)\.\s*(?:✅\s*)?\(([W\d]+)\)\s*(.+?)\s+[-—–]\s+(.+?)$', line)
        
        if match:
            number = int(match.group(1))
            wave = match.group(2)  # W1, W2, W3, W4
            title = match.group(3).strip()
            author = match.group(4).strip()
            
            books.append({
                'number': number,
                'wave': wave,
                'title': title,
                'author': author,
                'original_line': line
            })
    
    return books


def group_by_wave(books: List[Dict]) -> Dict[str, List[Dict]]:
    """Group books by wave"""
    waves = {}
    for book in books:
        wave = book['wave']
        if wave not in waves:
            waves[wave] = []
        waves[wave].append(book)
    
    # Sort each wave by number
    for wave in waves:
        waves[wave].sort(key=lambda x: x['number'])
    
    return waves


def filter_books(books: List[Dict], wave_filters: Dict[str, int]) -> List[Dict]:
    """
    Filter books by wave and count
    wave_filters: {'W1': 10, 'W2': 5} means "10 from W1, 5 from W2"
    """
    filtered = []
    waves = group_by_wave(books)
    
    for wave, count in wave_filters.items():
        if wave in waves:
            filtered.extend(waves[wave][:count])
    
    # Sort by original number
    filtered.sort(key=lambda x: x['number'])
    return filtered








