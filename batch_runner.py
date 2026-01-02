"""
Fast Batch PDF Aggregation
Process books in small, manageable batches from Newbooks.txt.

Usage:
  python batch_runner.py              # Show status
  python batch_runner.py run          # Run next batch (25 books)
  python batch_runner.py range 1 25   # Run specific book range (line-based)
  python batch_runner.py verify       # Check what you've downloaded
  python batch_runner.py list         # List all batches
"""

import re
import sys
import json
import time
import webbrowser
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus
from ddgs import DDGS

# Configuration
BOOKS_FILE = Path('Newbooks.txt')
BATCHES_DIR = Path('batches')
PDF_DIR = Path('pdf')
LOGS_DIR = Path('logs')

BATCHES_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Search config
DEFAULT_BATCH_SIZE = 25
TABS_PER_BOOK = 5
DELAY_BETWEEN_BOOKS = 3
HEADER_LINES = 2  # First 2 lines are header text

# Domain filtering
BAD_DOMAINS = [
    'amazon', 'goodreads', 'wikipedia', 'reddit', 'quora',
    'youtube', 'facebook', 'twitter', 'linkedin', 'pinterest',
    'paywall', 'subscription', 'signup', 'register',
    'buy', 'purchase', 'shop'
]

GOOD_DOMAINS = [
    'archive.org', 'libgen', 'pdfdrive', 'sci-hub',
    'researchgate.net', 'academia.edu', 'arxiv.org',
    'github.com', 'drive.google.com'
]


def parse_all_books():
    """Parse all books from Newbooks.txt - simple line-based."""
    books = []
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header lines, process rest
    book_num = 0
    for i, line in enumerate(lines):
        if i < HEADER_LINES:
            continue
        
        line = line.strip()
        if not line or not line.startswith('-'):
            continue
        
        book_num += 1
        
        # Parse: - Title — Author
        content = line[1:].strip()  # Remove leading dash
        
        # Split on em-dash or double hyphen
        if ' — ' in content:
            parts = content.split(' — ', 1)
        elif ' -- ' in content:
            parts = content.split(' -- ', 1)
        else:
            parts = [content, 'Unknown']
        
        title = parts[0].strip()
        author = parts[1].strip() if len(parts) > 1 else 'Unknown'
        
        # Clean up common artifacts
        title = re.sub(r'^Free PDF', '', title).strip()
        author = re.sub(r'^Free PDF', '', author).strip()
        
        books.append({
            'number': book_num,
            'line': i + 1,  # 1-indexed line number
            'title': title,
            'author': author
        })
    
    return books


def get_batch_info():
    """Get info about existing batches and what's left."""
    all_books = parse_all_books()
    
    # Find existing batch folders
    existing_batches = []
    for folder in PDF_DIR.glob('batch_*'):
        if folder.is_dir():
            batch_num = int(folder.name.split('_')[1])
            pdf_count = len(list(folder.glob('*.pdf')))
            existing_batches.append({
                'num': batch_num,
                'folder': folder.name,
                'pdf_count': pdf_count
            })
    
    existing_batches.sort(key=lambda x: x['num'])
    
    return {
        'total': len(all_books),
        'batches': existing_batches,
        'all_books': all_books
    }


def search_book(title, author):
    """Simple, effective search."""
    candidates = []
    seen_urls = set()
    
    queries = [
        f"{title} {author} pdf",
        f'"{title}" {author} pdf',
    ]
    
    try:
        ddgs = DDGS()
        for query in queries:
            try:
                results = list(ddgs.text(query, max_results=15))
                for r in results:
                    url = r.get('href', '')
                    if not url or url in seen_urls:
                        continue
                    
                    seen_urls.add(url)
                    url_lower = url.lower()
                    
                    # Skip bad domains
                    if any(bad in url_lower for bad in BAD_DOMAINS):
                        continue
                    
                    # Score
                    score = 0
                    if url_lower.endswith('.pdf'):
                        score += 300
                    if 'archive.org' in url_lower:
                        score += 100
                    elif 'libgen' in url_lower:
                        score += 90
                    elif any(good in url_lower for good in GOOD_DOMAINS):
                        score += 60
                    if '/pdf' in url_lower:
                        score += 40
                    
                    if score > 0:
                        candidates.append({'url': url, 'score': score})
            
            except:
                continue
        
        candidates.sort(key=lambda x: x['score'], reverse=True)
        return [c['url'] for c in candidates[:TABS_PER_BOOK]]
    
    except:
        return []


