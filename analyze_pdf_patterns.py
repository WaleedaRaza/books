"""
Analysis script for opened_links_log.json
Helps identify patterns in which PDFs actually worked vs didn't.
Use this to refine the PDF detection algorithm.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from urllib.parse import urlparse


def analyze_log(log_file="opened_links_log.json"):
    """Analyze the log file to find patterns."""
    log_path = Path(log_file)
    
    if not log_path.exists():
        print(f"❌ Log file not found: {log_file}")
        return
    
    with open(log_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pdf_links = [link for link in data['links_opened'] if link['link_type'] == 'pdf']
    search_links = [link for link in data['links_opened'] if link['link_type'] == 'search']
    
    print("="*90)
    print("PDF Pattern Analysis")
    print("="*90)
    print(f"\n📊 Overview:")
    print(f"   - Total books processed: {len(data['books_processed'])}")
    print(f"   - Total PDF links opened: {len(pdf_links)}")
    print(f"   - Total search pages opened: {len(search_links)}")
    
    # Domain analysis
    print(f"\n🌐 Top Domains (PDF links):")
    domains = Counter()
    for link in pdf_links:
        try:
            domain = urlparse(link['url']).netloc
            domains[domain] += 1
        except:
            pass
    
    for domain, count in domains.most_common(15):
        print(f"   {domain:40s} : {count:3d} links")
    
    # Score distribution
    print(f"\n📈 Score Distribution:")
    scores = [link['score'] for link in pdf_links if link.get('score')]
    if scores:
        print(f"   - Average score: {sum(scores)/len(scores):.1f}")
        print(f"   - Min score: {min(scores)}")
        print(f"   - Max score: {max(scores)}")
        print(f"   - Scores >= 150 (high confidence): {sum(1 for s in scores if s >= 150)}")
        print(f"   - Scores >= 80 (medium-high): {sum(1 for s in scores if s >= 80)}")
        print(f"   - Scores < 80 (low-medium): {sum(1 for s in scores if s < 80)}")
    
    # Domain patterns
    print(f"\n✅ High-Scoring Domains (likely good sources):")
    high_score_domains = defaultdict(list)
    for link in pdf_links:
        if link.get('score', 0) >= 150:
            try:
                domain = urlparse(link['url']).netloc
                high_score_domains[domain].append(link['score'])
            except:
                pass
    
    for domain, scores_list in sorted(high_score_domains.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        avg_score = sum(scores_list) / len(scores_list)
        print(f"   {domain:40s} : {len(scores_list):3d} links, avg score {avg_score:.1f}")
    
    # Export CSV for manual review
    csv_file = log_path.with_suffix('.csv')
    print(f"\n💾 Exporting to CSV: {csv_file}")
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("Book Number,Title,Author,Link Type,URL,Score,Reason\n")
        for link in data['links_opened']:
            book_num = link.get('book_number', '')
            book_title = link.get('book_title', '').replace(',', ';')
            link_type = link.get('link_type', '')
            url = link.get('url', '').replace(',', ';')
            score = link.get('score', '')
            reason = link.get('reason', '').replace(',', ';')
            f.write(f"{book_num},{book_title},{link_type},{url},{score},{reason}\n")
    
    print(f"\n✅ Analysis complete! Review {csv_file} to manually mark which PDFs actually worked.")


if __name__ == '__main__':
    analyze_log()



