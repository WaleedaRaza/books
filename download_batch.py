"""
Download PDFs from open Chrome tabs to specific folder
Usage: python download_batch.py batch_14_books
       python download_batch.py batch_1_books
"""

import pyautogui
import time
import sys
from pathlib import Path

# Configuration
PDF_DIR = Path(__file__).parent / 'pdf'
DELAY = 0.8  # Delay between actions (adjust if needed)


def create_batch_folder(folder_name):
    """Create batch folder inside pdf/"""
    batch_path = PDF_DIR / folder_name
    batch_path.mkdir(parents=True, exist_ok=True)
    return batch_path.absolute()


def save_tab_to_folder(folder_path, delay=DELAY):
    """
    Save current PDF tab to specific folder.
    Strategy: Ctrl+S -> Type full path in filename field -> Enter -> Close tab
    """
    
    # Open Save dialog
    pyautogui.hotkey('ctrl', 's')
    time.sleep(delay)
    
    # Clear filename field and type full path
    # The filename field is usually auto-selected, but let's be safe
    pyautogui.hotkey('ctrl', 'a')  # Select all in filename field
    time.sleep(0.2)
    
    # Type the folder path (Windows will use it as save location)
    # We'll just use the filename Chrome suggests, but save to our folder
    # Strategy: Use the "location" dropdown/field
    
    # Press Alt+D to go to location bar in Save dialog
    pyautogui.hotkey('alt', 'd')
    time.sleep(0.3)
    
    # Type the full path
    pyautogui.write(str(folder_path), interval=0.01)
    time.sleep(0.3)
    
    # Press Enter to navigate to folder
    pyautogui.press('enter')
    time.sleep(delay)
    
    # Now press Enter again to save with default filename
    pyautogui.press('enter')
    time.sleep(delay)
    
    # Close tab
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.4)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExample:")
        print("  python download_batch.py batch_14_books")
        print("  python download_batch.py batch_1_books")
        return
    
    folder_name = sys.argv[1]
    
    # Create batch folder
    batch_path = create_batch_folder(folder_name)
    
    print("="*70)
    print("BATCH PDF DOWNLOADER")
    print("="*70)
    print(f"\nDownload to: {batch_path}")
    print(f"Folder: {folder_name}")
    print("\nInstructions:")
    print("  1. Make sure all PDF tabs are open in Chrome")
    print("  2. Click on the FIRST PDF tab you want to save")
    print("  3. Keep Chrome window active")
    print("  4. Don't touch keyboard/mouse while running")
    print("\nPress ENTER when ready...")
    input()
    
    print("\nStarting in 3 seconds - CLICK ON CHROME NOW!")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n[Running] Press Ctrl+C to stop\n")
    
    count = 0
    try:
        while True:
            count += 1
            print(f"[{count}] Downloading...", end=' ', flush=True)
            save_tab_to_folder(batch_path)
            print("[OK]")
    
    except KeyboardInterrupt:
        print(f"\n\n[Stopped]")
        print(f"Downloaded {count} file(s) to: {batch_path}")
        print("\nCheck the folder for your PDFs")
        print("="*70)


if __name__ == '__main__':
    main()
