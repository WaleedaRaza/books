"""
Folder Watcher - Monitors download directory for new PDFs
Processes and renames them, then uploads to library (pending approval)
"""

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading
from typing import Optional, Callable
import shutil


class PDFWatcher(FileSystemEventHandler):
    """Watches for new PDF files in a directory"""
    
    def __init__(self, watch_directory: str, on_new_pdf: Callable, db=None, renamer=None):
        self.watch_directory = Path(watch_directory)
        self.on_new_pdf = on_new_pdf
        self.db = db
        self.renamer = renamer
        self.processed_files = set()
        self.observer = None
    
    def on_created(self, event):
        """Called when a new file is created"""
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            time.sleep(2)  # Wait for file to finish downloading
            file_path = Path(event.src_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                if str(file_path) not in self.processed_files:
                    self.processed_files.add(str(file_path))
                    self.on_new_pdf(file_path, self.db, self.renamer)
    
    def start(self):
        """Start watching the directory"""
        self.observer = Observer()
        self.observer.schedule(self, str(self.watch_directory), recursive=False)
        self.observer.start()
    
    def stop(self):
        """Stop watching"""
        if self.observer:
            self.observer.stop()
            self.observer.join()


def process_new_pdf(file_path: Path, db, renamer):
    """Process a newly downloaded PDF"""
    if not db or not renamer:
        return
    
    try:
        # Extract title/author from filename
        filename = file_path.stem
        if ' - ' in filename:
            parts = filename.split(' - ', 1)
            title = parts[0].strip()
            author = parts[1].strip() if len(parts) > 1 else 'Unknown'
        else:
            title = filename
            author = 'Unknown'
        
        # Copy file to library directory
        library_dir = Path(renamer.pdf_directory)
        library_dir.mkdir(parents=True, exist_ok=True)
        
        from core.renamer import sanitize_filename
        title_clean = sanitize_filename(title)
        author_clean = sanitize_filename(author)
        final_filename = f"{title_clean} - {author_clean}.pdf"
        library_path = library_dir / final_filename
        
        # Handle duplicates
        counter = 1
        original_library_path = library_path
        while library_path.exists():
            stem = original_library_path.stem
            library_path = library_dir / f"{stem} ({counter}).pdf"
            counter += 1
        
        # Copy file to library
        shutil.copy2(file_path, library_path)
        final_filename = library_path.name
        
        # Add to database as PENDING (needs Waleed's approval)
        book_id = db.add_book(
            title=title,
            author=author,
            status='PENDING_APPROVAL'
        )
        
        db.update_book(book_id, pdf_path=final_filename)
        
        print(f"Processed: {final_filename} - Status: PENDING_APPROVAL")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")





