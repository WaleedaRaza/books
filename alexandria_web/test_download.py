"""Test the download manager with a real PDF"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.downloader import DownloadManager
from core.discovery import PDFDiscoveryEngine
import time

def test_real_download():
    print("Testing Full Pipeline: Discovery -> Download")
    print("=" * 50)
    
    # Step 1: Find a PDF
    print("\n[1] Searching for a book...")
    discovery = PDFDiscoveryEngine()
    results = discovery.search_for_book("The Art of War", "Sun Tzu")
    
    if not results:
        print("  No PDFs found!")
        return False
    
    # Get highest scored URL
    best = results[0]
    print(f"  Found: {best['url'][:70]}...")
    print(f"  Score: {best['score']}, Source: {best['source']}")
    
    # Step 2: Download it
    print("\n[2] Downloading...")
    test_dir = Path(__file__).parent / 'test_downloads'
    test_dir.mkdir(exist_ok=True)
    
    # Clean old test files
    for f in test_dir.glob('*.pdf'):
        f.unlink()
    
    dm = DownloadManager(str(test_dir))
    dm.queue_downloads([best['url']])
    
    # Wait for download
    max_wait = 30
    for i in range(max_wait):
        status = dm.get_queue_status()
        
        # Show progress
        if status['active_downloads']:
            progress = status['active_downloads'][0].get('progress', 0)
            print(f"  [{i+1}s] Downloading... {progress}%")
        else:
            print(f"  [{i+1}s] Q:{status['queued']} C:{status['completed']} F:{status['failed']}")
        
        if status['completed'] > 0:
            print(f"\n  SUCCESS!")
            files = list(test_dir.glob('*.pdf'))
            for f in files:
                size_kb = f.stat().st_size / 1024
                print(f"    Downloaded: {f.name} ({size_kb:.1f} KB)")
            return True
        
        if status['failed'] > 0:
            print(f"\n  FAILED!")
            if dm.failed_downloads:
                print(f"  Error: {dm.failed_downloads[-1].get('error', 'Unknown')}")
            return False
        
        time.sleep(1)
    
    print("\n  TIMEOUT")
    return False

if __name__ == '__main__':
    success = test_real_download()
    print("\n" + "=" * 50)
    print(f"Pipeline test: {'PASSED' if success else 'FAILED'}")
