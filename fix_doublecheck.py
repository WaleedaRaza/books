"""
Move back properly formatted files from doublecheck that were incorrectly moved
"""

from pathlib import Path
import re

def main():
    """Move back files that are actually properly formatted."""
    script_dir = Path(__file__).parent
    pdf_dir = script_dir / 'pdf'
    doublecheck_dir = script_dir / 'doublecheck'
    
    if not doublecheck_dir.exists():
        print("doublecheck directory doesn't exist")
        return
    
    print("="*80)
    print("Moving back properly formatted files from doublecheck/")
    print("="*80)
    print()
    
    # Pattern that allows hyphens in title/author but requires " - " separator
    # This matches: "Title - Author.pdf" or "Title - Author (1).pdf"
    pattern = re.compile(r'^(.+?)\s+-\s+(.+?)(\s+\(\d+\))?\.pdf$')
    
    moved_back = 0
    
    for pdf_file in doublecheck_dir.glob("*.pdf"):
        match = pattern.match(pdf_file.name)
        if match:
            title = match.group(1).strip()
            author = match.group(2).strip()
            
            # Basic validation: title and author should have reasonable length
            if len(title) > 3 and len(author) > 2:
                try:
                    dest = pdf_dir / pdf_file.name
                    # Handle duplicates
                    counter = 1
                    original_dest = dest
                    while dest.exists():
                        stem = original_dest.stem
                        dest = pdf_dir / f"{stem} ({counter}).pdf"
                        counter += 1
                    
                    pdf_file.rename(dest)
                    print(f"  MOVED BACK: {pdf_file.name}")
                    moved_back += 1
                except Exception as e:
                    print(f"  ERROR moving back {pdf_file.name}: {e}")
    
    print()
    print("="*80)
    print(f"Moved back {moved_back} properly formatted files")
    print("="*80)


if __name__ == '__main__':
    main()


