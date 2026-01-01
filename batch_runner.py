"""
Fast Batch PDF Aggregation
Process books in small, manageable batches.

Usage:
  python batch_runner.py              # Show next batch to run
  python batch_runner.py run          # Run next batch (25 books)
  python batch_runner.py run 20       # Run next 20 books
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
RANKED_FILE = Path('Ranked_Library_Waves.md')
BATCHES_DIR = Path('batches')
PDF_DIR = Path('pdf')

BATCHES_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

# Search config
DEFAULT_BATCH_SIZE = 25
TABS_PER_BOOK = 5
DELAY_BETWEEN_BOOKS = 3

# Domain filtering (simple and effective)
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
    """Parse all books from Ranked_Library_Waves.md."""
    books = []
    with open(RANKED_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines[4:]:  # Skip header
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        
        match = re.match(r'(\d+)\.\s*(✅)?\s*\(([^)]+)\)\s*(.+?)\s*—\s*(.+?)(?:\s*\[|$)', line)
        if match:
            books.append({
                'number': int(match.group(1)),
                'done': bool(match.group(2)),
                'wave': match.group(3),
                'title': match.group(4).strip(),
                'author': match.group(5).strip()
            })
    
    return books


def get_batch_info():
    """Get info about existing batches and what's left."""
    all_books = parse_all_books()
    pending = [b for b in all_books if not b['done']]
    
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
        'done': len(all_books) - len(pending),
        'pending': len(pending),
        'pending_books': pending,
        'batches': existing_batches
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


def run_batch(size=DEFAULT_BATCH_SIZE, start_book=None, end_book=None):
    """Run next batch of books or specific range."""
    
    all_books = parse_all_books()
    
    if start_book and end_book:
        # Process specific range
        books_to_process = [b for b in all_books if start_book <= b['number'] <= end_book]
        actual_size = len(books_to_process)
    else:
        # Process next pending books
        info = get_batch_info()
        if info['pending'] == 0:
            print("No pending books!")
            return
        books_to_process = info['pending_books'][:size]
        actual_size = len(books_to_process)
    
    # Determine batch number
    if start_book and end_book:
        # Calculate batch number from start book
        batch_num = ((books_to_process[0]['number'] - 1) // DEFAULT_BATCH_SIZE) + 1
    else:
        info = get_batch_info()
        batch_num = len(info['batches']) + 1
    
    batch_name = f"batch_{batch_num:02d}"
    
    print(f"\n{'='*70}")
    print(f"BATCH {batch_num}: {actual_size} books")
    print(f"Books {books_to_process[0]['number']}-{books_to_process[-1]['number']}")
    print(f"{'='*70}")
    print(f"Folder: pdf/{batch_name}/")
    print(f"Opening {TABS_PER_BOOK} tabs per book")
    print()
    
    # Save batch metadata
    batch_meta = {
        'batch_num': batch_num,
        'started': datetime.now().isoformat(),
        'size': actual_size,
        'books': []
    }
    
    total_tabs = 0
    
    for i, book in enumerate(books_to_process, 1):
        print(f"[{i}/{actual_size}] {book['number']:04d}. {book['title']} — {book['author']}")
        
        # Search
        urls = search_book(book['title'], book['author'])
        
        if not urls:
            print("  No results")
            batch_meta['books'].append({
                'number': book['number'],
                'title': book['title'],
                'author': book['author'],
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
            'urls': urls
        })
        
        # Delay between books
        if i < actual_size:
            time.sleep(DELAY_BETWEEN_BOOKS)
    
    # Save metadata
    batch_meta['finished'] = datetime.now().isoformat()
    batch_meta['total_tabs'] = total_tabs
    
    meta_file = BATCHES_DIR / f'{batch_name}.json'
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(batch_meta, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"BATCH {batch_num} COMPLETE")
    print(f"{'='*70}")
    print(f"Opened {total_tabs} tabs for {actual_size} books")
    print(f"\nNext steps:")
    print(f"  1. Close junk tabs (keep good PDFs)")
    print(f"  2. Run: python download_batch.py {batch_name}")
    print(f"  3. Run: python batch_runner.py verify")


def list_batches():
    """List all batches."""
    info = get_batch_info()
    
    print(f"\n{'='*70}")
    print(f"BATCH STATUS")
    print(f"{'='*70}")
    print(f"Progress: {info['done']}/{info['total']} books")
    print(f"Pending: {info['pending']}")
    print()
    
    if info['batches']:
        print("Completed batches:")
        for b in info['batches']:
            print(f"  {b['folder']:20s} - {b['pdf_count']} PDFs")
    else:
        print("No batches yet")
    
    if info['pending'] > 0:
        next_books = info['pending_books'][:5]
        print(f"\nNext {len(next_books)} books:")
        for book in next_books:
            print(f"  {book['number']:04d}. {book['title']}")
        
        print(f"\nRun: python batch_runner.py run")


def verify_batch(batch_num):
    """Verify specific batch."""
    meta_file = BATCHES_DIR / f'batch_{batch_num:02d}.json'
    pdf_folder = PDF_DIR / f'batch_{batch_num:02d}'
    
    if not meta_file.exists():
        print(f"Batch {batch_num} not found")
        return
    
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    
    # Get PDFs in folder
    pdfs = []
    if pdf_folder.exists():
        pdfs = [f.name for f in pdf_folder.glob('*.pdf')]
    
    print(f"\n{'='*70}")
    print(f"BATCH {batch_num} VERIFICATION")
    print(f"{'='*70}")
    print(f"Books in batch: {len(meta['books'])}")
    print(f"PDFs downloaded: {len(pdfs)}")
    print()
    
    # Check each book
    missing = []
    for book in meta['books']:
        # Try to find matching PDF
        title_lower = book['title'].lower()
        found = any(title_lower[:20] in pdf.lower() for pdf in pdfs)
        
        status = "[OK]" if found else "[MISSING]"
        print(f"{status} {book['number']:04d}. {book['title']}")
        
        if not found:
            missing.append(book)
    
    if missing:
        print(f"\nMissing {len(missing)} books - add to retry list")


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
    print(f"Books done: {info['done']}")
    print(f"Pending: {info['pending']}")


def main():
    if len(sys.argv) < 2:
        list_batches()
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'run':
        size = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_BATCH_SIZE
        run_batch(size)
    
    elif cmd == 'range':
        if len(sys.argv) < 4:
            print("Usage: python batch_runner.py range START END")
            return
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        run_batch(start_book=start, end_book=end)
    
    elif cmd == 'list':
        list_batches()
    
    elif cmd == 'verify':
        if len(sys.argv) > 2:
            verify_batch(int(sys.argv[2]))
        else:
            verify_all()
    
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
