"""
Enhanced script to search for books 21-50 from Ranked_Library_Waves.md
Searches for "[title] [author] free pdf online" and intelligently finds actual PDF files.
Prioritizes direct PDF links, filters paywalls/404s, looks at first 10 results.
"""

import re
import time
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus, urlparse
from ddgs import DDGS


def extract_books_21_50(file_path):
    """Extract books 21-50 from Ranked_Library_Waves.md and parse title/author."""
    books = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header lines (4 lines) and process books 21-50
    # Book 1 is at line 5 (index 4), so book 21 is at line 25 (index 24)
    # Books 21-50 are at indices 24-53
    for i, line in enumerate(lines[24:54], start=21):
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        
        # Parse format: "0021. (W1) Title — Author [category]"
        # Handle checkmarks if present
        match = re.match(r'\d+\.\s*✅?\s*\([^)]+\)\s*(.+?)\s*—\s*(.+?)\s*\[', line)
        if match:
            title = match.group(1).strip()
            author = match.group(2).strip()
            
            # Create search query
            search_query = f"{title} {author} free pdf online"
            books.append({
                'number': i,
                'title': title,
                'author': author,
                'search_query': search_query,
                'full_line': line
            })
    
    return books


def is_bad_domain(url):
    """Check if URL is from a domain we want to avoid (paywalls, sketchy sites, etc.)."""
    if not url:
        return True
    
    url_lower = url.lower()
    bad_domains = [
        'amazon.com', 'amazon.co.uk', 'amazon.ca',
        'goodreads.com',
        'wikipedia.org',
        'reddit.com',
        'quora.com',
        'youtube.com',
        'facebook.com',
        'twitter.com',
        'linkedin.com',
        'pinterest.com',
        'paywall', 'subscription', 'signup', 'register',
        '404', 'error', 'notfound',
        'adf.ly', 'bit.ly', 'tinyurl.com',  # URL shorteners (often spam)
        'spam', 'malware', 'virus'
    ]
    
    return any(bad in url_lower for bad in bad_domains)


def is_good_pdf_domain(url):
    """Check if URL is from a known good PDF hosting domain."""
    if not url:
        return False
    
    url_lower = url.lower()
    good_domains = [
        'archive.org',
        'libgen',
        'pdfdrive',
        'sci-hub',
        'researchgate.net',
        'academia.edu',
        'arxiv.org',
        'googleusercontent.com',  # Google Docs/Drive PDFs
        'drive.google.com',
        'dropbox.com',
        'github.com',  # Sometimes has PDFs
        'edu',  # Educational institutions
        'gov',  # Government sites
    ]
    
    return any(good in url_lower for good in good_domains)


def score_pdf_url(url, title, body):
    """Score a URL based on how likely it is to be an actual readable PDF.
    Higher score = better. Returns (score, reason)."""
    if not url:
        return (0, "No URL")
    
    url_lower = url.lower()
    title_lower = title.lower() if title else ""
    body_lower = body.lower() if body else ""
    
    score = 0
    reasons = []
    
    # Highest priority: Direct PDF file
    if url_lower.endswith('.pdf'):
        score += 100
        reasons.append("Direct PDF file")
    
    # High priority: PDF in path
    if '/pdf' in url_lower or 'filetype=pdf' in url_lower or 'format=pdf' in url_lower:
        score += 80
        reasons.append("PDF in URL path")
    
    # Good domains get bonus
    if is_good_pdf_domain(url):
        score += 50
        reasons.append("Known PDF hosting domain")
    
    # Bad domains get penalized heavily
    if is_bad_domain(url):
        score -= 200
        reasons.append("BAD: Paywall/sketchy domain")
        return (score, ", ".join(reasons))
    
    # Title/body indicators
    if 'pdf' in title_lower or 'pdf' in body_lower:
        score += 30
        reasons.append("PDF mentioned in title/body")
    
    if 'download' in title_lower and 'pdf' in title_lower:
        score += 20
        reasons.append("Download PDF in title")
    
    # Avoid pages that are just listings
    if any(word in url_lower for word in ['list', 'search', 'results', 'index']):
        score -= 10
        reasons.append("Likely listing page")
    
    # Prefer shorter URLs (often more direct)
    if len(url) < 100:
        score += 5
        reasons.append("Short URL (likely direct)")
    
    return (score, ", ".join(reasons) if reasons else "Generic link")


