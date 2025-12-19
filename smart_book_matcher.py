"""
Smart Book Matcher - Uses intelligence/knowledge to match PDFs to books
Falls back to parsing only when needed.
"""

import re
from pathlib import Path
from difflib import SequenceMatcher


# Knowledge base of book title variations and common patterns
BOOK_KNOWLEDGE = {
    # Robert Greene books
    "daily laws": ["The Daily Laws", "Daily Laws"],
    "laws of human nature": ["Laws of Human Nature", "The Laws of Human Nature"],
    
    # Taleb books
    "fooled by randomness": ["Fooled by Randomness", "Fooled by Randomness: The Hidden Role of Chance"],
    "antifragile": ["Antifragile", "Antifragile: Things That Gain from Disorder"],
    "skin in the game": ["Skin in the Game", "Skin in the Game: Hidden Asymmetries in Daily Life"],
    "black swan": ["The Black Swan", "Black Swan"],
    
    # Classics
    "prince": ["The Prince", "Prince"],
    "meditations": ["Meditations", "Meditations of Marcus Aurelius"],
    "art of war": ["The Art of War", "Art of War"],
    "book of five rings": ["The Book of Five Rings", "Book of Five Rings"],
    "hagakure": ["Hagakure", "Hagakure: The Book of the Samurai"],
    
    # Stoicism
    "enchiridion": ["Enchiridion", "The Enchiridion"],
    "discourses": ["Discourses", "The Discourses"],
    "letters from a stoic": ["Letters from a Stoic", "Letters from a Stoic: Epistulae Morales ad Lucilium"],
    "on the shortness of life": ["On the Shortness of Life", "De Brevitate Vitae"],
    
    # Buddhism
    "zen mind beginner's mind": ["Zen Mind, Beginner's Mind", "Zen Mind Beginner's Mind"],
    "miracle of mindfulness": ["The Miracle of Mindfulness", "Miracle of Mindfulness"],
    "what the buddha taught": ["What the Buddha Taught", "What Buddha Taught"],
    "dhammapada": ["Dhammapada", "The Dhammapada"],
    
    # Russian literature
    "crime and punishment": ["Crime and Punishment", "Crime & Punishment"],
    "brothers karamazov": ["The Brothers Karamazov", "Brothers Karamazov"],
    "notes from underground": ["Notes from Underground", "Notes from the Underground"],
    
    # Economics
    "basic economics": ["Basic Economics", "Basic Economics: A Common Sense Guide to the Economy"],
    "capitalism and freedom": ["Capitalism and Freedom", "Capitalism & Freedom"],
    "road to serfdom": ["The Road to Serfdom", "Road to Serfdom"],
    "capital": ["Capital", "Das Kapital", "Capital: A Critique of Political Economy"],
    "communist manifesto": ["The Communist Manifesto", "Communist Manifesto"],
    
    # Psychology/Self-help
    "atomic habits": ["Atomic Habits", "Atomic Habits: An Easy & Proven Way to Build Good Habits"],
    "deep work": ["Deep Work", "Deep Work: Rules for Focused Success"],
    "getting things done": ["Getting Things Done", "GTD"],
    "influence": ["Influence", "Influence: The Psychology of Persuasion"],
    "pre-suasion": ["Pre-Suasion", "Pre-Suasion: A Revolutionary Way to Influence and Persuade"],
    
    # Strategy/Game Theory
    "strategy of conflict": ["The Strategy of Conflict", "Strategy of Conflict"],
    "prisoner's dilemma": ["The Prisoner's Dilemma", "Prisoner's Dilemma"],
    "co-opetition": ["Co-Opetition", "Co-opetition"],
    "games and decisions": ["Games and Decisions", "Games and Decisions: Introduction and Critical Survey"],
    
    # Tech/Engineering
    "code complete": ["Code Complete", "Code Complete: A Practical Handbook of Software Construction"],
    "clean code": ["Clean Code", "Clean Code: A Handbook of Agile Software Craftsmanship"],
    "pragmatic programmer": ["The Pragmatic Programmer", "Pragmatic Programmer"],
    "designing data-intensive applications": ["Designing Data-Intensive Applications", "DDIA"],
    "site reliability engineering": ["Site Reliability Engineering", "SRE", "Google SRE"],
    
    # Biographies
    "steve jobs": ["Steve Jobs", "Steve Jobs: The Exclusive Biography"],
    "shoe dog": ["Shoe Dog", "Shoe Dog: A Memoir by the Creator of Nike"],
    "elon musk": ["Elon Musk", "Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future"],
    
    # Other notable books
    "behave": ["Behave", "Behave: The Biology of Humans at Our Best and Worst"],
    "righteous mind": ["The Righteous Mind", "Righteous Mind"],
    "happiness hypothesis": ["The Happiness Hypothesis", "Happiness Hypothesis"],
    "superforecasting": ["Superforecasting", "Superforecasting: The Art and Science of Prediction"],
    "noise": ["Noise", "Noise: A Flaw in Human Judgment"],
    "scout mindset": ["The Scout Mindset", "Scout Mindset"],
    "elephant in the brain": ["The Elephant in the Brain", "Elephant in the Brain"],
    "how the mind works": ["How the Mind Works", "How The Mind Works"],
    "sources of power": ["Sources of Power", "Sources of Power: How People Make Decisions"],
}


