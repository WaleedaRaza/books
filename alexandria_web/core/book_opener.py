"""
BookPDFOpener - Integrated from search_wave1_remaining.py
This is the PROVEN working code for finding PDFs.
"""

import re
import time
import json
import webbrowser
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus, urlparse
from ddgs import DDGS
import requests


class BookPDFOpener:
    """Main class for finding and opening book PDFs - integrated from proven scripts."""
    
    def __init__(self, log_file="opened_links_log.json"):
        self.log_file = Path(log_file)
        self.session_log = {
            'session_start': datetime.now().isoformat(),
            'books_processed': [],
            'links_opened': []
        }
        self._load_existing_log()
        self.callbacks = {
            'on_search_start': None,
            'on_link_found': None,
            'on_book_complete': None,
            'on_error': None
        }
    
    def set_callback(self, event, callback):
        """Set callback for real-time UI updates"""
        if event in self.callbacks:
            self.callbacks[event] = callback
    
    def _emit(self, event, data):
        """Emit event to callback"""
        if self.callbacks.get(event):
            self.callbacks[event](data)
    
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
            'link_type': link_type,
            'url': url,
            'score': score,
            'reason': reason
        }
        self.session_log['links_opened'].append(entry)
        self._save_log()
        return entry
    
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
        return entry
    
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
            'adf.ly', 'bit.ly', 'tinyurl.com', 't.co',
            'spam', 'malware', 'virus', 'phishing',
            'bookstore', 'buy', 'purchase', 'shop',
            'review', 'summary', 'synopsis',
        ]
        
        return any(bad in url_lower for bad in bad_domains)
    
    @staticmethod
    def is_good_pdf_domain(url):
        """Check if URL is from a known PDF-friendly source."""
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
            'googleusercontent.com',
            'drive.google.com',
            'docs.google.com',
            'dropbox.com',
            'github.com',
            'githubusercontent.com',
        ]
        
        return any(good in url_lower for good in good_domains)
    
    def is_actual_pdf(self, url):
        """Check if URL is actually a PDF file by checking headers."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/pdf,*/*',
            }
            response = requests.head(url, timeout=5, headers=headers, allow_redirects=True)
            content_type = response.headers.get('content-type', '').lower()
            
            if 'application/pdf' in content_type:
                return True
            if url.lower().endswith('.pdf'):
                return True
            return False
        except:
            return url.lower().endswith('.pdf')
    
    def score_pdf_url(self, url, title='', body=''):
        """Score a URL for how likely it is to be an actual PDF. Returns (score, reasons, confidence)."""
        if not url:
            return (0, "No URL", "none")
        
        url_lower = url.lower()
        title_lower = title.lower() if title else ""
        body_lower = body.lower() if body else ""
        
        score = 0
        reasons = []
        confidence = "low"
        
        # Direct PDF file
        if url_lower.endswith('.pdf'):
            score += 200
            reasons.append("Direct PDF file")
            confidence = "high"
        
        # PDF in URL
        if '/pdf' in url_lower or 'filetype=pdf' in url_lower:
            score += 120
            reasons.append("PDF in URL")
            confidence = "medium-high"
        
        # Good domains
        if self.is_good_pdf_domain(url):
            score += 80
            reasons.append("Known PDF hosting domain")
            confidence = "medium-high"
        
        # Bad domains = reject
        if self.is_bad_domain(url):
            score -= 500
            reasons.append("BLOCKED: Paywall/bad domain")
            return (score, ", ".join(reasons), "none")
        
        # Archive.org bonus
        if 'archive.org' in url_lower:
            score += 60
            reasons.append("Internet Archive")
            confidence = "high"
        
        # PDF mentioned in text
        if 'pdf' in title_lower or 'pdf' in body_lower:
            score += 40
            reasons.append("PDF mentioned")
        
        # Free/download mentioned
        if 'free' in title_lower or 'download' in body_lower:
            score += 20
            reasons.append("Free/download mentioned")
        
        # Update confidence
        if score >= 150:
            confidence = "high"
        elif score >= 80:
            confidence = "medium"
        elif score >= 30:
            confidence = "low-medium"
        
        return (score, ", ".join(reasons) if reasons else "Generic link", confidence)
    
    def search_for_book(self, title, author, max_results=15):
        """Search for PDFs of a specific book. Returns list of scored results."""
        query = f"{title} {author} free pdf online"
        
        self._emit('on_search_start', {
            'title': title,
            'author': author,
            'query': query
        })
        
        try:
            ddgs = DDGS()
            results = ddgs.text(query, max_results=max_results)
            
            scored_results = []
            for result in results:
                url = result.get('href', '')
                result_title = result.get('title', '')
                body = result.get('body', '')
                
                score, reason, confidence = self.score_pdf_url(url, result_title, body)
                is_pdf = self.is_actual_pdf(url) if score > 0 else False
                
                if score > 0:
                    link_data = {
                        'url': url,
                        'title': result_title,
                        'body': body,
                        'score': score,
                        'reason': reason,
                        'confidence': confidence,
                        'source': self._extract_source(url),
                        'is_pdf': is_pdf
                    }
                    scored_results.append(link_data)
                    self._emit('on_link_found', link_data)
            
            # Sort: PDF files first, then by score
            scored_results.sort(key=lambda x: (not x['is_pdf'], -x['score']))
            return scored_results[:10]
            
        except Exception as e:
            self._emit('on_error', {'error': str(e), 'book': title})
            return []
    
    def _extract_source(self, url):
        """Extract source name from URL."""
        url_lower = url.lower()
        
        if 'archive.org' in url_lower:
            return 'archive.org'
        elif 'libgen' in url_lower:
            return 'libgen'
        elif 'pdfdrive' in url_lower:
            return 'pdfdrive'
        elif 'sci-hub' in url_lower:
            return 'sci-hub'
        elif 'researchgate' in url_lower:
            return 'researchgate'
        elif 'academia.edu' in url_lower:
            return 'academia'
        elif 'arxiv.org' in url_lower:
            return 'arxiv'
        elif 'drive.google' in url_lower or 'docs.google' in url_lower:
            return 'google-drive'
        elif 'github' in url_lower:
            return 'github'
        elif url_lower.endswith('.pdf'):
            return 'direct-pdf'
        else:
            return 'other'
    
    def process_book(self, book_number, title, author, open_tabs=True, max_tabs=3):
        """Process a single book - search and optionally open tabs."""
        results = self.search_for_book(title, author)
        
        opened = 0
        for result in results[:max_tabs]:
            self._log_link(
                book_number=book_number,
                book_title=title,
                link_type='pdf' if result['is_pdf'] else 'search',
                url=result['url'],
                score=result['score'],
                reason=result['reason']
            )
            
            if open_tabs:
                webbrowser.open(result['url'])
                opened += 1
                time.sleep(0.5)  # Brief delay between tabs
        
        book_entry = self._log_book(
            book_number=book_number,
            title=title,
            author=author,
            pdfs_found=len(results),
            pdfs_opened=opened
        )
        
        self._emit('on_book_complete', {
            'book': book_entry,
            'results': results
        })
        
        return results
    
    def process_book_list(self, books, open_tabs=True, delay_between_books=2.0):
        """Process a list of books. Each book is dict with 'number', 'title', 'author'."""
        all_results = []
        
        for i, book in enumerate(books):
            results = self.process_book(
                book_number=book.get('number', i + 1),
                title=book['title'],
                author=book['author'],
                open_tabs=open_tabs
            )
            all_results.append({
                'book': book,
                'results': results
            })
            
            # Rate limiting
            if i < len(books) - 1:
                time.sleep(delay_between_books)
        
        self._save_log()
        return all_results