def find_best_pdf_links(search_query, max_results_to_check=10, max_pdfs_to_open=3):
    """Search and intelligently find the best PDF links.
    Checks up to max_results_to_check results, returns up to max_pdfs_to_open best ones."""
    candidates = []
    
    try:
        print(f"Searching: {search_query}")
        
        # Try multiple search strategies
        search_variants = [
            f"{search_query} filetype:pdf",  # Try filetype first (most specific)
            search_query,
            f'"{search_query}" pdf',
        ]
        
        seen_urls = set()
        
        with DDGS() as ddgs:
            for variant in search_variants:
                if len(candidates) >= max_results_to_check:
                    break
                    
                try:
                    results = list(ddgs.text(variant, max_results=max_results_to_check))
                    
                    # Score each result
                    for result in results:
                        if len(candidates) >= max_results_to_check:
                            break
                            
                        url = result.get('href', '') or result.get('url', '') or result.get('link', '')
                        
                        if not url or url in seen_urls:
                            continue
                        
                        seen_urls.add(url)
                        
                        # Skip bad domains immediately
                        if is_bad_domain(url):
                            continue
                        
                        title = result.get('title', '')
                        body = result.get('body', '')
                        
                        # Score this URL
                        score, reason = score_pdf_url(url, title, body)
                        
                        # Only consider if score is positive (or at least not heavily penalized)
                        if score > -50:
                            candidates.append({
                                'url': url,
                                'score': score,
                                'reason': reason,
                                'title': title
                            })
                            print(f"  [{score:4d}] {url[:70]}... ({reason})")
                    
                except Exception as e:
                    print(f"  Error with variant '{variant}': {e}")
                    continue
        
        # Sort by score (highest first)
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # Take top max_pdfs_to_open
        best_pdfs = candidates[:max_pdfs_to_open]
        
        if not best_pdfs:
            print(f"  ✗ No good PDFs found")
        else:
            print(f"\n  ✓ Selected {len(best_pdfs)} best PDF(s):")
            for i, pdf in enumerate(best_pdfs, 1):
                print(f"    {i}. Score {pdf['score']}: {pdf['url'][:80]}...")
        
        return [pdf['url'] for pdf in best_pdfs]
        
    except Exception as e:
        print(f"  Error searching: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """Main function to process books 21-50 and open PDFs."""
    script_dir = Path(__file__).parent
    ranked_file = script_dir / 'Ranked_Library_Waves.md'
    
    if not ranked_file.exists():
        print(f"Error: {ranked_file} not found!")
        return
    
    # Extract books 21-50
    books = extract_books_21_50(ranked_file)
    print(f"Found {len(books)} books (21-50)\n")
    
    if not books:
        print("No books found! Check the file format.")
        return
    
    opened_count = 0
    
    # Process each book
    for i, book in enumerate(books, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(books)}] Book #{book['number']}: {book['title']} — {book['author']}")
        print(f"{'='*80}")
        
        # Find best PDF links (checks up to 10 results, opens up to 3 best)
        pdf_urls = find_best_pdf_links(book['search_query'], max_results_to_check=10, max_pdfs_to_open=3)
        
        # Create DuckDuckGo search URL
        search_url = f"https://duckduckgo.com/?q={quote_plus(book['search_query'])}"
        
        # Open search results page first
        print(f"\n  Opening search results page...")
        webbrowser.open(search_url)
        time.sleep(1.0)  # Delay before opening PDFs
        
        # Open PDF links (up to 3 best ones)
        for j, pdf_url in enumerate(pdf_urls, 1):
            print(f"  Opening PDF {j}/{len(pdf_urls)}...")
            webbrowser.open(pdf_url)
            time.sleep(0.6)  # Small delay between PDF tabs
        
        if pdf_urls:
            opened_count += len(pdf_urls)
        
        # Delay between books to avoid rate limiting
        # Longer delay every 5 books
        if i % 5 == 0:
            delay = 7
            print(f"\n  ⏳ Extended delay: {delay} seconds...")
        else:
            delay = 4
            print(f"\n  ⏳ Waiting {delay} seconds before next book...")
        
        time.sleep(delay)
    
    print(f"\n{'='*80}")
    print(f"Done! Processed {len(books)} books.")
    print(f"Opened {opened_count} PDF links total.")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
