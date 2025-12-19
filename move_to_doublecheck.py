"""
Move unmatched PDFs and duplicates to doublecheck directory
"""

import re
from pathlib import Path
from collections import defaultdict

def main():
    """Move unmatched and duplicate PDFs to doublecheck folder."""
    script_dir = Path(__file__).parent
    pdf_dir = script_dir / 'pdf'
    doublecheck_dir = script_dir / 'doublecheck'
    
    # Create doublecheck directory if it doesn't exist
    doublecheck_dir.mkdir(exist_ok=True)
    
    print("="*80)
    print("Moving Unmatched PDFs and Duplicates to doublecheck/")
    print("="*80)
    print()
    
    # Get all PDFs
    all_pdfs = [f for f in pdf_dir.glob("*.pdf") if not f.name.endswith('.crdownload')]
    
    # Pattern for properly formatted files
    pattern = re.compile(r'^([^-]+) - ([^-]+)( \(\d+\))?\.pdf$')
    
    # Track properly formatted files by title-author
    formatted_files = defaultdict(list)
    unmatched_files = []
    
    for pdf_file in all_pdfs:
        match = pattern.match(pdf_file.name)
        if match:
            title = match.group(1).strip()
            author = match.group(2).strip()
            key = f"{title} - {author}"
            formatted_files[key].append(pdf_file)
        else:
            unmatched_files.append(pdf_file)
    
    moved_count = 0
    
    # Move unmatched files
    print("Moving unmatched PDFs:")
    print("-" * 80)
    for pdf_file in unmatched_files:
        try:
            dest = doublecheck_dir / pdf_file.name
            # Handle duplicates in doublecheck
            counter = 1
            original_dest = dest
            while dest.exists():
                stem = original_dest.stem
                dest = doublecheck_dir / f"{stem} ({counter}).pdf"
                counter += 1
            
            pdf_file.rename(dest)
            print(f"  MOVED: {pdf_file.name}")
            moved_count += 1
        except Exception as e:
            print(f"  ERROR moving {pdf_file.name}: {e}")
    
    print()
    
    # Move duplicates (keep first, move rest)
    print("Moving duplicate PDFs:")
    print("-" * 80)
    duplicates_moved = 0
    
    for key, files in formatted_files.items():
        if len(files) > 1:
            # Sort by modification time, keep the oldest (or first)
            files_sorted = sorted(files, key=lambda f: f.stat().st_mtime)
            keep_file = files_sorted[0]
            duplicate_files = files_sorted[1:]
            
            print(f"  Found {len(files)} copies of: {key}")
            print(f"    KEEPING: {keep_file.name}")
            
            for dup_file in duplicate_files:
                try:
                    dest = doublecheck_dir / dup_file.name
                    # Handle duplicates in doublecheck
                    counter = 1
                    original_dest = dest
                    while dest.exists():
                        stem = original_dest.stem
                        dest = doublecheck_dir / f"{stem} ({counter}).pdf"
                        counter += 1
                    
                    dup_file.rename(dest)
                    print(f"    MOVED: {dup_file.name}")
                    duplicates_moved += 1
                    moved_count += 1
                except Exception as e:
                    print(f"    ERROR moving {dup_file.name}: {e}")
            print()
    
    print("="*80)
    print(f"Summary:")
    print(f"  Unmatched PDFs moved: {len(unmatched_files)}")
    print(f"  Duplicate PDFs moved: {duplicates_moved}")
    print(f"  Total moved: {moved_count}")
    print(f"  Remaining in pdf/: {len(all_pdfs) - moved_count}")
    print("="*80)


if __name__ == '__main__':
    main()


