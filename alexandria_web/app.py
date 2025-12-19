"""
Alexandria Library - Flask Web Application
Your PDF Book Hub - 1500+ books and growing
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from pathlib import Path
import os
import sys
import re

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import BookDatabase
from core.discovery import PDFDiscoveryEngine
from core.downloader import DownloadManager
from core.renamer import RenamingEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'alexandria-dev-secret-key')
app.config['PDF_DIRECTORY'] = os.environ.get('PDF_DIRECTORY', str(Path(__file__).parent.parent / 'pdf'))
app.config['DATABASE_PATH'] = os.environ.get('DATABASE_PATH', str(Path(__file__).parent / 'data' / 'books.db'))

# Initialize core components
db = BookDatabase(app.config['DATABASE_PATH'])
discovery = PDFDiscoveryEngine(db=db)
downloader = DownloadManager(app.config['PDF_DIRECTORY'])
renamer = RenamingEngine(app.config['PDF_DIRECTORY'])


@app.route('/')
def index():
    """Main library view"""
    search_query = request.args.get('search', '').strip()
    filter_status = request.args.get('filter', '').strip()
    sort_by = request.args.get('sort', 'title').strip()
    
    books = db.get_all_books(search=search_query, filter_status=filter_status, sort_by=sort_by)
    stats = db.get_statistics()
    
    return render_template('library.html', 
                         books=books, 
                         stats=stats,
                         search_query=search_query,
                         filter_status=filter_status,
                         sort_by=sort_by)


@app.route('/discover', methods=['GET', 'POST'])
def discover():
    """Get Books - paste list or generate one"""
    if request.method == 'POST':
        book_list_text = request.form.get('book_list', '').strip()
        if book_list_text:
            from utils.parsers import parse_book_list
            books = parse_book_list(book_list_text)
            
            # Check library first, then queue for discovery
            book_ids = []
            for book_data in books:
                # Check if we already have this book
                existing = db.search_books(book_data.get('title', ''))
                if existing:
                    book_ids.append(existing[0]['id'])
                else:
                    book_id = db.add_book(
                        title=book_data.get('title', ''),
                        author=book_data.get('author', 'Unknown'),
                        status='SEARCHING'
                    )
                    book_ids.append(book_id)
            
            session['discovery_book_ids'] = book_ids
            discovery.start_discovery(book_ids, db_instance=db)
            
            return redirect(url_for('discover_progress'))
    
    stats = db.get_statistics()
    return render_template('discover.html', stats=stats)


@app.route('/generate-list', methods=['POST'])
def generate_list():
    """Generate a book list from a prompt (placeholder for LLM)"""
    prompt = request.form.get('prompt', '').strip()
    # For now, redirect back - will implement LLM generation
    stats = db.get_statistics()
    return render_template('discover.html', stats=stats, message="List generation coming soon!")


@app.route('/discover/progress')
def discover_progress():
    """Show discovery progress"""
    book_ids = session.get('discovery_book_ids', [])
    if not book_ids:
        return redirect(url_for('discover'))
    
    progress = discovery.get_progress(book_ids)
    stats = db.get_statistics()
    
    if progress.get('complete', False):
        return redirect(url_for('discover_results'))
    
    return render_template('discover_progress.html', progress=progress, stats=stats, auto_refresh=True)


@app.route('/discover/results')
def discover_results():
    """Show discovery results"""
    book_ids = session.get('discovery_book_ids', [])
    books_with_pdfs = []
    
    for book_id in book_ids:
        book = db.get_book(book_id)
        if book:
            pdf_links = db.get_pdf_links(book_id)
            books_with_pdfs.append({
                'book': book,
                'pdf_links': pdf_links
            })
    
    stats = db.get_statistics()
    return render_template('discover_results.html', books_with_pdfs=books_with_pdfs, stats=stats)


@app.route('/download/queue', methods=['POST'])
def queue_downloads():
    """Queue selected PDFs for download"""
    selected_pdfs = request.form.getlist('pdf_urls')
    book_ids = request.form.getlist('book_ids')
    
    if selected_pdfs:
        downloader.queue_downloads(selected_pdfs, book_ids)
        return redirect(url_for('download_queue'))
    
    return redirect(url_for('discover_results'))


@app.route('/download/queue')
def download_queue():
    """Show download queue"""
    queue = downloader.get_queue_status()
    stats = db.get_statistics()
    
    if queue.get('active_downloads'):
        return render_template('download.html', queue=queue, stats=stats, auto_refresh=True)
    
    return render_template('download.html', queue=queue, stats=stats, auto_refresh=False)


@app.route('/book/<book_id>')
def view_book(book_id):
    """View book details"""
    book = db.get_book(book_id)
    if not book:
        return redirect(url_for('index'))
    
    pdf_links = db.get_pdf_links(book_id)
    stats = db.get_statistics()
    
    return render_template('book_detail.html', book=book, pdf_links=pdf_links, stats=stats)


@app.route('/reading-list')
def reading_list():
    """My reading list"""
    stats = db.get_statistics()
    return render_template('reading_list.html', reading_list=[], stats=stats)


@app.route('/api')
def api_docs():
    """API documentation page"""
    stats = db.get_statistics()
    return render_template('api.html', stats=stats)


@app.route('/api/stats')
def api_stats():
    """API: Library statistics"""
    stats = db.get_statistics()
    return jsonify(stats)


@app.route('/api/search')
def api_search():
    """API: Search books"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Missing query parameter q'}), 400
    
    books = db.get_all_books(search=query)
    return jsonify({'results': books, 'count': len(books)})


@app.route('/api/book/<book_id>')
def api_book(book_id):
    """API: Get book details"""
    book = db.get_book(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    pdf_links = db.get_pdf_links(book_id)
    return jsonify({'book': book, 'pdf_links': pdf_links})


@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    """Serve PDF files from the pdf directory"""
    return send_from_directory(app.config['PDF_DIRECTORY'], filename)


@app.route('/download-pdf/<book_id>')
def download_book_pdf(book_id):
    """Download a book's PDF"""
    book = db.get_book(book_id)
    if not book or not book.get('pdf_path'):
        return redirect(url_for('view_book', book_id=book_id))
    
    return send_from_directory(
        app.config['PDF_DIRECTORY'], 
        book['pdf_path'],
        as_attachment=True
    )


if __name__ == '__main__':
    Path(app.config['DATABASE_PATH']).parent.mkdir(parents=True, exist_ok=True)
    Path(app.config['PDF_DIRECTORY']).mkdir(parents=True, exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
