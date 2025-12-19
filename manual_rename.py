"""
Manually rename remaining unmatched PDFs
"""

import re
from pathlib import Path

# Manual mappings for unmatched PDFs
MANUAL_MAPPINGS = {
    # Game Theory & Strategy
    "thetangledweb_ebook.pdf": ("The Tangled Web", "Michal Zalewski"),
    "GT_book.pdf": ("A Course in Game Theory", "Martin J. Osborne & Ariel Rubinstein"),
    "GameTheory.pdf": ("Game Theory", "Various"),
    "theoryofgames.pdf": ("Theory of Games and Economic Behavior", "John von Neumann & Oskar Morgenstern"),
    "Boyd PDF.pdf": ("Boyd: The Fighter Pilot Who Changed the Art of War", "Robert Coram"),
    "OsborneRubinsteinMasterpiece.pdf": ("A Course in Game Theory", "Martin J. Osborne & Ariel Rubinstein"),
    "ArtOfWar.pdf": ("The Art of War", "Sun Tzu"),
    
    # Tech/Engineering
    "Metasploit PDF.pdf": ("Metasploit: The Penetration Tester's Guide", "David Kennedy et al."),
    "postgresql internals- - part en.pdf": ("PostgreSQL Internals", "Egor Rogov"),
    "SpringSecurityinAction_ch1.pdf": ("Spring Security in Action", "Laurentiu Spilca"),
    "CleanCode.pdf": ("Clean Code", "Robert C. Martin"),
    "pragmatic_programmer_ch4.pdf": ("The Pragmatic Programmer", "Andrew Hunt & David Thomas"),
    "Distributed_Systems_3-200225.pdf": ("Distributed Systems", "Tanenbaum & van Steen"),
    "Scott Meyers-Effective - Modern C++-.pdf": ("Effective Modern C++", "Scott Meyers"),
    "Sources of Power- How People Make Decisions - Gary A. Klein.pdf": ("Sources of Power", "Gary A. Klein"),
    
    # Philosophy/Stoicism
    "epictetus_discourse.pdf": ("Discourses", "Epictetus"),
    "Notes_Underground_1108.pdf": ("Notes from Underground", "Fyodor Dostoevsky"),
    
    # Economics
    "Great_Transformation.pdf": ("The Great Transformation", "Karl Polanyi"),
    "schumpeter.pdf": ("Capitalism, Socialism and Democracy", "Joseph Schumpeter"),
    "H2707_manifest.pdf": ("The Communist Manifesto", "Karl Marx & Friedrich Engels"),
    
    # Other
    "Evans03.pdf": ("Domain-Driven Design", "Eric Evans"),
    "Taleb Nassim - Fooled - by Randomness.pdf": ("Fooled by Randomness", "Nassim Nicholas Taleb"),
    "Serious Cryptography - Jean-Philippe Aumasson.pdf": ("Serious Cryptography", "Jean-Philippe Aumasson"),
    "Game-Changer - David McAdams.pdf": ("Game-Changer", "David McAdams"),
    "Rock, Paper, Scissors- Game Theory in Everyday Life - Len Fisher.pdf": ("Rock, Paper, Scissors", "Len Fisher"),
    "MongoDB- The Definitive Guide - Kristina Chodorow.pdf": ("MongoDB: The Definitive Guide", "Kristina Chodorow"),
    "Building Event-Driven Microservices - Adam Bellemare.pdf": ("Building Event-Driven Microservices", "Adam Bellemare"),
    "Co-Opetition - Adam Brandenburger & Barry Nalebuff.pdf": ("Co-Opetition", "Adam Brandenburger & Barry Nalebuff"),
    "Pre-Suasion - Robert Cialdini.pdf": ("Pre-Suasion", "Robert Cialdini"),
    "Noise- A Flaw in Human Judgment - Daniel Kahneman, Olivier Sibony, Cass R. Sunstein.pdf": ("Noise: A Flaw in Human Judgment", "Daniel Kahneman, Olivier Sibony, Cass R. Sunstein"),
    "Pre-Suasion - Robert Cialdini (1).pdf": ("Pre-Suasion", "Robert Cialdini"),
    
    # Papers/Non-books (skip these)
    # "mat.pdf": None,  # Unknown
    # "WM-8-CVCOW.pdf": None,  # Paper code
    # "36735535.pdf": None,  # ISBN/code
    # "bca-honors-curriculum-and-syllabus-2024.pdf": None,  # Curriculum
    # "MiningPrograms.pdf": None,  # Unknown
    # "mintest.pdf": None,  # Unknown
    # "resume.pdf": None,  # Resume
    # "Coords_JEBO2009.pdf": None,  # Journal paper
    # "AD1160094.pdf": None,  # Code
    # "5db48c35efecc.pdf": None,  # Code
    # "9780735619678.pdf": None,  # ISBN
    # "9780201485677.pdf": None,  # ISBN
    # "preview-9781449332501_A24027703.pdf": None,  # Preview
    # "0133390098.pdf": None,  # ISBN
    # "OSS2017_BPF_superpowers.pdf": None,  # Conference paper
}


def sanitize_filename(filename):
    """Remove invalid characters for Windows filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    filename = filename.strip(' .')
    filename = re.sub(r'-+', '-', filename)
    return filename


def main():
    """Rename files manually."""
    script_dir = Path(__file__).parent
    pdf_dir = script_dir / 'pdf'
    
    print("="*80)
    print("Manual PDF Renamer")
    print("="*80)
    print()
    
    renamed = 0
    skipped = 0
    
    for old_name, book_info in MANUAL_MAPPINGS.items():
        if book_info is None:
            continue
            
        title, author = book_info
        old_path = pdf_dir / old_name
        
        if not old_path.exists():
            print(f"SKIP: {old_name} (not found)")
            continue
        
        # Sanitize
        title = sanitize_filename(title)
        author = sanitize_filename(author)
        
        # Generate new name
        new_name = f"{title} - {author}.pdf"
        new_path = pdf_dir / new_name
        
        # Handle duplicates
        counter = 1
        original_new_path = new_path
        while new_path.exists() and new_path != old_path:
            stem = original_new_path.stem
            new_path = pdf_dir / f"{stem} ({counter}).pdf"
            counter += 1
        
        # Skip if already correctly named
        if new_path == old_path:
            print(f"SKIP: {old_name} (already correct)")
            continue
        
        try:
            old_path.rename(new_path)
            print(f"OK: {old_name}")
            print(f"  -> {new_path.name}")
            renamed += 1
        except Exception as e:
            print(f"ERROR renaming {old_name}: {e}")
            skipped += 1
    
    print()
    print("="*80)
    print(f"Renamed: {renamed} files")
    print(f"Errors: {skipped} files")
    print("="*80)


if __name__ == '__main__':
    main()