def normalize_for_matching(text):
    """Normalize text for intelligent matching."""
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove common PDF artifacts
    text = re.sub(r'\s*\(pdf\)\s*', ' ', text)
    text = re.sub(r'\s*pdf\s*$', '', text)
    text = re.sub(r'^pdf\s*', '', text)
    
    # Remove edition markers but keep them for context
    text = re.sub(r'\s*\(2e\)\s*', ' ', text)
    text = re.sub(r'\s*2nd\s+edition\s*', ' ', text)
    text = re.sub(r'\s*second\s+edition\s*', ' ', text)
    
    # Remove common prefixes
    text = re.sub(r'^(the|a|an)\s+', '', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def extract_keywords(text):
    """Extract meaningful keywords from text."""
    normalized = normalize_for_matching(text)
    words = normalized.split()
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from'}
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return set(keywords)


def intelligent_match(book_title, book_author, pdf_filename):
    """Use knowledge base and intelligence to match books to PDFs."""
    
    # Normalize inputs
    title_norm = normalize_for_matching(book_title)
    author_norm = normalize_for_matching(book_author)
    pdf_norm = normalize_for_matching(pdf_filename)
    
    # Check knowledge base first
    for key, variations in BOOK_KNOWLEDGE.items():
        if key in title_norm:
            # Check if any variation matches PDF
            for variation in variations:
                var_norm = normalize_for_matching(variation)
                if var_norm in pdf_norm or pdf_norm in var_norm:
                    return True, 0.95, f"Knowledge base match: {variation}"
    
    # Extract keywords (more flexible)
    title_keywords = extract_keywords(book_title)
    author_keywords = extract_keywords(book_author)
    pdf_keywords = extract_keywords(pdf_filename)
    
    # Check if significant title keywords appear in PDF
    title_match_count = len(title_keywords.intersection(pdf_keywords))
    title_match_ratio = title_match_count / max(len(title_keywords), 1)
    
    # Check if author keywords appear
    author_match_count = len(author_keywords.intersection(pdf_keywords))
    author_match_ratio = author_match_count / max(len(author_keywords), 1)
    
    # Calculate base score
    # Title match is more important (70%), author match (30%)
    score = (title_match_ratio * 0.7) + (author_match_ratio * 0.3)
    
    # Boost score if multiple title words match
    if title_match_count >= 2:
        score += 0.15
    if title_match_count >= 3:
        score += 0.15
    if title_match_count >= 4:
        score += 0.1
    
    # Boost if author matches (even partially)
    if author_match_ratio > 0.3:
        score += 0.1
    if author_match_ratio > 0.5:
        score += 0.15
    
    # Check for partial substring matches (more flexible)
    # If 3+ consecutive words from title appear in PDF
    title_words = title_norm.split()
    pdf_words = ' '.join(pdf_keywords)
    consecutive_matches = 0
    for i in range(len(title_words) - 2):
        phrase = ' '.join(title_words[i:i+3])
        if phrase in pdf_norm:
            consecutive_matches += 1
            score += 0.2
    
    # Check for exact substring matches (high confidence)
    if title_norm in pdf_norm or pdf_norm in title_norm:
        score = max(score, 0.9)
    
    # Check for common abbreviations/acronyms
    common_abbrevs = {
        "ddia": "designing data-intensive applications",
        "sre": "site reliability engineering",
        "gtd": "getting things done",
        "ddd": "domain-driven design",
        "sla": "service level",
    }
    for abbrev, full in common_abbrevs.items():
        if abbrev in pdf_norm and full in title_norm:
            score = max(score, 0.85)
    
    # Check for author last name match (common in PDFs)
    author_parts = author_norm.split()
    if author_parts:
        last_name = author_parts[-1]
        if last_name in pdf_norm and title_match_count >= 2:
            score += 0.15
    
    # Lower threshold for matching - be more permissive
    # But still require some title match
    if title_match_count == 0:
        score = 0  # Must have at least some title match
    
    return score >= 0.4, score, f"Title: {title_match_count}/{len(title_keywords)}, Author: {author_match_count}/{len(author_keywords)}"


def parse_book_from_line(line):
    """Parse book from ranked list line - fallback when intelligence fails."""
    # Format: "0001. (W1) Title — Author [category]"
    match = re.match(r'(\d+)\.\s*✅?\s*\(W1\)\s*(.+?)\s*—\s*(.+?)\s*\[', line)
    if match:
        return {
            'number': int(match.group(1)),
            'title': match.group(2).strip(),
            'author': match.group(3).strip(),
        }
    return None


def main():
    """Main matching function."""
    script_dir = Path(__file__).parent
    ranked_file = script_dir / 'Ranked_Library_Waves.md'
    pdf_dir = script_dir / 'pdf'
    
    print("="*80)
    print("Smart Book Matcher - Using Intelligence + Parsing")
    print("="*80)
    
    # Load Wave 1 books
    print("\nLoading Wave 1 books...")
    books = []
    with open(ranked_file, 'r', encoding='utf-8') as f:
        for line in f:
            book = parse_book_from_line(line)
            if book:
                books.append(book)
    
    print(f"   Found {len(books)} Wave 1 books")
    
    # Load PDFs
    print("\nLoading PDFs...")
    pdf_files = [f for f in pdf_dir.glob("*.pdf") if not f.name.endswith('.crdownload')]
    print(f"   Found {len(pdf_files)} PDF files")
    
    # Match using intelligence
    print("\nMatching using intelligence...")
    matched = []
    unmatched_books = []
    used_pdfs = set()
    
    for book in books:
        best_match = None
        best_score = 0
        best_reason = ""
        
        for pdf_file in pdf_files:
            if pdf_file in used_pdfs:
                continue
            
            is_match, score, reason = intelligent_match(
                book['title'],
                book['author'],
                pdf_file.stem
            )
            
            if is_match and score > best_score:
                best_match = pdf_file
                best_score = score
                best_reason = reason
        
        if best_match and best_score >= 0.4:
            matched.append({
                'book': book,
                'pdf': best_match,
                'score': best_score,
                'reason': best_reason
            })
            used_pdfs.add(best_match)
        else:
            unmatched_books.append(book)
    
    # Sort by score
    matched.sort(key=lambda x: x['score'], reverse=True)
    
    # Results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    print(f"\nMatched: {len(matched)}/{len(books)} ({len(matched)/len(books)*100:.1f}%)")
    print(f"Missing: {len(unmatched_books)}/{len(books)} ({len(unmatched_books)/len(books)*100:.1f}%)")
    
    # Show high-confidence matches
    print(f"\nHigh-Confidence Matches (score >= 0.8):")
    high_conf = [m for m in matched if m['score'] >= 0.8]
    for match in high_conf[:15]:
        book = match['book']
        pdf = match['pdf']
        score = match['score']
        print(f"   [{book['number']:04d}] {book['title'][:45]:45s} -> {pdf.name[:45]}")
        print(f"        Score: {score:.2f} | {match['reason']}")
    
    # Show unmatched
    if unmatched_books:
        print(f"\nUnmatched Books ({len(unmatched_books)}):")
        for book in unmatched_books:
            print(f"   [{book['number']:04d}] {book['title']} -- {book['author']}")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    main()

