"""
Enhanced PDF Renamer with Text Extraction
Uses intelligence first, then extracts text from PDF when needed to identify books.
"""

import re
from pathlib import Path
from difflib import SequenceMatcher

# Try to import PDF extraction libraries
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

# Try to import comprehensive database
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


def extract_text_from_pdf(pdf_path, max_pages=5):
    """Extract text from first few pages of PDF."""
    text = ""
    
    # Try pdfplumber first (better quality)
    if HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages[:max_pages]):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception:
            pass
    
    # Fall back to PyPDF2
    if HAS_PYPDF2:
        try:
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(pdf_reader.pages[:max_pages]):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            pass
    
    return text


def extract_title_author_from_text(text):
    """Extract title and author from PDF text using intelligent patterns."""
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    # Look for common patterns in first 50 lines
    search_lines = lines[:50]
    text_lower = text.lower()
    
    # Pattern 1: Look for "Title" by "Author" or "Title" — "Author"
    for i, line in enumerate(search_lines):
        # Check for "by" pattern
        match = re.search(r'^(.+?)\s+by\s+(.+?)$', line, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            author = match.group(2).strip()
            # Validate: title should be reasonable length
            if 5 < len(title) < 100 and 3 < len(author) < 80:
                return title, author
        
        # Check for em/en dash pattern
        match = re.search(r'^(.+?)\s+[—–-]\s+(.+?)$', line)
        if match:
            title = match.group(1).strip()
            author = match.group(2).strip()
            if 5 < len(title) < 100 and 3 < len(author) < 80:
                return title, author
    
    # Pattern 2: Look for title on one line, author on next
    for i in range(len(search_lines) - 1):
        line1 = search_lines[i]
        line2 = search_lines[i + 1]
        
        # If line1 looks like a title and line2 looks like an author
        if (10 < len(line1) < 100 and 
            re.match(r'^[A-Z][^.!?]*$', line1) and  # Title-like (capitalized, no sentence enders)
            3 < len(line2) < 80 and
            re.search(r'\b[A-Z][a-z]+\s+[A-Z]', line2)):  # Author-like (has name pattern)
            return line1, line2
    
    # Pattern 3: Search for known book patterns in text
    # Look for lines that contain book-like phrases
    for line in search_lines:
        # Look for copyright or "Published by" patterns
        match = re.search(r'copyright\s+\d{4}\s+(.+?)(?:\s+by\s+)?(.+?)$', line, re.IGNORECASE)
        if match:
            author = match.group(1).strip() if match.group(1) else match.group(2).strip()
            # Look backwards for title
            idx = search_lines.index(line)
            if idx > 0:
                potential_title = search_lines[idx - 1]
                if 10 < len(potential_title) < 100:
                    return potential_title, author
    
    # Pattern 4: Extract from filename if it has useful info
    return None, None


def find_book_match(pdf_filename, pdf_text=None):
    """Find matching book from database using intelligence."""
    pdf_norm = normalize_for_search(pdf_filename)
    
    best_match = None
    best_score = 0
    
    # Strategy 1: Exact key match
    if pdf_norm in BOOK_DATABASE:
        return BOOK_DATABASE[pdf_norm], 1.0
    
    # Strategy 2: Key substring match
    for key, book_info in BOOK_DATABASE.items():
        key_norm = normalize_for_search(key)
        title_norm = normalize_for_search(book_info['title'])
        author_norm = normalize_for_search(book_info['author'])
        
        if key_norm in pdf_norm and len(key_norm) > 3:
            score = 0.9
            if title_norm in pdf_norm:
                score = 1.0
            if score > best_score:
                best_match = book_info
                best_score = score
                continue
        
        # Strategy 3: Title word overlap
        title_words = set(title_norm.split())
        pdf_words = set(pdf_norm.split())
        
        common_words = {'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'and', 'or', 'pdf', 'book'}
        title_words = title_words - common_words
        pdf_words = pdf_words - common_words
        
        if len(title_words) == 0:
            continue
            
        title_match = len(title_words.intersection(pdf_words))
        min_match = 2 if len(title_words) > 3 else 1
        
        if title_match >= min_match:
            overlap_ratio = title_match / len(title_words)
            score = 0.6 + (overlap_ratio * 0.3)
            
            author_words = set(author_norm.split()) - common_words
            if len(author_words) > 0:
                author_match = len(author_words.intersection(pdf_words))
                if author_match > 0:
                    score += 0.1
                    if author_match >= 2:
                        score += 0.05
            
            if score > best_score:
                best_match = book_info
                best_score = score
        
        # Strategy 4: If we have PDF text, search in it
        if pdf_text:
            text_norm = normalize_for_search(pdf_text[:2000])  # First 2000 chars
            if title_norm in text_norm:
                score = 0.85
                if author_norm in text_norm:
                    score = 0.95
                if score > best_score:
                    best_match = book_info
                    best_score = score
    
    return best_match, best_score


def sanitize_filename(filename):
    """Remove invalid characters for Windows filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    filename = filename.strip(' .')
    filename = re.sub(r'-+', '-', filename)
    return filename


def rename_pdf(pdf_file, dry_run=False):
    """Rename PDF using intelligence + extraction."""
    # Try intelligence matching first
    match, score = find_book_match(pdf_file.stem)
    
    if match and score >= 0.7:
        title = match['title']
        author = match['author']
        source = "intelligence"
    else:
        # Extract text from PDF
        print(f"Extracting text from: {pdf_file.name}...")
        pdf_text = extract_text_from_pdf(pdf_file)
        
        if pdf_text:
            # Try matching with extracted text
            match, score = find_book_match(pdf_file.stem, pdf_text)
            if match and score >= 0.7:
                title = match['title']
                author = match['author']
                source = "intelligence+extraction"
            else:
                # Extract title/author from text
                extracted_title, extracted_author = extract_title_author_from_text(pdf_text)
                if extracted_title and extracted_author:
                    title = extracted_title
                    author = extracted_author
                    source = "extraction"
                else:
                    # Try parsing filename
                    stem = pdf_file.stem
                    # Common patterns
                    if ' by ' in stem.lower():
                        parts = re.split(r'\s+by\s+', stem, flags=re.IGNORECASE)
                        if len(parts) == 2:
                            title = parts[0].strip()
                            author = parts[1].strip()
                            source = "parsing"
                        else:
                            return False
                    elif ' - ' in stem or ' — ' in stem:
                        parts = re.split(r'\s+[-—–]\s+', stem)
                        if len(parts) >= 2:
                            title = parts[0].strip()
                            author = parts[-1].strip()
                            source = "parsing"
                        else:
                            return False
                    else:
                        return False
        else:
            return False
    
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
        print(f"           -> {new_path.name}")
        print(f"           Method: {source}\n")
    else:
        pdf_file.rename(new_path)
        print(f"Renamed: {pdf_file.name} -> {new_path.name} ({source})")
    
    return True


def main():
    """Main function."""
    script_dir = Path(__file__).parent
    pdf_dir = script_dir / 'pdf'
    
    print("="*80)
    print("Enhanced PDF Renamer with Text Extraction")
    print("="*80)
    print(f"PyPDF2: {HAS_PYPDF2}, pdfplumber: {HAS_PDFPLUMBER}")
    print(f"Database keys: {len(BOOK_DATABASE)}\n")
    
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
        for name in not_matched[:20]:
            print(f"  - {name}")
    
    print("="*80)


if __name__ == '__main__':
    main()


