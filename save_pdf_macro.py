"""
Simple PDF Tab Saver Macro
Just simulates: Ctrl+S, Enter, Ctrl+W
That's it. No fancy stuff.
"""

import pyautogui
import time
import sys


def install_pyautogui():
    """Install pyautogui if needed."""
    try:
        import pyautogui
        return pyautogui
    except ImportError:
        print("Installing pyautogui...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
        import pyautogui
        return pyautogui


def save_and_close_tab(delay_between_actions=0.5):
    """Macro: Ctrl+S, Enter, Ctrl+W"""
    py = install_pyautogui()
    
    # Ctrl+S (Save)
    py.hotkey('ctrl', 's')
    time.sleep(delay_between_actions)
    
    # Enter (Confirm save)
    py.press('enter')
    time.sleep(delay_between_actions)
    
    # Ctrl+W (Close tab)
    py.hotkey('ctrl', 'w')
    time.sleep(delay_between_actions * 0.6)  # Slightly faster for closing


def main():
    """Main macro loop."""
    print("="*60)
    print("PDF Tab Saver Macro")
    print("="*60)
    print("\n📋 Instructions:")
    print("   1. Open all PDF tabs in Chrome")
    print("   2. Click on the FIRST PDF tab")
    print("   3. Make sure Chrome is the active window")
    print("\n⚠️  When timer starts, CLICK on the Chrome window!")
    print("    (Keep Chrome active and don't touch anything)")
    print("\nPress ENTER when ready to start...")
    input()
    
    print("\n⏱️  Starting in 3 seconds...")
    print("   👆 CLICK ON CHROME WINDOW NOW!")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🚀 Running macro...")
    print("   Press Ctrl+C to stop\n")
    
    count = 0
    try:
        while True:
            count += 1
            print(f"[{count}] Saving tab...", end=' ', flush=True)
            save_and_close_tab()
            print("✅")
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Stopped by user")
        print(f"✅ Processed {count} tab(s)")
        print("="*60)


if __name__ == '__main__':
    main()

