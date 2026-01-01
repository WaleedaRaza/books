"""
Renaming Engine
Intelligently renames PDFs to consistent format
"""

from pathlib import Path
import re
from typing import Optional


def sanitize_filename(filename):
    """Remove invalid characters for Windows filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    filename = filename.strip(' .')
    filename = re.sub(r'-+', '-', filename)  # Replace multiple hyphens with single
    return filename


class RenamingEngine:
    """Manages PDF renaming"""
    
    def __init__(self, pdf_directory: str):
        self.pdf_directory = Path(pdf_directory)
    
    def rename_file(self, file_path: str, title: str, author: str) -> Optional[str]:
        """Rename a PDF file"""
        pdf_file = Path(file_path)
        if not pdf_file.exists():
            return None
        
        # Sanitize
        title_clean = sanitize_filename(title)
        author_clean = sanitize_filename(author)
        
        # Generate new name
        new_name = f"{title_clean} - {author_clean}.pdf"
        new_path = self.pdf_directory / new_name
        
        # Handle duplicates
        counter = 1
        original_new_path = new_path
        while new_path.exists() and new_path != pdf_file:
            stem = original_new_path.stem
            new_path = self.pdf_directory / f"{stem} ({counter}).pdf"
            counter += 1
        
        if new_path == pdf_file:
            return str(new_path)
        
        try:
            pdf_file.rename(new_path)
            return str(new_path)
        except Exception as e:
            print(f"Error renaming {file_path}: {e}")
            return None







