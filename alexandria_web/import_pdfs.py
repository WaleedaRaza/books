"""
Import existing PDFs from the pdf folder into the database.
Run this once to populate the library with Waleed's 1500+ books.
"""

import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from core.database import BookDatabase


def parse_pdf_filename(filename: str) -> tuple:
    """Parse a PDF filename into title and author."""
    # Remove .pdf extension
    name = filename.replace('.pdf', '')
    
    # Remove duplicate markers like (1), (2) at the end
    name = re.sub(r'\s*\(\d+\)$', '', name)
    
    # Try to split by " - " (Title - Author format)
    if ' - ' in name:
        parts = name.split(' - ', 1)
        title = parts[0].strip()
        author = parts[1].strip() if len(parts) > 1 else 'Unknown'
        return title, author
    
    # No author found
    return name.strip(), 'Unknown'


def import_pdfs(pdf_directory: str, db_path: str):
    """Import all PDFs from directory into database."""
    pdf_dir = Path(pdf_directory)
    db = BookDatabase(db_path)
    
    if not pdf_dir.exists():
        print(f"Directory not found: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob('*.pdf'))
    print(f"Found {len(pdf_files)} PDF files")
    
    imported = 0
    skipped = 0
    
    for pdf_file in pdf_files:
        title, author = parse_pdf_filename(pdf_file.name)
        
        # Check if already exists (by title)
        existing = db.get_all_books(search=title)
        if existing:
            # Check for exact match
            exact_match = any(b['title'].lower() == title.lower() for b in existing)
            if exact_match:
                skipped += 1
                continue
        
        # Add to database
        book_id = db.add_book(
            title=title,
            author=author,
            status='READY'
        )
        
        # Update with PDF path
        db.update_book(book_id, pdf_path=pdf_file.name)
        
        imported += 1
        if imported % 50 == 0:
            print(f"Imported {imported} books...")
    
    print(f"\nDone! Imported {imported} books, skipped {skipped} duplicates.")
    
    stats = db.get_statistics()
    print(f"Library now has {stats['total']} total books, {stats['ready']} ready.")


if __name__ == '__main__':
    # Paths
    pdf_directory = str(Path(__file__).parent.parent / 'pdf')
    db_path = str(Path(__file__).parent / 'data' / 'books.db')
    
    print(f"PDF Directory: {pdf_directory}")
    print(f"Database: {db_path}")
    print()
    
    import_pdfs(pdf_directory, db_path)
