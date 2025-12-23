"""
Download Manager
Handles PDF downloads with queue, progress tracking, and error handling
"""

import requests
from pathlib import Path
from typing import List, Dict, Optional
import time
import threading
from urllib.parse import urlparse


class DownloadManager:
    """Manages PDF downloads"""
    
    def __init__(self, download_directory: str):
        self.download_directory = Path(download_directory)
        self.download_directory.mkdir(parents=True, exist_ok=True)
        self.download_queue = []
        self.active_downloads = {}
        self.completed_downloads = []
        self.failed_downloads = []
    
    def queue_downloads(self, pdf_urls: List[str], book_ids: List[str] = None):
        """Queue PDFs for download"""
        for i, url in enumerate(pdf_urls):
            book_id = book_ids[i] if book_ids and i < len(book_ids) else None
            self.download_queue.append({
                'url': url,
                'book_id': book_id,
                'status': 'queued',
                'progress': 0
            })
        
        # Start download thread if not already running
        if not hasattr(self, '_download_thread') or not self._download_thread.is_alive():
            self._download_thread = threading.Thread(target=self._process_queue, daemon=True)
            self._download_thread.start()
    
    def _process_queue(self):
        """Process download queue"""
        while self.download_queue:
            item = self.download_queue.pop(0)
            self._download_pdf(item)
    
    def _download_pdf(self, item: Dict):
        """Download a single PDF"""
        url = item['url']
        book_id = item.get('book_id')
        
        download_id = str(int(time.time() * 1000))
        self.active_downloads[download_id] = {
            'url': url,
            'book_id': book_id,
            'status': 'downloading',
            'progress': 0
        }
        
        try:
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name or 'download.pdf'
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Headers to look like a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/pdf,*/*',
            }
            
            # Download file
            response = requests.get(url, stream=True, timeout=60, headers=headers)
            response.raise_for_status()
            
            # Save to download directory
            file_path = self.download_directory / filename
            total_size = int(response.headers.get('content-length', 0))
            
            with open(file_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.active_downloads[download_id]['progress'] = progress
            
            # Mark as complete
            self.active_downloads[download_id]['status'] = 'completed'
            self.active_downloads[download_id]['file_path'] = str(file_path)
            self.completed_downloads.append(self.active_downloads.pop(download_id))
            
        except Exception as e:
            # Mark as failed
            self.active_downloads[download_id]['status'] = 'failed'
            self.active_downloads[download_id]['error'] = str(e)
            self.failed_downloads.append(self.active_downloads.pop(download_id))
    
    def get_queue_status(self) -> Dict:
        """Get current download queue status"""
        return {
            'queued': len(self.download_queue),
            'active_downloads': list(self.active_downloads.values()),
            'completed': len(self.completed_downloads),
            'failed': len(self.failed_downloads)
        }




