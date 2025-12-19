"""
Rename newly added PDFs using intelligent filename parsing and database matching
"""

import re
from pathlib import Path

try:
    from book_database_generated import BOOK_DATABASE
except ImportError:
    BOOK_DATABASE = {}


def normalize_for_search(text):
    """Normalize text for searching."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def sanitize_filename(filename):
    """Remove invalid characters for Windows filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    filename = filename.strip(' .')
    filename = re.sub(r'-+', '-', filename)
    return filename


def intelligent_parse_filename(filename):
    """Intelligently parse title and author from various filename patterns."""
    stem = Path(filename).stem
    
    # Pattern 1: "Title by Author" or "Title - Author"
    patterns = [
        (r'^(.+?)\s+by\s+(.+?)$', 'by'),
        (r'^(.+?)\s+[-—–]\s+(.+?)$', 'dash'),
        (r'^(.+?)\s+BY\s+(.+?)$', 'BY'),
    ]
    
    for pattern, sep_type in patterns:
        match = re.match(pattern, stem, re.IGNORECASE if 'by' in sep_type.lower() else 0)
        if match:
            title = match.group(1).strip()
            author = match.group(2).strip()
            # Clean up title (remove common suffixes)
            title = re.sub(r'\s*(PDF|pdf|ebook|e-book|edition|ed\.?)$', '', title, flags=re.IGNORECASE)
            # Heuristic: if title is much shorter than author, might be reversed
            if len(title.split()) < 2 and len(author.split()) > 2:
                title, author = author, title
            return title, author
    
    # Pattern 2: Handle underscore/hyphen separated titles
    # e.g., "The_33_Strategies_of_War" or "niccolo-machiavelli-discourses-of-livy"
    cleaned = stem.replace('_', ' ').replace('-', ' ').replace('+', ' ')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Check if it contains author name patterns
    # Look for "by Author" pattern
    match = re.search(r'\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', cleaned, re.IGNORECASE)
    if match:
        author_part = match.group(1)
        title_part = cleaned[:match.start()].strip()
        return title_part, author_part
    
    # Pattern 3: Look for known author names in filename
    known_authors = {
        'robert greene': 'Robert Greene',
        'robert coram': 'Robert Coram',
        'james carse': 'James P. Carse',
        'neil postman': 'Neil Postman',
        'eric hoffer': 'Eric Hoffer',
        'walter lippmann': 'Walter Lippmann',
        'eric berne': 'Eric Berne',
        'niccolo machiavelli': 'Niccolò Machiavelli',
        'machiavelli': 'Niccolò Machiavelli',
        'gracian': 'Baltasar Gracián',
        'donella meadows': 'Donella Meadows',
        'edward bernays': 'Edward Bernays',
        'gustave le bon': 'Gustave Le Bon',
    }
    
    stem_lower = stem.lower()
    for author_key, author_name in known_authors.items():
        if author_key in stem_lower:
            # Extract title by removing author and common words
            title_part = stem_lower.replace(author_key, '').replace('by', '').replace('pdf', '')
            title_part = re.sub(r'[_\-\+\.]', ' ', title_part)
            title_part = re.sub(r'\s+', ' ', title_part).strip()
            # Capitalize properly
            title_part = ' '.join(word.capitalize() for word in title_part.split())
            return title_part, author_name
    
    # Pattern 4: Handle specific known patterns
    specific_patterns = {
        r'meadows.*thinking.*systems': ('Thinking in Systems', 'Donella Meadows'),
        r'finite.*infinite.*games.*james.*carse': ('Finite and Infinite Games', 'James P. Carse'),
        r'amusing.*ourselves.*death.*postman': ('Amusing Ourselves to Death', 'Neil Postman'),
        r'dictators.*handbook': ("Dictator's Handbook", 'Bruce Bueno de Mesquita & Smith'),
        r'public.*opinion.*lippmann': ('Public Opinion', 'Walter Lippmann'),
        r'games.*people.*play': ('Games People Play', 'Eric Berne'),
        r'true.*believer.*hoffer': ('The True Believer', 'Eric Hoffer'),
        r'crowd.*study.*popular': ('The Crowd: A Study of the Popular Mind', 'Gustave Le Bon'),
        r'propaganda.*bernays': ('Propaganda', 'Edward Bernays'),
        r'gracian': ('The Art of Worldly Wisdom', 'Baltasar Gracián'),
        r'discourses.*livy.*machiavelli': ('Discourses on Livy', 'Niccolò Machiavelli'),
        r'mastery.*robert.*greene': ('Mastery', 'Robert Greene'),
        r'33.*strategies.*war': ('The 33 Strategies of War', 'Robert Greene'),
        r'art.*seduction.*robert.*greene': ('The Art of Seduction', 'Robert Greene'),
        r'48.*laws.*power': ('The 48 Laws of Power', 'Robert Greene'),
    }
    
    stem_norm = normalize_for_search(stem)
    for pattern, (title, author) in specific_patterns.items():
        if re.search(pattern, stem_norm):
            return title, author
    
    return None, None


