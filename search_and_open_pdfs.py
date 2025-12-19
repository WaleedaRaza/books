"""
Script to search for PDF documents and open the first PDF result for each search term.
Reads search terms from Newbooks.txt (lines 1-22) and opens PDFs in the browser.
Includes delays to avoid rate limiting.
"""

import re
import time
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus
from ddgs import DDGS


def extract_search_terms(file_path):
    """Extract and clean search terms from lines 1-22 of the file."""
    search_terms = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Process lines 1-22 (index 0-21)
    for i, line in enumerate(lines[:22], start=1):
        line = line.strip()
        if not line or line.startswith('###'):
            continue
        
        # Remove "Free PDF" prefix and clean up
        cleaned = re.sub(r'^Free PDF\s*', '', line, flags=re.IGNORECASE)
        cleaned = re.sub(r'Free PDF', '', cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip()
        
        if cleaned:
            search_terms.append(cleaned)
    
    return search_terms


def is_pdf_url(url):
    """Check if URL points to a PDF file."""
    if not url:
        return False
    url_lower = url.lower()
    # Check for direct PDF links
    if url_lower.endswith('.pdf'):
        return True
    # Check for PDF in path or query params
    if '/pdf' in url_lower or 'filetype=pdf' in url_lower or 'format=pdf' in url_lower:
        return True
    # Check common PDF hosting domains
    pdf_domains = ['pdfdrive', 'libgen', 'archive.org', 'sci-hub', 'researchgate.net']
    if any(domain in url_lower for domain in pdf_domains):
        return True
    return False


def find_first_pdf_result(search_term):
    """Search for the term and return the first PDF URL found and the search query used."""
    try:
        print(f"Searching for: {search_term}")
        
        # Try multiple search strategies
        search_queries = [
            f"{search_term} pdf",
            f"{search_term} filetype:pdf",
            f'"{search_term}" pdf download',
        ]
        
        with DDGS() as ddgs:
            for query in search_queries:
                try:
                    results = list(ddgs.text(query, max_results=15))
                    
                    # Check each result
                    for result in results:
                        # Try different possible URL fields
                        url = result.get('href', '') or result.get('url', '') or result.get('link', '')
                        
                        if not url:
                            continue
                            
                        # Check if it's a PDF URL
                        if is_pdf_url(url):
                            print(f"  Found PDF: {url}")
                            return url, query
                        
                        # Also check the title/body for PDF indicators
                        title = result.get('title', '').lower()
                        body = result.get('body', '').lower()
                        if 'pdf' in title or 'pdf' in body:
                            # This might be a page that links to a PDF, try it
                            print(f"  Found potential PDF page: {url}")
                            return url, query
                    
                except Exception as e:
                    print(f"  Error with query '{query}': {e}")
                    continue
        
        print(f"  No PDF found for: {search_term}")
        return None, None
        
    except Exception as e:
        print(f"  Error searching for '{search_term}': {e}")
        import traceback
        traceback.print_exc()
        return None, None


def main():
    """Main function to process all search terms and open PDFs."""
    script_dir = Path(__file__).parent
    books_file = script_dir / 'Newbooks.txt'
    
    if not books_file.exists():
        print(f"Error: {books_file} not found!")
        return
    
    # Extract search terms
    search_terms = extract_search_terms(books_file)
    print(f"Found {len(search_terms)} search terms\n")
    
    opened_count = 0
    
    # Search for each term with delays
    for i, term in enumerate(search_terms, 1):
        print(f"[{i}/{len(search_terms)}] ", end='')
        pdf_url, search_query = find_first_pdf_result(term)
        
        if pdf_url and search_query:
            # Create DuckDuckGo search URL
            search_url = f"https://duckduckgo.com/?q={quote_plus(search_query)}"
            
            # Open search results page first
            print(f"  Opening search results: {search_url}")
            webbrowser.open(search_url)
            time.sleep(0.5)  # Small delay between tabs
            
            # Then open the PDF
            print(f"  Opening PDF: {pdf_url}")
            webbrowser.open(pdf_url)
            opened_count += 1
        else:
            # Still open search results even if no PDF found
            search_url = f"https://duckduckgo.com/?q={quote_plus(f'{term} pdf')}"
            print(f"  Opening search results (no PDF found): {search_url}")
            webbrowser.open(search_url)
        
        # Delay between searches to avoid rate limiting
        # Longer delay every 5 searches
        if i % 5 == 0:
            delay = 5
            print(f"  Waiting {delay} seconds (extended delay)...")
        else:
            delay = 2
            print(f"  Waiting {delay} seconds...")
        
        time.sleep(delay)
        print()
    
    print(f"\nDone! Opened {opened_count} PDF links (2 tabs each: search + PDF).")


if __name__ == '__main__':
    main()

