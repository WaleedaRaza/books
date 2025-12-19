"""
Fix remaining files with colons and formatting issues
"""

from pathlib import Path
import re

def sanitize_filename(filename):
    """Remove invalid characters for Windows filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    filename = filename.strip(' .')
    filename = re.sub(r'-+', '-', filename)
    return filename

def main():
    """Fix files with colons."""
    pdf_dir = Path('h:/Books/pdf')
    
    # Files that need colon removal/fixing
    fixes = {
        "MongoDB- The Definitive Guide - Kristina Chodorow.pdf": ("MongoDB: The Definitive Guide", "Kristina Chodorow"),
        "Noise- A Flaw in Human Judgment - Daniel Kahneman, Olivier Sibony, Cass R. Sunstein.pdf": ("Noise: A Flaw in Human Judgment", "Daniel Kahneman, Olivier Sibony, Cass R. Sunstein"),
        "Metasploit- The Penetration Tester's Guide - David Kennedy et al.pdf": ("Metasploit: The Penetration Tester's Guide", "David Kennedy et al."),
        "Boyd- The Fighter Pilot Who Changed the Art of War - Robert Coram.pdf": ("Boyd: The Fighter Pilot Who Changed the Art of War", "Robert Coram"),
    }
    
    print("Fixing files with colons...")
    print("="*80)
    
    for old_name, (title, author) in fixes.items():
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


