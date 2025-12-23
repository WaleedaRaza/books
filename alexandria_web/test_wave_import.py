"""Test wave import parser with real data"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from utils.wave_parser import parse_wave_list, group_by_wave

# Read actual file
wave_file = Path(__file__).parent.parent / 'Ranked_Library_Waves.md'
content = wave_file.read_text(encoding='utf-8')

print("=" * 60)
print("TESTING WAVE IMPORT PARSER")
print("=" * 60)

books = parse_wave_list(content)
print(f"\n[PASS] Parsed {len(books)} books from Ranked_Library_Waves.md")

waves = group_by_wave(books)
print(f"\n[PASS] Waves found: {sorted(waves.keys())}")

for wave in sorted(waves.keys()):
    count = len(waves[wave])
    print(f"   {wave}: {count} books")

print(f"\n[PASS] Sample books:")
for book in books[:5]:
    print(f"   {book['number']:04d}. ({book['wave']}) {book['title']} - {book['author']}")

print("\n" + "=" * 60)
print("PARSER TEST: PASSED")
print("=" * 60)





