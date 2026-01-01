"""Quick test of wave parser"""
import sys
sys.path.insert(0, '.')
from utils.wave_parser import parse_wave_list, group_by_wave

# Test with actual content from Ranked_Library_Waves.md
test_text = """# Ranked Download Plan — The Library (Global Rank + Wave)
Legend: (W1)=Wave 1 (largest, escape velocity + worldview OS), (W2)=Wave 2 (expansion), (W3)=Wave 3 (deep/primary/reference), (W4)=Wave 4 (long tail).
Each line is globally ranked. Wave 1 is intentionally oversized.

0001. (W1) The 48 Laws of Power — Robert Greene
0002. (W1) The Art of Seduction — Robert Greene
0003. (W1) The 33 Strategies of War — Robert Greene
0004. (W1) Mastery — Robert Greene
0005. (W1) The Daily Laws — Robert Greene
0021. ✅ (W1) Fooled by Randomness — Nassim Nicholas Taleb
0022. ✅ (W1) Antifragile — Nassim Nicholas Taleb
"""

print("Testing wave parser...")
print(f"Input text ({len(test_text)} chars):")
print(test_text[:200])
print("...")

books = parse_wave_list(test_text)
print(f"\nParsed {len(books)} books:")
for book in books:
    print(f"  {book['number']}. ({book['wave']}) {book['title']} — {book['author']}")

waves = group_by_wave(books)
print(f"\nGrouped by wave:")
for wave, wave_books in waves.items():
    print(f"  {wave}: {len(wave_books)} books")