def run_batch(start_book=None, end_book=None):
    """Run batch for specific book range (1-indexed, based on line order)."""
    
    all_books = parse_all_books()
    
    if start_book is None or end_book is None:
        print("Usage: python batch_runner.py range START END")
        print("Example: python batch_runner.py range 1 25")
        return
    
    # Filter to exact range (1-indexed book numbers)
    books_to_process = [b for b in all_books if start_book <= b['number'] <= end_book]
    
    if not books_to_process:
        print(f"No books found in range {start_book}-{end_book}")
        return
    
    actual_size = len(books_to_process)
    
    # Calculate batch number from start book
    batch_num = ((start_book - 1) // DEFAULT_BATCH_SIZE) + 1
    batch_name = f"batch_{batch_num:02d}"
    
    print(f"\n{'='*70}")
    print(f"BATCH {batch_num}: Books {start_book}-{end_book} ({actual_size} books)")
    print(f"{'='*70}")
    print(f"Source: {BOOKS_FILE}")
    print(f"Folder: pdf/{batch_name}/")
    print(f"Opening {TABS_PER_BOOK} tabs per book")
    print()
    
    # Show what we're about to process
    print("Books in this batch:")
    for book in books_to_process[:5]:
        print(f"  #{book['number']:4d}. {book['title'][:50]}")
    if len(books_to_process) > 5:
        print(f"  ... and {len(books_to_process) - 5} more")
    print()
    
    # Confirm
    input("Press ENTER to start (Ctrl+C to cancel)...")
    print()
    
    # Save batch metadata
    batch_meta = {
        'batch': f"{start_book}-{end_book}",
        'started': datetime.now().isoformat(),
        'books': []
    }
    
    total_tabs = 0
    
    for i, book in enumerate(books_to_process, 1):
        print(f"[{i}/{actual_size}] #{book['number']:04d}. {book['title'][:45]} — {book['author'][:20]}")
        
        # Search
        urls = search_book(book['title'], book['author'])
        
        if not urls:
            print("  No results")
            batch_meta['books'].append({
                'number': book['number'],
                'title': book['title'],
                'author': book['author'],
                'found': 0,
                'opened': 0,
                'urls': []
            })
            continue
        
        print(f"  Opening {len(urls)} tabs...")
        
        # Open tabs
        for url in urls:
            webbrowser.open(url)
            total_tabs += 1
            time.sleep(0.3)
        
        batch_meta['books'].append({
            'number': book['number'],
            'title': book['title'],
            'author': book['author'],
            'found': len(urls),
            'opened': len(urls),
            'urls': urls
        })
        
        # Delay between books
        if i < actual_size:
            time.sleep(DELAY_BETWEEN_BOOKS)
    
    # Save log
    batch_meta['finished'] = datetime.now().isoformat()
    batch_meta['total_opened'] = total_tabs
    
    log_file = LOGS_DIR / f'batch_{start_book}_{end_book}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(batch_meta, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"BATCH COMPLETE: Books {start_book}-{end_book}")
    print(f"{'='*70}")
    print(f"Opened {total_tabs} tabs for {actual_size} books")
    print(f"Log saved: {log_file}")
    print(f"\nNext steps:")
    print(f"  1. Close junk tabs (keep good PDFs)")
    print(f"  2. Run: python download_batch.py {batch_name}")


def list_batches():
    """List all batches and current status."""
    info = get_batch_info()
    
    total_batches = (info['total'] + DEFAULT_BATCH_SIZE - 1) // DEFAULT_BATCH_SIZE
    
    print(f"\n{'='*70}")
    print(f"BATCH STATUS - {info['total']} books in {BOOKS_FILE}")
    print(f"{'='*70}")
    print(f"Total batches needed: {total_batches} (at {DEFAULT_BATCH_SIZE} books each)")
    print()
    
    if info['batches']:
        print("Downloaded batches:")
        for b in info['batches']:
            print(f"  {b['folder']:20s} - {b['pdf_count']} PDFs")
    else:
        print("No batches downloaded yet")
    
    print(f"\nBatch ranges:")
    for i in range(1, min(total_batches + 1, 11)):  # Show first 10
        start = (i - 1) * DEFAULT_BATCH_SIZE + 1
        end = min(i * DEFAULT_BATCH_SIZE, info['total'])
        odd_even = "ODD" if i % 2 == 1 else "EVEN"
        print(f"  batch_{i:02d}.bat = Books {start:4d}-{end:4d}  [{odd_even}]")
    
    if total_batches > 10:
        print(f"  ... and {total_batches - 10} more batches")
    
    print(f"\nUsage:")
    print(f"  Run odds:  batch_01.bat, batch_03.bat, batch_05.bat...")
    print(f"  Run evens: batch_02.bat, batch_04.bat, batch_06.bat...")


def verify_all():
    """Quick verification of all batches."""
    info = get_batch_info()
    
    print(f"\n{'='*70}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*70}")
    
    total_pdfs = 0
    for b in info['batches']:
        total_pdfs += b['pdf_count']
        print(f"Batch {b['num']:2d}: {b['pdf_count']:3d} PDFs")
    
    print(f"\nTotal PDFs: {total_pdfs}")
    print(f"Total books: {info['total']}")


def main():
    if len(sys.argv) < 2:
        list_batches()
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'run':
        # Run next batch (not implemented - use range instead)
        print("Use: python batch_runner.py range START END")
        print("Or run the batch .bat files directly")
    
    elif cmd == 'range':
        if len(sys.argv) < 4:
            print("Usage: python batch_runner.py range START END")
            print("Example: python batch_runner.py range 1 25")
            return
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        run_batch(start_book=start, end_book=end)
    
    elif cmd == 'list':
        list_batches()
    
    elif cmd == 'verify':
        verify_all()
    
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
