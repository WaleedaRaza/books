"""
Build comprehensive book database from categorized_books.md
Extracts all books and creates a knowledge base for intelligent matching.
"""

import re
from pathlib import Path


def extract_books_from_categorized():
    """Extract all books from categorized_books.md."""
    books = {}
    script_dir = Path(__file__).parent
    file_path = script_dir / 'categorized_books.md'
    
    # Try different encodings (including UTF-16)
    encodings = ['utf-16-le', 'utf-16', 'utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    content = None
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.readlines()
            # Remove BOM if present
            if content and content[0].startswith('\ufeff'):
                content[0] = content[0][1:]
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if content is None:
        raise ValueError(f"Could not decode {file_path} with any encoding")
    
    for line in content:
            line = line.strip()
            # Match format: "- Title — Author" (using em dash, en dash, or regular dash)
            # Try em dash (—), en dash (–), or regular dash (-)
            match = re.match(r'^-\s+(.+?)\s+[—–-]\s+(.+)$', line)
            if match:
                title = match.group(1).strip()
                author = match.group(2).strip()
                
                # Create search keys from title
                title_lower = title.lower()
                # Remove common prefixes
                title_clean = re.sub(r'^(the|a|an)\s+', '', title_lower)
                
                # Create multiple keys for better matching
                keys = []
                
                # Key 1: Full normalized title
                keys.append(re.sub(r'[^\w\s]', ' ', title_lower))
                
                # Key 2: Title without "The/A/An"
                if title_clean != title_lower:
                    keys.append(re.sub(r'[^\w\s]', ' ', title_clean))
                
                # Key 3: First few significant words
                words = [w for w in re.sub(r'[^\w\s]', ' ', title_lower).split() if len(w) > 2]
                if len(words) >= 2:
                    keys.append(' '.join(words[:3]))  # First 3 significant words
                if len(words) >= 4:
                    keys.append(' '.join(words[:4]))  # First 4 significant words
                
                # Key 4: Acronym or short form if applicable
                if '(' in title and ')' in title:
                    # Extract edition info like "(2e)" but also look for acronyms
                    pass
                
                # Store book info
                book_info = {
                    'title': title,
                    'author': author
                }
                
                # Add all keys pointing to this book
                for key in keys:
                    key_norm = re.sub(r'\s+', ' ', key).strip()
                    if key_norm and len(key_norm) > 2:
                        # If key already exists, prefer longer/more specific title
                        if key_norm not in books or len(title) > len(books[key_norm]['title']):
                            books[key_norm] = book_info
    
    return books


def generate_python_database(books):
    """Generate Python code for BOOK_DATABASE."""
    lines = ['BOOK_DATABASE = {']
    
    # Sort by title for readability
    sorted_items = sorted(books.items(), key=lambda x: x[1]['title'].lower())
    
    current_title = None
    for key, book_info in sorted_items:
        title = book_info['title']
        author = book_info['author']
        
        # Group by title (show only once per title)
        if title != current_title:
            if current_title is not None:
                lines.append('')
            # Add comment with title
            title_comment = title.replace('"', '\\"')
            lines.append(f'    # {title_comment}')
            current_title = title
        
        # Escape quotes in strings
        key_escaped = key.replace('"', '\\"')
        title_escaped = title.replace('"', '\\"')
        author_escaped = author.replace('"', '\\"')
        
        lines.append(f'    "{key_escaped}": {{"title": "{title_escaped}", "author": "{author_escaped}"}},')
    
    lines.append('}')
    return '\n'.join(lines)


def main():
    """Main function."""
    print("Extracting books from categorized_books.md...")
    books = extract_books_from_categorized()
    
    print(f"Extracted {len(set(b['title'] for b in books.values()))} unique books")
    print(f"Generated {len(books)} search keys")
    
    # Save to file
    script_dir = Path(__file__).parent
    output_file = script_dir / 'book_database_generated.py'
    
    db_code = generate_python_database(books)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('"""\n')
        f.write('Auto-generated book database from categorized_books.md\n')
        f.write('Generated by build_book_database.py\n')
        f.write('"""\n\n')
        f.write(db_code)
        f.write('\n')
    
    print(f"\nDatabase saved to: {output_file}")
    print("\nSample entries:")
    sample_items = list(books.items())[:10]
    for key, book_info in sample_items:
        print(f"  '{key}' -> {book_info['title']} — {book_info['author']}")


if __name__ == '__main__':
    main()


