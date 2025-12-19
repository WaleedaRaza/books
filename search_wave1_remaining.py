"""
Enhanced POC script for BookPDFOpener - Finishes Wave 1 (books 101-220)
Searches for "[title] [author] free pdf online" and intelligently finds actual PDF files.
Prioritizes direct PDF links, filters paywalls/404s, logs all opened links for pattern analysis.

This is the POC version that will be converted to a LangChain/Vercel webapp.
"""

import re
import time
import json
import webbrowser
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus, urlparse
from ddgs import DDGS


class BookPDFOpener:
    """Main class for finding and opening book PDFs - designed for webapp conversion."""
    
    def __init__(self, log_file="opened_links_log.json"):
        self.log_file = Path(log_file)
        self.session_log = {
            'session_start': datetime.now().isoformat(),
            'books_processed': [],
            'links_opened': []
        }
        self._load_existing_log()
    
    def _load_existing_log(self):
        """Load existing log if it exists."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.session_log = json.load(f)
            except:
                pass
    
    def _save_log(self):
        """Save current session log to file."""
        self.session_log['session_end'] = datetime.now().isoformat()
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_log, f, indent=2, ensure_ascii=False)
    
    def _log_link(self, book_number, book_title, link_type, url, score=None, reason=None):
        """Log a link that was opened."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'book_number': book_number,
            'book_title': book_title,
            'link_type': link_type,  # 'search' or 'pdf'
            'url': url,
            'score': score,
            'reason': reason
        }
        self.session_log['links_opened'].append(entry)
        self._save_log()
    
    def _log_book(self, book_number, title, author, pdfs_found, pdfs_opened):
        """Log book processing results."""
        entry = {
            'book_number': book_number,
            'title': title,
            'author': author,
            'pdfs_found': pdfs_found,
            'pdfs_opened': pdfs_opened,
            'timestamp': datetime.now().isoformat()
        }
        self.session_log['books_processed'].append(entry)
    
    @staticmethod
    def is_bad_domain(url):
        """Check if URL is from a domain we want to avoid."""
        if not url:
            return True
        
        url_lower = url.lower()
        bad_domains = [
            'amazon.com', 'amazon.co.uk', 'amazon.ca', 'amazon.',
            'goodreads.com',
            'wikipedia.org', 'wiki',
            'reddit.com', 'redd.it',
            'quora.com',
            'youtube.com', 'youtu.be',
            'facebook.com', 'fb.com',
            'twitter.com', 'x.com',
            'linkedin.com',
            'pinterest.com',
            'instagram.com',
            'paywall', 'subscription', 'signup', 'register', 'login',
            '404', 'error', 'notfound', 'page-not-found',
            'adf.ly', 'bit.ly', 'tinyurl.com', 't.co',  # URL shorteners
            'spam', 'malware', 'virus', 'phishing',
            'bookstore', 'buy', 'purchase', 'shop',
            'review', 'summary', 'synopsis',  # Not actual books
        ]
        
        return any(bad in url_lower for bad in bad_domains)
    
    @staticmethod
    def is_good_pdf_domain(url):
        """Check if URL is from a known good PDF hosting domain."""
        if not url:
            return False
        
        url_lower = url.lower()
        good_domains = [
            'archive.org',  # Internet Archive - best source
            'libgen', 'library genesis',
            'pdfdrive', 'pdf drive',
            'sci-hub',
            'researchgate.net',
            'academia.edu',
            'arxiv.org',
            'googleusercontent.com',  # Google Docs/Drive PDFs
            'drive.google.com',
            'docs.google.com',
            'dropbox.com',
            'github.com', 'github.io',  # Sometimes has PDFs
            'edu',  # Educational institutions
            'gov',  # Government sites
            'org',  # Non-profits often host PDFs
        ]
        
        return any(good in url_lower for good in good_domains)
    
    @staticmethod
    def score_pdf_url(url, title, body):
        """Score a URL based on how likely it is to be an actual viewable PDF.
        Higher score = better. Returns (score, reason, confidence)."""
        if not url:
            return (0, "No URL", "low")
        
        url_lower = url.lower()
        title_lower = title.lower() if title else ""
        body_lower = body.lower() if body else ""
        
        score = 0
        reasons = []
        confidence = "low"
        
        # CRITICAL: Direct PDF file (highest priority)
        if url_lower.endswith('.pdf'):
            score += 200  # Massive boost for direct PDFs
            reasons.append("Direct PDF file (.pdf)")
            confidence = "high"
        
        # HIGH: PDF in URL path/params
        if '/pdf' in url_lower or 'filetype=pdf' in url_lower or 'format=pdf' in url_lower:
            score += 120
            reasons.append("PDF in URL path/params")
            confidence = "medium-high"
        
        # HIGH: Known good PDF hosting domains
        if BookPDFOpener.is_good_pdf_domain(url):
            score += 80
            reasons.append("Known PDF hosting domain")
            confidence = "medium-high"
        
        # CRITICAL: Bad domains get heavily penalized
        if BookPDFOpener.is_bad_domain(url):
            score -= 500  # Heavy penalty
            reasons.append("BLOCKED: Paywall/sketchy domain")
            return (score, ", ".join(reasons), "none")
        
        # MEDIUM: Title/body indicators
        if 'pdf' in title_lower or 'pdf' in body_lower:
            score += 40
            reasons.append("PDF mentioned")
        
        if 'download' in title_lower and 'pdf' in title_lower:
            score += 30
            reasons.append("Download PDF in title")
        
        if 'free' in title_lower and 'pdf' in title_lower:
            score += 20
            reasons.append("Free PDF in title")
        
        # MEDIUM: Archive.org specific patterns (very reliable)
        if 'archive.org' in url_lower:
            score += 60
            reasons.append("Internet Archive (highly reliable)")
            confidence = "high"
        
        # LOW: Avoid listing/search pages
        if any(word in url_lower for word in ['/search', '/results', '/list', '/index', '?q=']):
            score -= 15
            reasons.append("Likely listing page")
        
        # LOW: Prefer shorter URLs (often more direct)
        if len(url) < 80:
            score += 10
            reasons.append("Short URL (likely direct)")
        
        # BONUS: Common PDF file patterns
        if any(pattern in url_lower for pattern in ['/download/', '/file/', '/document/', '/book/']):
            score += 15
            reasons.append("PDF file path pattern")
        
        # Determine confidence
        if score >= 150:
            confidence = "high"
        elif score >= 80:
            confidence = "medium"
        elif score >= 30:
            confidence = "low-medium"
        
        return (score, ", ".join(reasons) if reasons else "Generic link", confidence)
    
    def find_best_pdf_links(self, search_query, max_results_to_check=15, max_pdfs_to_open=3):
        """Search and intelligently find the best PDF links.
        Checks up to max_results_to_check results, returns up to max_pdfs_to_open best ones."""
        candidates = []
        
        try:
            print(f"  🔍 Searching: {search_query}")
            
            # Try multiple search strategies (prioritize filetype first)
            search_variants = [
                f"{search_query} filetype:pdf",  # Most specific
                f'"{search_query}" filetype:pdf',  # Quoted + filetype
                search_query,  # General search
                f'"{search_query}" pdf download',  # Quoted + download
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
                            if BookPDFOpener.is_bad_domain(url):
                                continue
                            
                            title = result.get('title', '')
                            body = result.get('body', '')
                            
                            # Score this URL
                            score, reason, confidence = BookPDFOpener.score_pdf_url(url, title, body)
                            
                            # Only consider if score is positive (not heavily penalized)
                            if score > -100:
                                candidates.append({
                                    'url': url,
                                    'score': score,
                                    'reason': reason,
                                    'confidence': confidence,
                                    'title': title
                                })
                                print(f"    [{score:4d}] [{confidence:12s}] {url[:65]}...")
                        
                    except Exception as e:
                        print(f"    ⚠ Error with variant '{variant}': {e}")
                        continue
            
            # Sort by score (highest first), then by confidence
            candidates.sort(key=lambda x: (x['score'], x['confidence'] == 'high'), reverse=True)
            
            # Take top max_pdfs_to_open
            best_pdfs = candidates[:max_pdfs_to_open]
            
            if not best_pdfs:
                print(f"  ❌ No good PDFs found")
            else:
                print(f"\n  ✅ Selected {len(best_pdfs)} best PDF(s):")
                for i, pdf in enumerate(best_pdfs, 1):
                    print(f"    {i}. Score {pdf['score']} [{pdf['confidence']}]: {pdf['url'][:75]}...")
            
            return best_pdfs
            
        except Exception as e:
            print(f"  ❌ Error searching: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def extract_books_101_220(self, file_path):
        """Extract books 101-220 (remaining Wave 1) from Ranked_Library_Waves.md."""
        books = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Book 1 is at line 5 (index 4), so book 101 is at line 105 (index 104)
        # Books 101-220 are at indices 104-223 (120 books)
        for i, line in enumerate(lines[104:224], start=101):
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            
            # Parse format: "0051. (W1) Title — Author [category]"
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
    
    def process_books(self, books, delay_between_books=4, extended_delay=7):
        """Process a list of books and open PDFs."""
        opened_count = 0
        
        for i, book in enumerate(books, 1):
            print(f"\n{'='*90}")
            print(f"[{i}/{len(books)}] Book #{book['number']}: {book['title']} — {book['author']}")
            print(f"{'='*90}")
            
            # Find best PDF links
            pdf_candidates = self.find_best_pdf_links(
                book['search_query'], 
                max_results_to_check=15, 
                max_pdfs_to_open=3
            )
            
            # Create DuckDuckGo search URL
            search_url = f"https://duckduckgo.com/?q={quote_plus(book['search_query'])}"
            
            # Open search results page first
            print(f"\n  🌐 Opening search results page...")
            webbrowser.open(search_url)
            self._log_link(book['number'], book['title'], 'search', search_url)
            time.sleep(1.2)  # Delay before opening PDFs
            
            # Open PDF links (up to 3 best ones)
            pdfs_opened = []
            for j, pdf_info in enumerate(pdf_candidates, 1):
                pdf_url = pdf_info['url']
                print(f"  📄 Opening PDF {j}/{len(pdf_candidates)}...")
                webbrowser.open(pdf_url)
                self._log_link(
                    book['number'], 
                    book['title'], 
                    'pdf', 
                    pdf_url,
                    score=pdf_info['score'],
                    reason=pdf_info['reason']
                )
                pdfs_opened.append(pdf_url)
                time.sleep(0.7)  # Small delay between PDF tabs
            
            # Log book processing
            self._log_book(
                book['number'],
                book['title'],
                book['author'],
                len(pdf_candidates),
                len(pdfs_opened)
            )
            
            if pdfs_opened:
                opened_count += len(pdfs_opened)
            
            # Delay between books
            if i % 5 == 0:
                delay = extended_delay
                print(f"\n  ⏳ Extended delay: {delay} seconds...")
            else:
                delay = delay_between_books
                print(f"\n  ⏳ Waiting {delay} seconds before next book...")
            
            time.sleep(delay)
        
        return opened_count


def main():
    """Main function - POC for BookPDFOpener webapp."""
    script_dir = Path(__file__).parent
    ranked_file = script_dir / 'Ranked_Library_Waves.md'
    log_file = script_dir / 'opened_links_log.json'
    
    if not ranked_file.exists():
        print(f"❌ Error: {ranked_file} not found!")
        return
    
    # Initialize opener
    opener = BookPDFOpener(log_file=str(log_file))
    
    print("="*90)
    print("BookPDFOpener POC - Finishing Wave 1 (Books 101-220)")
    print("="*90)
    print(f"📝 Logging to: {log_file}")
    print()
    
    # Extract books 101-220
    books = opener.extract_books_101_220(ranked_file)
    print(f"📚 Found {len(books)} books (101-220) to process\n")
    
    if not books:
        print("❌ No books found! Check the file format.")
        return
    
    # Process all books
    opened_count = opener.process_books(books, delay_between_books=4, extended_delay=7)
    
    # Final summary
    print(f"\n{'='*90}")
    print(f"✅ Done! Processed {len(books)} books.")
    print(f"📄 Opened {opened_count} PDF links total.")
    print(f"📝 Full log saved to: {log_file}")
    print(f"{'='*90}")
    
    # Show log summary
    print(f"\n📊 Session Summary:")
    print(f"   - Books processed: {len(opener.session_log['books_processed'])}")
    print(f"   - Total links opened: {len(opener.session_log['links_opened'])}")
    print(f"   - Search pages: {sum(1 for link in opener.session_log['links_opened'] if link['link_type'] == 'search')}")
    print(f"   - PDF links: {sum(1 for link in opener.session_log['links_opened'] if link['link_type'] == 'pdf')}")


if __name__ == '__main__':
    main()

