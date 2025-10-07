import json
import PyPDF2
from pathlib import Path

# Load the extracted analysis
with open('segments_analysis.json', 'r') as f:
    data = json.load(f)

# Create comprehensive markdown report
report = """# COMPREHENSIVE DARDEN SEGMENTS ANALYSIS
## Extracted from Q1 FY2026 & FY2025 Financial Reports

---

## 1. OLIVE GARDEN INSIGHTS

"""

for item in data['olive_garden'][:15]:
    report += f"- {item}\n\n"

report += """
---

## 2. LONGHORN STEAKHOUSE INSIGHTS

"""

for item in data['longhorn'][:15]:
    report += f"- {item}\n\n"

report += """
---

## 3. FINE DINING SEGMENT INSIGHTS

"""

for item in data['fine_dining'][:15]:
    report += f"- {item}\n\n"

report += """
---

## 4. COMPETITOR ANALYSIS

"""

for item in data['competitors'][:15]:
    report += f"- {item}\n\n"

report += """
---

## 5. GROWTH DRIVERS (Pricing, Traffic, New Stores)

"""

for item in data['growth_drivers'][:15]:
    report += f"- {item}\n\n"

report += """
---

## 6. FUTURE PLANS & GUIDANCE

"""

for item in data['future_plans'][:15]:
    report += f"- {item}\n\n"

with open('COMPREHENSIVE_SEGMENTS_REPORT.md', 'w') as f:
    f.write(report)

print("✓ Created COMPREHENSIVE_SEGMENTS_REPORT.md")

# Now extract Q1 FY2026 specific data for TTM calculations
print("\nExtracting Q1 FY2026 financial data...")

with open('extracted_reports.json', 'r') as f:
    reports = json.load(f)

q1_2026_text = reports.get('Q1_FY2026 Earnings Call Transcript.pdf', '')
q1_2026_deck = reports.get('Q1 FY2026 Earnings Release Deck.pdf', '')

# Extract key metrics
import re

metrics = {
    'revenue': [],
    'same_store_sales': [],
    'ebitda': [],
    'eps': [],
    'restaurant_count': []
}

combined_text = q1_2026_text + q1_2026_deck

# Find revenue mentions
revenue_matches = re.findall(r'revenue[^.]{0,100}(?:\$[\d,]+(?:\.\d+)?|\d+(?:\.\d+)?%)', combined_text, re.IGNORECASE)
metrics['revenue'] = revenue_matches[:10]

# Find same-store sales
sss_matches = re.findall(r'same[- ]store sales[^.]{0,100}(?:\d+(?:\.\d+)?%)', combined_text, re.IGNORECASE)
metrics['same_store_sales'] = sss_matches[:10]

# Find EBITDA
ebitda_matches = re.findall(r'EBITDA[^.]{0,100}(?:\$[\d,]+(?:\.\d+)?|\d+(?:\.\d+)?%)', combined_text, re.IGNORECASE)
metrics['ebitda'] = ebitda_matches[:10]

# Find EPS
eps_matches = re.findall(r'(?:earnings per share|EPS)[^.]{0,100}\$?\d+\.\d+', combined_text, re.IGNORECASE)
metrics['eps'] = eps_matches[:10]

with open('Q1_FY2026_KEY_METRICS.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("✓ Created Q1_FY2026_KEY_METRICS.json")
print(f"  - Revenue mentions: {len(metrics['revenue'])}")
print(f"  - Same-store sales: {len(metrics['same_store_sales'])}")
print(f"  - EBITDA mentions: {len(metrics['ebitda'])}")
print(f"  - EPS mentions: {len(metrics['eps'])}")
