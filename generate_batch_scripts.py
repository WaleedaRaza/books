"""
Generate individual batch scripts for easy iteration.
Run once to create batch_01.bat through batch_XX.bat

Based on Newbooks.txt - simple line-based batching.
"""

import re
from pathlib import Path

BOOKS_FILE = Path('Newbooks.txt')
BATCH_SIZE = 25
HEADER_LINES = 2


def count_books():
    """Count books in Newbooks.txt."""
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    count = 0
    for i, line in enumerate(lines):
        if i < HEADER_LINES:
            continue
        line = line.strip()
        if line and line.startswith('-'):
            count += 1
    
    return count


def generate_batch_scripts():
    """Generate all batch .bat files."""
    
    total_books = count_books()
    total_batches = (total_books + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"Found {total_books} books in {BOOKS_FILE}")
    print(f"Generating {total_batches} batch scripts...")
    print()
    
    scripts_created = []
    
    for batch_num in range(1, total_batches + 1):
        start_book = (batch_num - 1) * BATCH_SIZE + 1
        end_book = min(batch_num * BATCH_SIZE, total_books)
        
        batch_name = f"batch_{batch_num:02d}"
        script_name = f"{batch_name}.bat"
        
        odd_even = "ODD" if batch_num % 2 == 1 else "EVEN"
        
        # Create .bat file
        bat_content = f"""@echo off
REM Batch {batch_num} [{odd_even}]: Books {start_book}-{end_book}
REM Source: Newbooks.txt (line-based)
echo ====================================================================
echo BATCH {batch_num} [{odd_even}]: Books {start_book}-{end_book}
echo ====================================================================
echo.
echo Run ODD batches (1,3,5,7...) on one machine
echo Run EVEN batches (2,4,6,8...) on another machine
echo.

REM Run search and open tabs for specific book range
python batch_runner.py range {start_book} {end_book}

echo.
echo ====================================================================
echo BATCH {batch_num} SEARCH COMPLETE
echo ====================================================================
echo.
echo Next steps:
echo   1. Close junk tabs (keep good PDFs)
echo   2. Run: {batch_name}_download.bat
echo.
pause
"""
        
        with open(script_name, 'w') as f:
            f.write(bat_content)
        
        # Create download script
        download_name = f"{batch_name}_download.bat"
        download_content = f"""@echo off
REM Download PDFs for Batch {batch_num}
echo ====================================================================
echo DOWNLOADING BATCH {batch_num} PDFs
echo ====================================================================
echo.
echo Make sure you're on the first PDF tab in Chrome!
echo.

python download_batch.py {batch_name}

echo.
echo ====================================================================
echo Check: pdf\\{batch_name}\\
echo ====================================================================
echo.
pause
"""
        
        with open(download_name, 'w') as f:
            f.write(download_content)
        
        scripts_created.append(script_name)
        scripts_created.append(download_name)
    
    # Create status script
    with open('status.bat', 'w') as f:
        f.write("""@echo off
REM Check batch status
python batch_runner.py list
pause
""")
    
    # Create verify script
    with open('verify.bat', 'w') as f:
        f.write("""@echo off
REM Verify all batches
python batch_runner.py verify
pause
""")
    
    print(f"Created {len(scripts_created)} batch scripts:")
    print()
    print("ODD batches (you run these):")
    for i in range(1, min(total_batches + 1, 11), 2):
        start = (i - 1) * BATCH_SIZE + 1
        end = min(i * BATCH_SIZE, total_books)
        print(f"  batch_{i:02d}.bat  -> Books {start:4d}-{end:4d}")
    print()
    print("EVEN batches (friend runs these):")
    for i in range(2, min(total_batches + 1, 11), 2):
        start = (i - 1) * BATCH_SIZE + 1
        end = min(i * BATCH_SIZE, total_books)
        print(f"  batch_{i:02d}.bat  -> Books {start:4d}-{end:4d}")
    print()
    print("NO OVERLAP - each batch has completely different books!")
    print()
    print("Usage:")
    print("  1. Double-click batch_01.bat (or batch_03, batch_05...)")
    print("  2. Close junk tabs, keep PDFs")
    print("  3. Double-click batch_01_download.bat")
    print("  4. Repeat with next ODD batch")


if __name__ == '__main__':
    generate_batch_scripts()
