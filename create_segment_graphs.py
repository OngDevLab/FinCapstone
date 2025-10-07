import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

wb = openpyxl.load_workbook('Darden Financials.xlsx', data_only=True)
ws = wb['Segments-Formatted']

data = []
for row in ws.iter_rows(min_row=3, values_only=True):
    if row[0] and 'Avg' not in str(row[0]):
        data.append(row)

df = pd.DataFrame(data, columns=[
    'Company', 'TSG_2022', 'TSG_2023', 'TSG_2024', 'TSG_2025', 'TSG_Comments', None,
    'SSS_2022', 'SSS_2023', 'SSS_2024', 'SSS_2025', 'SSS_Comments', None,
    'EBITDA_2022', 'EBITDA_2023', 'EBITDA_2024', 'EBITDA_2025', 'EBITDA_Comments', None,
    'EPS_2022', 'EPS_2023', 'EPS_2024', 'EPS_2025', 'EPS_Comments', None,
    'Debt_2022', 'Debt_2023', 'Debt_2024', 'Debt_2025', 'Debt_Comments', None,
    'AUV_2022', 'AUV_2023', 'AUV_2024', 'AUV_2025', 'AUV_Comments'
])

# Filter Darden segments
darden_segments = df[df['Company'].str.contains('Darden', na=False)]

# 1. Same-Store Sales Growth by Segment
fig, ax = plt.subplots(figsize=(12, 6))
segments = ['Olive Garden', 'LongHorn Steakhouse', 'Fine Dining', 'Other']
years = ['2022', '2023', '2024', '2025']
x = range(len(years))
width = 0.2

for i, seg in enumerate(segments):
    row = darden_segments[darden_segments['Company'].str.contains(seg, na=False)]
    if not row.empty:
        values = [row[f'SSS_{y}'].values[0] for y in years]
        ax.bar([p + width*i for p in x], values, width, label=seg)

ax.set_xlabel('Year')
ax.set_ylabel('Same-Store Sales Growth (%)')
ax.set_title('Darden Segments: Same-Store Sales Growth Comparison')
ax.set_xticks([p + width*1.5 for p in x])
ax.set_xticklabels(years)
ax.legend()
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('segment_sss_growth.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. EBITDA Margin by Segment
fig, ax = plt.subplots(figsize=(12, 6))
for i, seg in enumerate(segments):
    row = darden_segments[darden_segments['Company'].str.contains(seg, na=False)]
    if not row.empty:
        values = []
        for y in years:
            val = row[f'EBITDA_{y}'].values[0]
            values.append(val if val != 'N/A' else None)
        if any(v is not None for v in values):
            ax.plot(years, values, marker='o', linewidth=2, label=seg)

ax.set_xlabel('Year')
ax.set_ylabel('Adjusted EBITDA Margin (%)')
ax.set_title('Darden Segments: EBITDA Margin Trends')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('segment_ebitda_margin.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. AUV Comparison
fig, ax = plt.subplots(figsize=(10, 6))
auv_data = []
labels = []
for seg in segments:
    row = darden_segments[darden_segments['Company'].str.contains(seg, na=False)]
    if not row.empty:
        val = row['AUV_2025'].values[0]
        if val != 'N/A':
            auv_data.append(val)
            labels.append(seg)

ax.barh(labels, auv_data, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
ax.set_xlabel('Average Unit Volume ($M)')
ax.set_title('Darden Segments: AUV Comparison (FY2025)')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(auv_data):
    ax.text(v + 0.1, i, f'${v}M', va='center')
plt.tight_layout()
plt.savefig('segment_auv_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Segment vs Competitors - Same-Store Sales (2025)
fig, ax = plt.subplots(figsize=(14, 8))
categories = {
    'Restaurant Groups': ['Darden Restaurants', "Bloomin' Brands", "Brinker Int'l"],
    'Fine Dining': ['The One Group (STKS)', 'Darden - Fine Dining'],
    'Casual Dining': ['Texas Roadhouse', "BJ's Restaurants", 'Cheesecake Factory', 
                      'Darden - Olive Garden', 'Darden - LongHorn Steakhouse'],
    'Fast Casual': ['Shake Shack', 'Chipotle', 'Wingstop', 'Darden - Other']
}

y_pos = 0
colors = {'Darden': '#d62728', 'Competitor': '#1f77b4'}
yticks = []
ylabels = []

for cat, companies in categories.items():
    y_pos -= 1
    ax.text(-5, y_pos, cat, fontweight='bold', fontsize=11)
    yticks.append(y_pos)
    ylabels.append('')
    
    for comp in companies:
        row = df[df['Company'] == comp]
        if not row.empty:
            val = row['SSS_2025'].values[0]
            if val != 'N/A' and val is not None:
                y_pos -= 1
                color = colors['Darden'] if 'Darden' in comp else colors['Competitor']
                ax.barh(y_pos, val, color=color, alpha=0.8)
                label = comp.replace('Darden - ', '')
                ax.text(-0.5, y_pos, label, ha='right', va='center', fontsize=9)
                ax.text(val + 0.3, y_pos, f'{val:.1f}%', va='center', fontsize=8)
                yticks.append(y_pos)
                ylabels.append('')
    y_pos -= 0.5

ax.set_yticks(yticks)
ax.set_yticklabels(ylabels)
ax.set_xlabel('Same-Store Sales Growth (%) - 2025')
ax.set_title('Darden Segments vs Competitors: Same-Store Sales Growth (2025)')
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(axis='x', alpha=0.3)
ax.legend([plt.Rectangle((0,0),1,1, color=colors['Darden']), 
           plt.Rectangle((0,0),1,1, color=colors['Competitor'])],
          ['Darden Segments', 'Competitors'], loc='lower right')
plt.tight_layout()
plt.savefig('segment_vs_competitors_sss.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Total Sales Growth Comparison
fig, ax = plt.subplots(figsize=(12, 6))
comparison_companies = ['Darden - Olive Garden', 'Darden - LongHorn Steakhouse', 
                        'Texas Roadhouse', 'Cheesecake Factory', "Brinker Int'l"]
for comp in comparison_companies:
    row = df[df['Company'] == comp]
    if not row.empty:
        values = [row[f'TSG_{y}'].values[0] for y in years]
        label = comp.replace('Darden - ', '')
        ax.plot(years, values, marker='o', linewidth=2, label=label)

ax.set_xlabel('Year')
ax.set_ylabel('Total Sales Growth (%)')
ax.set_title('Sales Growth: Darden Segments vs Key Casual Dining Competitors')
ax.legend()
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.savefig('segment_sales_growth_vs_competitors.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ segment_sss_growth.png")
print("✓ segment_ebitda_margin.png")
print("✓ segment_auv_comparison.png")
print("✓ segment_vs_competitors_sss.png")
print("✓ segment_sales_growth_vs_competitors.png")
