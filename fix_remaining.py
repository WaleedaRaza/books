"""Fix remaining unmatched PDFs"""

from pathlib import Path
import re

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    filename = filename.strip(' .')
    filename = re.sub(r'-+', '-', filename)
    return filename

# Manual fixes for remaining files
FIXES = {
    "Discourses - Epictetus (1).pdf": ("Discourses on Livy", "Niccolò Machiavelli"),  # Fix incorrect match
    "crowdastudypopu00bongoog.pdf": ("The Crowd: A Study of the Popular Mind", "Gustave Le Bon"),
    "Gracian.pdf": ("The Art of Worldly Wisdom", "Baltasar Gracián"),
}

def main():
    pdf_dir = Path('h:/Books/pdf')
    
    print("Fixing remaining files...")
    print("="*80)
    
    for old_name, (title, author) in FIXES.items():
        old_path = pdf_dir / old_name
        if not old_path.exists():
            print(f"SKIP: {old_name} (not found)")
            continue
        
        title = sanitize_filename(title)
        author = sanitize_filename(author)
        new_name = f"{title} - {author}.pdf"
        new_path = pdf_dir / new_name
        
        # Handle duplicates
        counter = 1
        original_new_path = new_path
        while new_path.exists() and new_path != old_path:
            stem = original_new_path.stem
            new_path = pdf_dir / f"{stem} ({counter}).pdf"
            counter += 1
        
        if new_path == old_path:
            print(f"SKIP: {old_name} (already correct)")
            continue
        
        try:
            old_path.rename(new_path)
            print(f"OK: {old_name}")
            print(f"  -> {new_path.name}")
        except Exception as e:
            print(f"ERROR: {old_name} - {e}")
    
    print("="*80)
    print("Done!")

if __name__ == '__main__':
    main()


