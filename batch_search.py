"""
Batch PDF Search Tool
Search and open PDF links for books in batches of 100.

Usage:
  python batch_search.py 13                    # Batch 13 (books 1201-1300)
  python batch_search.py 13 --tabs 8           # Open 8 tabs per book
  python batch_search.py --range 1250 1275     # Custom range
  python batch_search.py --status              # Show progress
  python batch_search.py --mark 1201 1300      # Mark batch as done

Options:
  --tabs N    Open top N links per book (default: 5)
"""

import re
import sys
import time
import json
import webbrowser
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus
from ddgs import DDGS

# Configuration
RANKED_FILE = Path(__file__).parent / 'Ranked_Library_Waves.md'
LOG_DIR = Path(__file__).parent / 'logs'
PDF_DIR = Path(__file__).parent / 'pdf'

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

# ============================================================================
# Domain Filtering (proven logic from existing scripts)
# ============================================================================

BAD_DOMAINS = [
    'amazon.com', 'amazon.co.uk', 'amazon.ca', 'amazon.',
    'goodreads.com', 'wikipedia.org', 'wiki',
    'reddit.com', 'redd.it', 'quora.com',
    'youtube.com', 'youtu.be', 'facebook.com', 'fb.com',
    'twitter.com', 'x.com', 'linkedin.com', 'pinterest.com', 'instagram.com',
    'paywall', 'subscription', 'signup', 'register', 'login',
    '404', 'error', 'notfound', 'page-not-found',
    'adf.ly', 'bit.ly', 'tinyurl.com', 't.co',
    'spam', 'malware', 'virus', 'phishing',
    'bookstore', 'buy', 'purchase', 'shop',
    'review', 'summary', 'synopsis',
]

GOOD_DOMAINS = [
    'archive.org', 'libgen', 'pdfdrive', 'sci-hub',
    'researchgate.net', 'academia.edu', 'arxiv.org',
    'googleusercontent.com', 'drive.google.com', 'docs.google.com',
    'dropbox.com', 'github.com', 'github.io',
]


def is_bad_domain(url: str) -> bool:
    if not url:
        return True
    url_lower = url.lower()
    return any(bad in url_lower for bad in BAD_DOMAINS)


def is_good_domain(url: str) -> bool:
    if not url:
        return False
    url_lower = url.lower()
    return any(good in url_lower for good in GOOD_DOMAINS)


def score_url(url: str, title: str = '', body: str = '') -> tuple:
    """Score URL likelihood of being a real PDF. Returns (score, reason)."""
    if not url:
        return (0, "No URL")
    
    url_lower = url.lower()
    title_lower = (title or '').lower()
    body_lower = (body or '').lower()
    
    if is_bad_domain(url):
        return (-500, "Blocked")
    
    score = 0
    reasons = []
    
    # Direct PDF file - HUGE boost
    if url_lower.endswith('.pdf'):
        score += 300
        reasons.append("PDF")
    
    # Known good sources - BIG boost
    if 'archive.org' in url_lower:
        score += 100
        reasons.append("Archive")
    elif 'libgen' in url_lower:
        score += 90
        reasons.append("LibGen")
    elif is_good_domain(url):
        score += 60
        reasons.append("Good")
    
    # PDF in URL or title
    if '/pdf' in url_lower or 'pdf' in title_lower:
        score += 40
        reasons.append("PDF-ref")
    
    # Download indicators
    if 'download' in url_lower or 'download' in title_lower:
        score += 20
        reasons.append("DL")
    
    # Base score for any non-blocked URL
    if not reasons:
        score = 10
        reasons.append("OK")
    
    return (score, " ".join(reasons))


# ============================================================================
# Book Parsing
# ============================================================================

