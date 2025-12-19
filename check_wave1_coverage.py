"""
Check Wave 1 PDF Coverage
Compares Wave 1 books with PDFs in the pdf folder.
"""

import re
from pathlib import Path
from difflib import SequenceMatcher


def extract_wave1_books(file_path):
    """Extract all Wave 1 books from Ranked_Library_Waves.md."""
    books = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match format: "0001. (W1) Title — Author [category]"
            match = re.match(r'(\d+)\.\s*✅?\s*\(W1\)\s*(.+?)\s*—\s*(.+?)\s*\[', line)
            if match:
                book_num = int(match.group(1))
                title = match.group(2).strip()
                author = match.group(3).strip()
                books.append({
                    'number': book_num,
                    'title': title,
                    'author': author,
                    'full_line': line.strip()
                })
    
    return books


def normalize_text(text):
    """Normalize text for comparison."""
    # Remove special chars, lowercase, remove extra spaces
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def similarity_score(str1, str2):
    """Calculate similarity between two strings."""
    return SequenceMatcher(None, normalize_text(str1), normalize_text(str2)).ratio()


def find_matching_pdf(book, pdf_files):
    """Find best matching PDF for a book."""
    book_title_norm = normalize_text(book['title'])
    book_author_norm = normalize_text(book['author'])
    
    best_match = None
    best_score = 0
    
    for pdf_file in pdf_files:
        pdf_name_norm = normalize_text(pdf_file.stem)
        
        # Check if title appears in PDF name
        title_score = similarity_score(book_title_norm, pdf_name_norm)
        
        # Check if author appears in PDF name
        author_score = similarity_score(book_author_norm, pdf_name_norm)
        
        # Combined score (title weighted more)
        combined_score = (title_score * 0.7) + (author_score * 0.3)
        
        # Bonus if both title and author keywords match
        title_words = set(book_title_norm.split())
        pdf_words = set(pdf_name_norm.split())
        if len(title_words.intersection(pdf_words)) >= 2:
            combined_score += 0.2
        
        if combined_score > best_score:
            best_score = combined_score
            best_match = pdf_file
    
    # Only return if confidence is reasonable
    if best_score >= 0.4:
        return best_match, best_score
    
    return None, 0


def main():
    """Main comparison function."""
    script_dir = Path(__file__).parent
    ranked_file = script_dir / 'Ranked_Library_Waves.md'
    pdf_dir = script_dir / 'pdf'
    
    print("="*80)
    print("Wave 1 PDF Coverage Check")
    print("="*80)
    
    # Extract Wave 1 books
    print("\nLoading Wave 1 books...")
    wave1_books = extract_wave1_books(ranked_file)
    print(f"   Found {len(wave1_books)} Wave 1 books")
    
    # Get PDF files
    print("\nScanning PDF folder...")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    # Filter out .crdownload files
    pdf_files = [f for f in pdf_files if not f.name.endswith('.crdownload')]
    print(f"   Found {len(pdf_files)} PDF files")
    
    # Match books to PDFs
    print("\nMatching books to PDFs...")
    matched = []
    unmatched = []
    
    for book in wave1_books:
        pdf_match, score = find_matching_pdf(book, pdf_files)
        if pdf_match:
            matched.append({
                'book': book,
                'pdf': pdf_match,
                'score': score
            })
        else:
            unmatched.append(book)
    
    # Sort matched by score (highest first)
    matched.sort(key=lambda x: x['score'], reverse=True)
    
    # Print results
    print("\n" + "="*80)
    print(f"RESULTS")
    print("="*80)
    print(f"\nMatched: {len(matched)}/{len(wave1_books)} books ({len(matched)/len(wave1_books)*100:.1f}%)")
    print(f"Missing: {len(unmatched)}/{len(wave1_books)} books ({len(unmatched)/len(wave1_books)*100:.1f}%)")
    
    # Show some high-confidence matches
    print(f"\nHigh-Confidence Matches (sample):")
    for match in matched[:10]:
        book = match['book']
        pdf = match['pdf']
        score = match['score']
        print(f"   [{book['number']:04d}] {book['title'][:50]:50s} -> {pdf.name[:50]}")
        print(f"        Score: {score:.2f}")
    
    # Show unmatched books
    if unmatched:
        print(f"\nMissing PDFs ({len(unmatched)} books):")
        for book in unmatched:  # Show all
            print(f"   [{book['number']:04d}] {book['title']} -- {book['author']}")
    
    # Summary by category (if we can extract it)
    print("\n" + "="*80)
    print("Next Steps:")
    print("   - Review unmatched books above")
    print("   - Some PDFs might have different filenames")
    print("   - Manual review recommended for accuracy")
    print("="*80)


if __name__ == '__main__':
    main()