def find_in_database(filename):
    """Try to find book in database."""
    stem_norm = normalize_for_search(Path(filename).stem)
    
    # Direct match
    if stem_norm in BOOK_DATABASE:
        return BOOK_DATABASE[stem_norm]
    
    # Substring match
    for key, book_info in BOOK_DATABASE.items():
        if key in stem_norm and len(key) > 3:
            return book_info
    
    # Word overlap
    stem_words = set(stem_norm.split())
    best_match = None
    best_score = 0
    
    for key, book_info in BOOK_DATABASE.items():
        title_norm = normalize_for_search(book_info['title'])
        author_norm = normalize_for_search(book_info['author'])
        
        title_words = set(title_norm.split())
        author_words = set(author_norm.split())
        
        title_overlap = len(title_words.intersection(stem_words))
        author_overlap = len(author_words.intersection(stem_words))
        
        score = title_overlap * 2 + author_overlap
        
        if score > best_score and (title_overlap >= 2 or author_overlap >= 1):
            best_match = book_info
            best_score = score
    
    return best_match


def rename_pdf(pdf_file, dry_run=False):
    """Rename PDF intelligently."""
    # Try database first
    db_match = find_in_database(pdf_file.name)
    
    if db_match:
        title = db_match['title']
        author = db_match['author']
        source = "database"
    else:
        # Parse filename intelligently
        title, author = intelligent_parse_filename(pdf_file.name)
        if not title or not author:
            return False
        source = "parsing"
    
    # Sanitize
    title = sanitize_filename(title)
    author = sanitize_filename(author)
    
    # Generate filename
    new_name = f"{title} - {author}.pdf"
    new_path = pdf_file.parent / new_name
    
    # Handle duplicates
    counter = 1
    original_new_path = new_path
    while new_path.exists() and new_path != pdf_file:
        stem = original_new_path.stem
        new_path = pdf_file.parent / f"{stem} ({counter}).pdf"
        counter += 1
    
    if new_path == pdf_file:
        return True
    
    if dry_run:
        print(f"Would rename: {pdf_file.name}")
        print(f"           -> {new_path.name} ({source})")
        print()
    else:
        pdf_file.rename(new_path)
        print(f"Renamed: {pdf_file.name} -> {new_path.name} ({source})")
    
    return True


def main():
    """Main function."""
    script_dir = Path(__file__).parent
    pdf_dir = script_dir / 'pdf'
    
    print("="*80)
    print("Intelligent Renamer for New PDFs")
    print("="*80)
    print(f"Database keys: {len(BOOK_DATABASE)}\n")
    
    # Get files that don't match the pattern
    pdf_files = [f for f in pdf_dir.glob("*.pdf") 
                 if not f.name.endswith('.crdownload') and 
                 not re.match(r'^[^-]+ - [^-]+( \(\d+\))?\.pdf$', f.name)]
    
    print(f"Found {len(pdf_files)} PDFs to process\n")
    
    renamed = 0
    not_matched = []
    
    for pdf_file in pdf_files:
        if rename_pdf(pdf_file, dry_run=False):
            renamed += 1
        else:
            not_matched.append(pdf_file.name)
    
    print("\n" + "="*80)
    print(f"Summary: {renamed}/{len(pdf_files)} PDFs renamed")
    print(f"Not matched: {len(not_matched)} PDFs")
    
    if not_matched:
        print(f"\nUnmatched PDFs:")
        for name in not_matched[:30]:
            print(f"  - {name}")
    
    print("="*80)


if __name__ == '__main__':
    main()