def parse_books(start: int, end: int) -> list:
    """Parse books from Ranked_Library_Waves.md for given range."""
    books = []
    
    with open(RANKED_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Lines start at index 4 (line 5) for book 1
    for line_idx, line in enumerate(lines[4:], start=1):
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        
        # Parse: "0001. ✅ (W1) Title — Author [category]" or "0001. (W1) Title — Author [category]"
        match = re.match(r'(\d+)\.\s*(✅)?\s*\(([^)]+)\)\s*(.+?)\s*—\s*(.+?)(?:\s*\[|$)', line)
        if match:
            book_num = int(match.group(1))
            
            if book_num < start or book_num > end:
                continue
            
            has_checkmark = bool(match.group(2))
            wave = match.group(3)
            title = match.group(4).strip()
            author = match.group(5).strip()
            
            books.append({
                'number': book_num,
                'title': title,
                'author': author,
                'wave': wave,
                'done': has_checkmark,
                'line_index': line_idx + 4,  # Actual line number in file
                'original_line': line
            })
    
    return books


def get_progress_status() -> dict:
    """Get current progress from checkmarks."""
    all_books = parse_books(1, 9999)
    
    done = [b for b in all_books if b['done']]
    pending = [b for b in all_books if not b['done']]
    
    # Group by wave
    waves = {}
    for b in all_books:
        w = b['wave']
        if w not in waves:
            waves[w] = {'done': 0, 'pending': 0}
        if b['done']:
            waves[w]['done'] += 1
        else:
            waves[w]['pending'] += 1
    
    return {
        'total': len(all_books),
        'done': len(done),
        'pending': len(pending),
        'done_numbers': [b['number'] for b in done],
        'waves': waves
    }


# ============================================================================
# Search Logic
# ============================================================================

def search_book(title: str, author: str, max_results: int = 20) -> list:
    """Search DDG for PDF links. Returns scored candidates."""
    candidates = []
    seen_urls = set()
    
    # Simple, effective search queries - all include "pdf"
    search_variants = [
        f"{title} {author} pdf",
        f"{title} {author} free pdf",
        f'"{title}" {author} pdf',
    ]
    
    try:
        with DDGS() as ddgs:
            for variant in search_variants:
                if len(candidates) >= max_results:
                    break
                
                try:
                    results = list(ddgs.text(variant, max_results=max_results))
                    
                    for r in results:
                        url = r.get('href', '') or r.get('url', '')
                        if not url or url in seen_urls:
                            continue
                        
                        seen_urls.add(url)
                        
                        # Only hard-block the worst domains
                        if is_bad_domain(url):
                            continue
                        
                        score, reason = score_url(url, r.get('title', ''), r.get('body', ''))
                        
                        # Less strict filtering - let user decide
                        if score > -50:
                            candidates.append({
                                'url': url,
                                'score': score,
                                'reason': reason,
                                'title': r.get('title', '')[:60]
                            })
                
                except Exception as e:
                    print(f"    [!] Search error: {e}")
                    continue
        
        # Sort by score descending
        candidates.sort(key=lambda x: x['score'], reverse=True)
        return candidates[:10]  # Top 10 (more options for user)
    
    except Exception as e:
        print(f"    [X] DDG error: {e}")
        return []


# ============================================================================
# Batch Processing
# ============================================================================

def process_batch(start: int, end: int, skip_done: bool = True, max_tabs: int = 5, delay: int = 3):
    """Process a batch of books."""
    
    books = parse_books(start, end)
    
    if skip_done:
        books = [b for b in books if not b['done']]
    
    if not books:
        print(f"No books to process in range {start}-{end}")
        return
    
    print(f"\n{'='*80}")
    print(f"BATCH: Books {start}-{end} ({len(books)} to process)")
    print(f"{'='*80}")
    print(f"PDFs save to: {PDF_DIR}")
    print(f"Opening top {max_tabs} links per book")
    print(f"Delay: {delay}s between books")
    print(f"\nTIP: Close junk tabs as they open, keep good PDFs")
    print()
    
    # Batch log
    batch_log = {
        'batch': f"{start}-{end}",
        'started': datetime.now().isoformat(),
        'books': []
    }
    
    total_opened = 0
    
    for i, book in enumerate(books, 1):
        print(f"\n[{i}/{len(books)}] #{book['number']:04d}: {book['title']} — {book['author']}")
        print("-" * 70)
        
        # Search
        results = search_book(book['title'], book['author'])
        
        if not results:
            print("  [X] No PDFs found")
            batch_log['books'].append({
                'number': book['number'],
                'title': book['title'],
                'found': 0,
                'opened': 0
            })
            time.sleep(delay)
            continue
        
        # Show top results only
        print(f"  Found {len(results)} links (showing top {min(len(results), max_tabs)}):")
        for j, r in enumerate(results[:max_tabs], 1):
            print(f"    {j}. [{r['score']:3d}] {r['reason']:15s} {r['url'][:50]}")
        
        # Open DDG search page first
        search_url = f"https://duckduckgo.com/?q={quote_plus(book['title'])} {quote_plus(book['author'])} pdf"
        webbrowser.open(search_url)
        time.sleep(0.5)
        
        # Open top PDF links
        opened = 0
        for r in results[:max_tabs]:
            webbrowser.open(r['url'])
            opened += 1
            time.sleep(0.4)
        
        print(f"  [OK] Opened {opened} tabs")
        total_opened += opened
        
        batch_log['books'].append({
            'number': book['number'],
            'title': book['title'],
            'author': book['author'],
            'found': len(results),
            'opened': opened,
            'urls': [r['url'] for r in results[:max_tabs]]
        })
        
        # Delay before next book
        if i < len(books):
            wait = delay + 3 if i % 5 == 0 else delay
            print(f"  [...] Waiting {wait}s...")
            time.sleep(wait)
    
    # Save log
    batch_log['finished'] = datetime.now().isoformat()
    batch_log['total_opened'] = total_opened
    
    log_file = LOG_DIR / f"batch_{start}_{end}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(batch_log, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"BATCH COMPLETE: {len(books)} books, {total_opened} tabs opened")
    print(f"Log saved: {log_file}")
    print(f"{'='*80}")
    
    # Offer to update checkmarks
    print(f"\nAfter downloading, run: python batch_search.py --mark {start} {end}")


def mark_done(start: int, end: int):
    """Add checkmarks to books in range."""
    with open(RANKED_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    updated = 0
    
    for i, line in enumerate(lines):
        # Match book lines without checkmark
        match = re.match(r'^(\d{4})\.\s+(\([^)]+\))', line)
        if match:
            book_num = int(match.group(1))
            if start <= book_num <= end:
                # Add checkmark if not present
                if '✅' not in line:
                    # Insert ✅ after the number and before the wave
                    new_line = re.sub(r'^(\d{4}\.)\s+(\([^)]+\))', r'\1 ✅ \2', line)
                    lines[i] = new_line
                    updated += 1
    
    if updated > 0:
        with open(RANKED_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"[OK] Marked {updated} books as done ({start}-{end})")
    else:
        print(f"No books to mark in range {start}-{end}")


def show_status():
    """Show progress status."""
    status = get_progress_status()
    
    print(f"\n{'='*60}")
    print(f"PROGRESS STATUS")
    print(f"{'='*60}")
    print(f"Total books: {status['total']}")
    print(f"Done:        {status['done']}")
    print(f"Pending:     {status['pending']}")
    print(f"\nBy Wave:")
    
    for wave, counts in sorted(status['waves'].items()):
        total = counts['done'] + counts['pending']
        pct = (counts['done'] / total * 100) if total > 0 else 0
        bar = '#' * int(pct / 5) + '-' * (20 - int(pct / 5))
        print(f"  {wave}: [{bar}] {counts['done']}/{total} ({pct:.0f}%)")
    
    print(f"\nNext batches to run:")
    # Find first unchecked book
    pending_start = None
    for num in range(1, status['total'] + 1):
        if num not in status['done_numbers']:
            pending_start = num
            break
    
    if pending_start:
        batch_num = (pending_start - 1) // 100 + 1
        print(f"  python batch_search.py {batch_num}  # Books {(batch_num-1)*100+1}-{batch_num*100}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        show_status()
        return
    
    arg = sys.argv[1]
    
    # Options
    max_tabs = 5  # default
    delay = 3  # default
    
    # Check for --tabs option
    if '--tabs' in sys.argv:
        idx = sys.argv.index('--tabs')
        if idx + 1 < len(sys.argv):
            max_tabs = int(sys.argv[idx + 1])
            sys.argv.pop(idx)  # remove --tabs
            sys.argv.pop(idx)  # remove number
    
    if arg == '--status':
        show_status()
    
    elif arg == '--range':
        if len(sys.argv) < 4:
            print("Usage: python batch_search.py --range START END [--tabs N]")
            return
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        process_batch(start, end, max_tabs=max_tabs, delay=delay)
    
    elif arg == '--mark':
        if len(sys.argv) < 4:
            print("Usage: python batch_search.py --mark START END")
            return
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        mark_done(start, end)
    
    elif arg.isdigit():
        batch_num = int(arg)
        start = (batch_num - 1) * 100 + 1
        end = batch_num * 100
        process_batch(start, end, max_tabs=max_tabs, delay=delay)
    
    else:
        print(f"Unknown argument: {arg}")
        print(__doc__)


if __name__ == '__main__':
    main()
