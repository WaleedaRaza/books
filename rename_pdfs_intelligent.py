"""
Intelligent PDF Renamer
Uses knowledge + parsing to rename PDFs to consistent format: "Title - Author.pdf"
Intelligence-first approach: tries knowledge base matching, falls back to parsing if needed.
"""

import re
from pathlib import Path
from difflib import SequenceMatcher

# Try to import comprehensive database, fall back to minimal if not available
try:
    from book_database_generated import BOOK_DATABASE
    print("Loaded comprehensive book database")
except ImportError:
    print("Warning: Could not load comprehensive database, using minimal fallback")
    # Minimal fallback database
BOOK_DATABASE = {
    # Robert Greene
    "48 laws": {"title": "The 48 Laws of Power", "author": "Robert Greene"},
    "art of seduction": {"title": "The Art of Seduction", "author": "Robert Greene"},
    "33 strategies": {"title": "The 33 Strategies of War", "author": "Robert Greene"},
    "mastery": {"title": "Mastery", "author": "Robert Greene"},
    "daily laws": {"title": "The Daily Laws", "author": "Robert Greene"},
    "laws of human nature": {"title": "Laws of Human Nature", "author": "Robert Greene"},
    
    # Taleb
    "fooled by randomness": {"title": "Fooled by Randomness", "author": "Nassim Nicholas Taleb"},
    "antifragile": {"title": "Antifragile", "author": "Nassim Nicholas Taleb"},
    "skin in the game": {"title": "Skin in the Game", "author": "Nassim Nicholas Taleb"},
    "black swan": {"title": "The Black Swan", "author": "Nassim Nicholas Taleb"},
    
    # Classics
    "prince": {"title": "The Prince", "author": "Niccolò Machiavelli"},
    "art of war": {"title": "The Art of War", "author": "Sun Tzu"},
    "book of five rings": {"title": "The Book of Five Rings", "author": "Miyamoto Musashi"},
    "hagakure": {"title": "Hagakure", "author": "Yamamoto Tsunetomo"},
    
    # Stoicism
    "meditations": {"title": "Meditations", "author": "Marcus Aurelius"},
    "enchiridion": {"title": "Enchiridion", "author": "Epictetus"},
    "discourses": {"title": "Discourses", "author": "Epictetus"},
    "letters from a stoic": {"title": "Letters from a Stoic", "author": "Seneca"},
    "on the shortness of life": {"title": "On the Shortness of Life", "author": "Seneca"},
    
    # Buddhism
    "zen mind": {"title": "Zen Mind, Beginner's Mind", "author": "Shunryu Suzuki"},
    "miracle of mindfulness": {"title": "The Miracle of Mindfulness", "author": "Thich Nhat Hanh"},
    "what the buddha taught": {"title": "What the Buddha Taught", "author": "Walpola Rahula"},
    "dhammapada": {"title": "Dhammapada", "author": "Various"},
    "why buddhism is true": {"title": "Why Buddhism is True", "author": "Robert Wright"},
    
    # Russian Literature
    "crime and punishment": {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
    "brothers karamazov": {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky"},
    "notes from underground": {"title": "Notes from Underground", "author": "Fyodor Dostoevsky"},
    
    # Economics
    "basic economics": {"title": "Basic Economics", "author": "Thomas Sowell"},
    "capitalism and freedom": {"title": "Capitalism and Freedom", "author": "Milton Friedman"},
    "road to serfdom": {"title": "The Road to Serfdom", "author": "F.A. Hayek"},
    "capital": {"title": "Capital", "author": "Karl Marx"},
    "communist manifesto": {"title": "The Communist Manifesto", "author": "Karl Marx & Friedrich Engels"},
    "debt": {"title": "Debt: The First 5,000 Years", "author": "David Graeber"},
    "great transformation": {"title": "The Great Transformation", "author": "Karl Polanyi"},
    "capitalism socialism and democracy": {"title": "Capitalism, Socialism and Democracy", "author": "Joseph Schumpeter"},
    
    # Psychology/Self-help
    "atomic habits": {"title": "Atomic Habits", "author": "James Clear"},
    "deep work": {"title": "Deep Work", "author": "Cal Newport"},
    "getting things done": {"title": "Getting Things Done", "author": "David Allen"},
    "four thousand weeks": {"title": "Four Thousand Weeks", "author": "Oliver Burkeman"},
    "indistractable": {"title": "Indistractable", "author": "Nir Eyal"},
    "ultralearning": {"title": "Ultralearning", "author": "Scott Young"},
    "war of art": {"title": "War of Art", "author": "Steven Pressfield"},
    
    # Influence/Persuasion
    "influence": {"title": "Influence", "author": "Robert Cialdini"},
    "pre-suasion": {"title": "Pre-Suasion", "author": "Robert Cialdini"},
    
    # Psychology
    "behave": {"title": "Behave", "author": "Robert Sapolsky"},
    "righteous mind": {"title": "The Righteous Mind", "author": "Jonathan Haidt"},
    "happiness hypothesis": {"title": "The Happiness Hypothesis", "author": "Jonathan Haidt"},
    "superforecasting": {"title": "Superforecasting", "author": "Philip Tetlock & Dan Gardner"},
    "noise": {"title": "Noise: A Flaw in Human Judgment", "author": "Daniel Kahneman, Olivier Sibony, Cass R. Sunstein"},
    "scout mindset": {"title": "The Scout Mindset", "author": "Julia Galef"},
    "elephant in the brain": {"title": "The Elephant in the Brain", "author": "Kevin Simler & Robin Hanson"},
    "how the mind works": {"title": "How the Mind Works", "author": "Steven Pinker"},
    "sources of power": {"title": "Sources of Power", "author": "Gary A. Klein"},
    
    # Strategy/Game Theory
    "strategy of conflict": {"title": "The Strategy of Conflict", "author": "Thomas Schelling"},
    "prisoner's dilemma": {"title": "The Prisoner's Dilemma", "author": "William Poundstone"},
    "co-opetition": {"title": "Co-Opetition", "author": "Adam Brandenburger & Barry Nalebuff"},
    "games and decisions": {"title": "Games and Decisions", "author": "R. Duncan Luce & Howard Raiffa"},
    "micromotives and macrobehavior": {"title": "Micromotives and Macrobehavior", "author": "Thomas Schelling"},
    "evolution of cooperation": {"title": "The Evolution of Cooperation", "author": "Robert Axelrod"},
    "theory of games and economic behavior": {"title": "Theory of Games and Economic Behavior", "author": "John von Neumann & Oskar Morgenstern"},
    "game theory": {"title": "Game Theory", "author": "Various"},  # Generic
    "behavioral game theory": {"title": "Behavioral Game Theory", "author": "Colin Camerer"},
    "evolutionary game theory": {"title": "Evolutionary Game Theory", "author": "Jörgen Weibull"},
    
    # Tech/Engineering
    "code complete": {"title": "Code Complete", "author": "Steve McConnell"},
    "clean code": {"title": "Clean Code", "author": "Robert C. Martin"},
    "clean architecture": {"title": "Clean Architecture", "author": "Robert C. Martin"},
    "refactoring": {"title": "Refactoring", "author": "Martin Fowler"},
    "pragmatic programmer": {"title": "The Pragmatic Programmer", "author": "Andrew Hunt & David Thomas"},
    "designing data-intensive applications": {"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"},
    "site reliability engineering": {"title": "Site Reliability Engineering", "author": "Google"},
    "phoenix project": {"title": "The Phoenix Project", "author": "Gene Kim et al."},
    "continuous delivery": {"title": "Continuous Delivery", "author": "Jez Humble & David Farley"},
    "database internals": {"title": "Database Internals", "author": "Alex Petrov"},
    "high performance mysql": {"title": "High Performance MySQL", "author": "Baron Schwartz et al."},
    "postgresql": {"title": "PostgreSQL: Up & Running", "author": "Regina Obe & Leo Hsu"},
    "redis in action": {"title": "Redis in Action", "author": "Josiah L. Carlson"},
    "computer systems": {"title": "Computer Systems: A Programmer's Perspective", "author": "Randal E. Bryant & David R. O'Hallaron"},
    "systems performance": {"title": "Systems Performance", "author": "Brendan Gregg"},
    "bpf performance tools": {"title": "BPF Performance Tools", "author": "Brendan Gregg"},
    "computer networking": {"title": "Computer Networking: A Top-Down Approach", "author": "Kurose & Ross"},
    
    # Biographies
    "steve jobs": {"title": "Steve Jobs", "author": "Walter Isaacson"},
    "shoe dog": {"title": "Shoe Dog", "author": "Phil Knight"},
    "elon musk": {"title": "Elon Musk", "author": "Walter Isaacson"},
    "bad blood": {"title": "Bad Blood", "author": "John Carreyrou"},
    "creativity inc": {"title": "Creativity, Inc.", "author": "Ed Catmull"},
    
    # Business
    "high output management": {"title": "High Output Management", "author": "Andrew S. Grove"},
    "effective executive": {"title": "The Effective Executive", "author": "Peter Drucker"},
    "good strategy bad strategy": {"title": "Good Strategy Bad Strategy", "author": "Richard Rumelt"},
    "competitive strategy": {"title": "Competitive Strategy", "author": "Michael E. Porter"},
    
    # Security/Crypto
    "applied cryptography": {"title": "Applied Cryptography", "author": "Bruce Schneier"},
    "serious cryptography": {"title": "Serious Cryptography", "author": "Jean-Philippe Aumasson"},
    "cryptography engineering": {"title": "Cryptography Engineering", "author": "Niels Ferguson, Bruce Schneier, Tadayoshi Kohno"},
    "security engineering": {"title": "Security Engineering", "author": "Ross Anderson"},
    "web application hacker": {"title": "The Web Application Hacker's Handbook", "author": "Stuttard & Pinto"},
    
    # Distributed Systems
    "understanding distributed systems": {"title": "Understanding Distributed Systems", "author": "Roberto Vitillo"},
    "designing distributed systems": {"title": "Designing Distributed Systems", "author": "Brendan Burns"},
    "seven databases": {"title": "Seven Databases in Seven Weeks", "author": "Eric Redmond & Jim R. Wilson"},
    "sql performance explained": {"title": "SQL Performance Explained", "author": "Markus Winand"},
    
    # Strategy/Military
    "strategy": {"title": "Strategy", "author": "B.H. Liddell Hart"},
    "on war": {"title": "On War", "author": "Carl von Clausewitz"},
    "makers of modern strategy": {"title": "Makers of Modern Strategy", "author": "Peter Paret"},
    "grand strategy of the byzantine empire": {"title": "The Grand Strategy of the Byzantine Empire", "author": "Edward N. Luttwak"},
    "peloponnesian war": {"title": "The Peloponnesian War", "author": "Thucydides"},
    "strategy logic of war and peace": {"title": "Strategy: The Logic of War and Peace", "author": "Edward Luttwak"},
    "36 stratagems": {"title": "The 36 Stratagems", "author": "Anonymous"},
    "boyd": {"title": "Boyd: The Fighter Pilot Who Changed the Art of War", "author": "Robert Coram"},
    
    # More
    "rock paper scissors": {"title": "Rock, Paper, Scissors: Game Theory in Everyday Life", "author": "Len Fisher"},
    "game changer": {"title": "Game-Changer", "author": "David McAdams"},
    "game theory at work": {"title": "Game Theory at Work", "author": "James D. Miller"},
    "the art of strategy": {"title": "The Art of Strategy", "author": "Avinash Dixit & Barry Nalebuff"},
    "science of strategy": {"title": "The Science of Strategy", "author": "Avinash Dixit"},
}


def parse_title_author_from_filename(filename):
    """
    Parse title and author from filename when intelligence fails.
    Handles common patterns like:
    - "Title - Author.pdf"
    - "Title — Author.pdf" (em dash)
    - "Title by Author.pdf"
    - "Author - Title.pdf"
    - "Title PDF.pdf" (try to extract from existing PDF names)
    """
    stem = Path(filename).stem
    
    # Pattern 1: "Title - Author" or "Title — Author"
    match = re.match(r'^(.+?)\s+[-—–]\s+(.+)$', stem)
    if match:
        title = match.group(1).strip()
        author = match.group(2).strip()
        # Heuristic: if title is shorter than author, might be reversed
        if len(title.split()) < len(author.split()) and len(author.split()) > 2:
            # Likely reversed, swap them
            title, author = author, title
        return {"title": title, "author": author}
    
    # Pattern 2: "Title by Author"
    match = re.match(r'^(.+?)\s+by\s+(.+)$', stem, re.IGNORECASE)
    if match:
        return {"title": match.group(1).strip(), "author": match.group(2).strip()}
    
    # Pattern 3: Remove common suffixes and try to split
    cleaned = re.sub(r'\s*(PDF|pdf|ebook|e-book|edition|ed\.?|vol\.?|volume)\s*$', '', stem, flags=re.IGNORECASE)
    
    # Try splitting on common separators
    for sep in [' - ', ' — ', ' – ', ' by ', ' BY ']:
        if sep in cleaned:
            parts = cleaned.split(sep, 1)
            if len(parts) == 2:
                title = parts[0].strip()
                author = parts[1].strip()
                # Heuristic: if title is shorter than author, might be reversed
                if len(title.split()) < len(author.split()) and len(author.split()) > 2:
                    title, author = author, title
                return {"title": title, "author": author}
    
    # Pattern 4: If filename already looks like "Title Author", try to split intelligently
    # Remove file extensions, numbers, etc.
    cleaned = re.sub(r'[_\d\(\)\[\]]+', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # If it's a reasonable length and has multiple words, try last 2-3 words as author
    words = cleaned.split()
    if len(words) >= 4:
        # Common pattern: last name might be author
        # Try last 2 words as author
        author = ' '.join(words[-2:])
        title = ' '.join(words[:-2])
        return {"title": title, "author": author}
    
    return None


def normalize_for_search(text):
    """Normalize text for searching."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def find_book_match(pdf_filename):
    """
    Find matching book from database using intelligence.
    Returns (match_dict, score) where match_dict has 'title' and 'author'.
    Score >= 0.7 means good match, < 0.7 means fall back to parsing.
    """
    pdf_norm = normalize_for_search(pdf_filename)
    
    best_match = None
    best_score = 0
    
    # Strategy 1: Exact key match (highest confidence)
    if pdf_norm in BOOK_DATABASE:
        return BOOK_DATABASE[pdf_norm], 1.0
    
    # Strategy 2: Key substring match
    for key, book_info in BOOK_DATABASE.items():
        key_norm = normalize_for_search(key)
        title_norm = normalize_for_search(book_info['title'])
        author_norm = normalize_for_search(book_info['author'])
        
        # Check if key is contained in filename
        if key_norm in pdf_norm and len(key_norm) > 3:
            score = 0.9
            # Boost if full title also matches
            if title_norm in pdf_norm:
                score = 1.0
            if score > best_score:
                best_match = book_info
                best_score = score
                continue
        
        # Strategy 3: Title word overlap (intelligent matching)
        title_words = set(title_norm.split())
        pdf_words = set(pdf_norm.split())
        
        # Remove very common words
        common_words = {'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'and', 'or', 'pdf', 'book'}
        title_words = title_words - common_words
        pdf_words = pdf_words - common_words
        
        if len(title_words) == 0:
            continue
            
        title_match = len(title_words.intersection(pdf_words))
        
        # Require at least 2 significant words to match (or 1 if title is short)
        min_match = 2 if len(title_words) > 3 else 1
        
        if title_match >= min_match:
            # Calculate score based on overlap ratio
            overlap_ratio = title_match / len(title_words)
            score = 0.6 + (overlap_ratio * 0.3)  # 0.6 to 0.9 range
            
            # Boost if author matches
            author_words = set(author_norm.split()) - common_words
            if len(author_words) > 0:
            author_match = len(author_words.intersection(pdf_words))
            if author_match > 0:
                score += 0.1
                    # Extra boost if multiple author words match
                    if author_match >= 2:
                        score += 0.05
            
            # Boost if key words appear in order
            title_list = [w for w in title_norm.split() if w not in common_words]
            pdf_list = [w for w in pdf_norm.split() if w not in common_words]
            if len(title_list) >= 2:
                # Check if first 2-3 words of title appear consecutively in PDF
                for i in range(len(pdf_list) - len(title_list) + 1):
                    if pdf_list[i:i+min(3, len(title_list))] == title_list[:min(3, len(title_list))]:
                        score += 0.05
                        break
            
            if score > best_score:
                best_match = book_info
                best_score = score
    
    return best_match, best_score


def sanitize_filename(filename):
    """Remove invalid characters for Windows filenames."""
    # Windows invalid characters: < > : " / \ | ? *
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    # Remove leading/trailing spaces and dots (Windows doesn't allow these)
    filename = filename.strip(' .')
    # Replace multiple dashes with single dash
    filename = re.sub(r'-+', '-', filename)
    return filename


def rename_pdf(pdf_file, dry_run=False):
    """
    Rename PDF to consistent format: "Title - Author.pdf"
    Uses intelligence first, falls back to parsing if needed.
    """
    # Try intelligence-based matching first
    match, score = find_book_match(pdf_file.stem)
    
    # If intelligence match is good (score >= 0.7), use it
    if match and score >= 0.7:
        title = match['title']
        author = match['author']
        source = "intelligence"
    else:
        # Fall back to parsing
        parsed = parse_title_author_from_filename(pdf_file.name)
        if parsed:
            title = parsed['title']
            author = parsed['author']
            source = "parsing"
            score = 0.5  # Lower confidence for parsed matches
        else:
            # Can't match or parse, skip this file
            return False
    
    # Sanitize title and author for Windows filenames
    title = sanitize_filename(title)
    author = sanitize_filename(author)
    
    # Generate consistent filename: "Title - Author.pdf"
    new_name = f"{title} - {author}.pdf"
        new_path = pdf_file.parent / new_name
        
        # Handle duplicates
        counter = 1
        original_new_path = new_path
        while new_path.exists() and new_path != pdf_file:
            stem = original_new_path.stem
            new_path = pdf_file.parent / f"{stem} ({counter}).pdf"
            counter += 1
        
    # Skip if already correctly named
    if new_path == pdf_file:
        return True
    
        if dry_run:
            print(f"Would rename: {pdf_file.name}")
            print(f"           -> {new_path.name}")
        print(f"           Method: {source}, Score: {score:.2f}\n")
        else:
            pdf_file.rename(new_path)
        print(f"Renamed: {pdf_file.name} -> {new_path.name} ({source})")
        
        return True


def main():
    """Main function."""
    script_dir = Path(__file__).parent
    pdf_dir = script_dir / 'pdf'
    
    print("="*80)
    print("Intelligent PDF Renamer")
    print("="*80)
    print("\nThis will rename PDFs to consistent format: 'Title - Author.pdf'")
    print("Uses intelligence-first matching, falls back to parsing when needed.\n")
    print(f"Loaded {len(BOOK_DATABASE)} search keys from database\n")
    
    pdf_files = [f for f in pdf_dir.glob("*.pdf") if not f.name.endswith('.crdownload')]
    
    renamed = 0
    not_matched = []
    
    for pdf_file in pdf_files:
        if rename_pdf(pdf_file, dry_run=False):  # ACTUALLY RENAME FILES
            renamed += 1
        else:
            not_matched.append(pdf_file.name)
    
    print("="*80)
    print(f"Summary: {renamed}/{len(pdf_files)} PDFs renamed")
    print(f"Not matched: {len(not_matched)} PDFs")
    
    if not_matched:
        print(f"\nUnmatched PDFs (first 20):")
        for name in not_matched[:20]:
            print(f"  - {name}")
    
    print("\n" + "="*80)
    print("DONE - Files have been renamed to consistent format: 'Title - Author.pdf'")
    print("="*80)


if __name__ == '__main__':
    main()

