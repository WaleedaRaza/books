"""
Generate individual batch scripts for easy iteration.
Run once to create batch_01.bat through batch_53.bat
"""

from pathlib import Path

# Total books: 1326
# Batch size: 25
# Total batches needed: 53

BATCH_SIZE = 25
TOTAL_BOOKS = 1326
TOTAL_BATCHES = (TOTAL_BOOKS + BATCH_SIZE - 1) // BATCH_SIZE  # 53

def generate_batch_scripts():
    """Generate all batch .bat files."""
    
    scripts_created = []
    
    for batch_num in range(1, TOTAL_BATCHES + 1):
        start_book = (batch_num - 1) * BATCH_SIZE + 1
        end_book = min(batch_num * BATCH_SIZE, TOTAL_BOOKS)
        
        batch_name = f"batch_{batch_num:02d}"
        script_name = f"{batch_name}.bat"
        
        # Create .bat file
        bat_content = f"""@echo off
REM Batch {batch_num}: Books {start_book}-{end_book}
echo ====================================================================
echo BATCH {batch_num}: Books {start_book}-{end_book}
echo ====================================================================
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
    
    # Create master script
    master_content = """@echo off
REM Master script to check status
python batch_runner.py
pause
"""
    
    with open('status.bat', 'w') as f:
        f.write(master_content)
    
    # Create verify script
    verify_content = """@echo off
REM Verify all batches
python batch_runner.py verify
pause
"""
    
    with open('verify.bat', 'w') as f:
        f.write(verify_content)
    
    print(f"Created {len(scripts_created)} batch scripts:")
    print(f"  - batch_01.bat through batch_{TOTAL_BATCHES:02d}.bat")
    print(f"  - batch_01_download.bat through batch_{TOTAL_BATCHES:02d}_download.bat")
    print(f"  - status.bat (check progress)")
    print(f"  - verify.bat (verify all batches)")
    print()
    print("Usage:")
    print("  1. Double-click batch_01.bat")
    print("  2. Close junk tabs, keep PDFs")
    print("  3. Double-click batch_01_download.bat")
    print("  4. Repeat with batch_02.bat, etc.")


if __name__ == '__main__':
    generate_batch_scripts()
