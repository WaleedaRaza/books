"""
PDF Discovery Engine
Searches for PDFs using DuckDuckGo and other sources
"""

import time
import re
from typing import List, Dict, Optional
from ddgs import DDGS
from urllib.parse import quote_plus


class PDFDiscoveryEngine:
    """Discovers PDF links for books"""
    
    def __init__(self, db=None):
        self.ddgs = DDGS()
        self.rate_limit_delay = 2.0
        self.extended_delay_interval = 5
        self.discovery_sessions = {}  # Track active discovery sessions
        self.db = db  # Database instance
    
    @staticmethod
    def is_bad_domain(url: str) -> bool:
        """Check if URL is from a domain we want to avoid"""
        if not url:
            return True
        
        url_lower = url.lower()
        bad_domains = [
            'amazon.com', 'amazon.co.uk', 'amazon.ca',
            'goodreads.com', 'wikipedia.org', 'reddit.com',
            'quora.com', 'youtube.com', 'facebook.com',
            'twitter.com', 'linkedin.com', 'pinterest.com',
            'paywall', 'subscription', 'signup', 'register',
            '404', 'error', 'notfound', 'bookstore', 'buy',
            'purchase', 'shop', 'review', 'summary'
        ]
        
        return any(bad in url_lower for bad in bad_domains)
    
    @staticmethod
    def is_good_pdf_domain(url: str) -> bool:
        """Check if URL is from a known good PDF hosting domain"""
        if not url:
            return False
        
        url_lower = url.lower()
        good_domains = [
            'archive.org', 'libgen', 'pdfdrive', 'sci-hub',
            'researchgate.net', 'academia.edu', 'arxiv.org',
            'googleusercontent.com', 'drive.google.com',
            'docs.google.com', 'dropbox.com', 'github.com'
        ]
        
        return any(good in url_lower for good in good_domains)
    
    def score_pdf_url(self, url: str, title: str = '', body: str = '') -> tuple:
        """Score a URL based on how likely it is to be an actual PDF"""
        if not url:
            return (0, "No URL", "low")
        
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
        
        # Bad domains
        if self.is_bad_domain(url):
            score -= 500
            reasons.append("BLOCKED: Paywall/sketchy domain")
            return (score, ", ".join(reasons), "none")
        
        # Archive.org specific
        if 'archive.org' in url_lower:
            score += 60
            reasons.append("Internet Archive")
            confidence = "high"
        
        # PDF mentioned
        if 'pdf' in title_lower or 'pdf' in body_lower:
            score += 40
            reasons.append("PDF mentioned")
        
        # Determine confidence
        if score >= 150:
            confidence = "high"
        elif score >= 80:
            confidence = "medium"
        elif score >= 30:
            confidence = "low-medium"
        
        return (score, ", ".join(reasons) if reasons else "Generic link", confidence)
    
    def search_for_book(self, title: str, author: str, max_results: int = 10) -> List[Dict]:
        """Search for PDFs of a specific book"""
        query = f"{title} {author} free pdf"
        
        try:
            results = self.ddgs.text(query, max_results=max_results)
            
            scored_results = []
            for result in results:
                url = result.get('href', '')
                result_title = result.get('title', '')
                body = result.get('body', '')
                
                score, reason, confidence = self.score_pdf_url(url, result_title, body)
                
                if score > 0:  # Only include positive scores
                    scored_results.append({
                        'url': url,
                        'title': result_title,
                        'body': body,
                        'score': score,
                        'reason': reason,
                        'confidence': confidence,
                        'source': self._extract_source(url)
                    })
            
            # Sort by score descending
            scored_results.sort(key=lambda x: x['score'], reverse=True)
            
            return scored_results[:5]  # Top 5
            
        except Exception as e:
            print(f"Error searching for {title}: {e}")
            return []
    
    def _extract_source(self, url: str) -> str:
        """Extract source name from URL"""
        url_lower = url.lower()
        
        if 'archive.org' in url_lower:
            return 'archive.org'
        elif 'libgen' in url_lower:
            return 'libgen'
        elif 'pdfdrive' in url_lower:
            return 'pdfdrive'
        elif url_lower.endswith('.pdf'):
            return 'direct'
        else:
            return 'other'
    
    def start_discovery(self, book_ids: List[str], db_instance=None):
        """Start discovery process for a list of books"""
        if db_instance:
            self.db = db_instance
        
        session_id = str(int(time.time()))
        self.discovery_sessions[session_id] = {
            'book_ids': book_ids,
            'current_index': 0,
            'results': {},
            'complete': False,
            'started_at': time.time()
        }
        
        # Start discovery in background thread
        import threading
        thread = threading.Thread(target=self._discover_books, args=(session_id,), daemon=True)
        thread.start()
        
        return session_id
    
    def _discover_books(self, session_id: str):
        """Background discovery process"""
        session = self.discovery_sessions[session_id]
        book_ids = session['book_ids']
        
        for i, book_id in enumerate(book_ids):
            if not self.db:
                continue
                
            book = self.db.get_book(book_id)
            if not book:
                continue
            
            session['current_index'] = i
            session['current'] = book['title']
            
            # Search for PDFs
            pdf_results = self.search_for_book(book['title'], book['author'])
            
            # Store results in database
            for result in pdf_results:
                self.db.add_pdf_link(
                    book_id=book_id,
                    url=result['url'],
                    source=result['source'],
                    confidence=0.8 if result['confidence'] == 'high' else 0.5,
                    score=result['score']
                )
            
            # Update book status
            if pdf_results:
                self.db.update_book(book_id, status='FOUND')
            else:
                self.db.update_book(book_id, status='NOT_FOUND')
            
            # Rate limiting
            if (i + 1) % self.extended_delay_interval == 0:
                time.sleep(self.rate_limit_delay * 2)
            else:
                time.sleep(self.rate_limit_delay)
        
        session['complete'] = True
    
    def get_progress(self, book_ids: List[str] = None) -> Dict:
        """Get discovery progress"""
        if not book_ids:
            # Get latest session
            if not self.discovery_sessions:
                return {'total': 0, 'completed': 0, 'current': None, 'complete': True}
            session = list(self.discovery_sessions.values())[-1]
        else:
            # Find session with matching book_ids
            session = None
            for s in self.discovery_sessions.values():
                if s['book_ids'] == book_ids:
                    session = s
                    break
            
            if not session:
                return {'total': len(book_ids), 'completed': 0, 'current': None, 'complete': False}
        
        total = len(session['book_ids'])
        completed = session['current_index'] + (1 if session['complete'] else 0)
        
        return {
            'total': total,
            'completed': completed,
            'current': session.get('current'),
            'complete': session['complete']
        }

