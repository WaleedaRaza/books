"""Test the discovery engine"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.discovery import PDFDiscoveryEngine

def test_search():
    print("Testing PDF Discovery Engine...")
    print("-" * 50)
    
    d = PDFDiscoveryEngine()
    
    # Test with a known book
    title = "Meditations"
    author = "Marcus Aurelius"
    
    print(f"Searching for: {title} by {author}")
    results = d.search_for_book(title, author)
    
    print(f"\nFound {len(results)} results:\n")
    
    for r in results:
        print(f"  Score: {r['score']:3d} | {r['source']:12s} | {r['confidence']:10s}")
        print(f"         {r['url'][:70]}...")
        print()
    
    return len(results) > 0

if __name__ == '__main__':
    success = test_search()
    print("-" * 50)
    print(f"Test {'PASSED' if success else 'FAILED'}")
