import PyPDF2
import re
import json
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except:
        return ""

reports_dir = Path('financial_reports')

# Priority documents to analyze
priority_docs = [
    'Q1_FY2026 Earnings Call Transcript.pdf',
    'Q4_FY2025 Earnings Call Transcript.pdf',
    'Q4_FY2025 10K.pdf',
    'Q1 FY2026 Earnings Release Deck.pdf',
    'Q4 FY2025 Earnings Release Deck.pdf',
]

print("Extracting key information from financial reports...")
print("=" * 80)

all_data = {}

for doc in priority_docs:
    doc_path = reports_dir / doc
    if doc_path.exists():
        print(f"\nProcessing: {doc}")
        text = extract_text_from_pdf(doc_path)
        all_data[doc] = text
        print(f"  ✓ Extracted {len(text)} characters")

# Save extracted text for analysis
with open('extracted_reports.json', 'w') as f:
    json.dump(all_data, f)

print("\n" + "=" * 80)
print("Extraction complete. Analyzing content...")
print("=" * 80)

# Analyze for segments
segments_data = {
    'olive_garden': [],
    'longhorn': [],
    'fine_dining': [],
    'other': [],
    'competitors': [],
    'growth_drivers': [],
    'future_plans': [],
    'risks': []
}

for doc_name, text in all_data.items():
    text_lower = text.lower()
    
    # Olive Garden mentions
    if 'olive garden' in text_lower:
        matches = re.finditer(r'([^.]*olive garden[^.]*\.)', text, re.IGNORECASE)
        for match in list(matches)[:10]:
            segments_data['olive_garden'].append(f"[{doc_name}] {match.group(1).strip()}")
    
    # LongHorn mentions
    if 'longhorn' in text_lower:
        matches = re.finditer(r'([^.]*longhorn[^.]*\.)', text, re.IGNORECASE)
        for match in list(matches)[:10]:
            segments_data['longhorn'].append(f"[{doc_name}] {match.group(1).strip()}")
    
    # Fine dining mentions
    if any(x in text_lower for x in ['capital grille', 'eddie v', 'ruth', 'seasons 52']):
        matches = re.finditer(r'([^.]*(?:capital grille|eddie v|ruth|seasons 52)[^.]*\.)', text, re.IGNORECASE)
        for match in list(matches)[:10]:
            segments_data['fine_dining'].append(f"[{doc_name}] {match.group(1).strip()}")
    
    # Competitor mentions
    if any(x in text_lower for x in ['texas roadhouse', 'bloomin', 'brinker', 'competitor', 'competition']):
        matches = re.finditer(r'([^.]*(?:texas roadhouse|bloomin|brinker|competitor|competition)[^.]*\.)', text, re.IGNORECASE)
        for match in list(matches)[:8]:
            segments_data['competitors'].append(f"[{doc_name}] {match.group(1).strip()}")
    
    # Growth drivers
    if any(x in text_lower for x in ['same-store sales', 'pricing', 'traffic', 'new restaurant']):
        matches = re.finditer(r'([^.]*(?:same-store sales|pricing|traffic|new restaurant)[^.]*\.)', text, re.IGNORECASE)
        for match in list(matches)[:8]:
            segments_data['growth_drivers'].append(f"[{doc_name}] {match.group(1).strip()}")
    
    # Future plans
    if any(x in text_lower for x in ['guidance', 'expect', 'plan to', 'will open', 'strategy']):
        matches = re.finditer(r'([^.]*(?:guidance|expect|plan to|will open|strategy)[^.]*\.)', text, re.IGNORECASE)
        for match in list(matches)[:8]:
            segments_data['future_plans'].append(f"[{doc_name}] {match.group(1).strip()}")

# Save analysis
with open('segments_analysis.json', 'w') as f:
    json.dump(segments_data, f, indent=2)

print("\n✓ Segments analysis saved to segments_analysis.json")
print(f"  - Olive Garden mentions: {len(segments_data['olive_garden'])}")
print(f"  - LongHorn mentions: {len(segments_data['longhorn'])}")
print(f"  - Fine Dining mentions: {len(segments_data['fine_dining'])}")
print(f"  - Competitor mentions: {len(segments_data['competitors'])}")
print(f"  - Growth driver mentions: {len(segments_data['growth_drivers'])}")
print(f"  - Future plans mentions: {len(segments_data['future_plans'])}")
