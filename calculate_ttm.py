import openpyxl
import pandas as pd

# Load existing financial data
wb = openpyxl.load_workbook('Darden Financials.xlsx', data_only=True)

# Get Income Statement data
ws = wb['Income Statement ']  # Note the space
data = []
for row in ws.iter_rows(min_row=1, values_only=True):
    data.append(row)

# Create TTM calculations
# TTM = Q1 FY2026 + Q4 FY2025 + Q3 FY2025 + Q2 FY2025
# This gives us the most recent 12 months

print("=" * 80)
print("TTM (TRAILING TWELVE MONTHS) CALCULATIONS")
print("Most Recent 12 Months: Q2 FY2025 + Q3 FY2025 + Q4 FY2025 + Q1 FY2026")
print("=" * 80)

# Key metrics from your Excel (FY2025 full year)
fy2025_sales = 12076.7
fy2025_operating_income = 1362.3
fy2025_net_earnings = 1049.6

# Q1 FY2026 estimates (from earnings call - typically ~25% of annual)
# These are approximations - you'll need actual Q1 numbers from 10-Q when available
q1_2026_sales_estimate = 3100  # Approximately, based on 6% growth
q1_2026_operating_income_estimate = 350
q1_2026_net_earnings_estimate = 270

# Q1 FY2025 (to subtract out for TTM calculation)
q1_2025_sales = 2989  # Approximate from quarterly data
q1_2025_operating_income = 330
q1_2025_net_earnings = 255

# TTM Calculation
ttm_sales = fy2025_sales - q1_2025_sales + q1_2026_sales_estimate
ttm_operating_income = fy2025_operating_income - q1_2025_operating_income + q1_2026_operating_income_estimate
ttm_net_earnings = fy2025_net_earnings - q1_2025_net_earnings + q1_2026_net_earnings_estimate

print(f"\nTTM REVENUE: ${ttm_sales:.1f}M")
print(f"  FY2025 Full Year: ${fy2025_sales:.1f}M")
print(f"  Less Q1 FY2025: -${q1_2025_sales:.1f}M")
print(f"  Plus Q1 FY2026: +${q1_2026_sales_estimate:.1f}M")
print(f"  Growth vs FY2025: {((ttm_sales/fy2025_sales - 1) * 100):.1f}%")

print(f"\nTTM OPERATING INCOME: ${ttm_operating_income:.1f}M")
print(f"  Operating Margin: {(ttm_operating_income/ttm_sales * 100):.2f}%")

print(f"\nTTM NET EARNINGS: ${ttm_net_earnings:.1f}M")
print(f"  Net Margin: {(ttm_net_earnings/ttm_sales * 100):.2f}%")

# Calculate key ratios
print("\n" + "=" * 80)
print("TTM KEY RATIOS")
print("=" * 80)

ttm_operating_margin = (ttm_operating_income / ttm_sales) * 100
ttm_net_margin = (ttm_net_earnings / ttm_sales) * 100

print(f"Operating Margin: {ttm_operating_margin:.2f}%")
print(f"Net Profit Margin: {ttm_net_margin:.2f}%")

# Segment TTM estimates
print("\n" + "=" * 80)
print("TTM BY SEGMENT (Estimates)")
print("=" * 80)

segments = {
    'Olive Garden': {'fy2025': 5236, 'growth': 0.017, 'margin': 21.9},
    'LongHorn': {'fy2025': 3073, 'growth': 0.051, 'margin': 18.2},
    'Fine Dining': {'fy2025': 2609, 'growth': -0.03, 'margin': 18.7},
    'Other': {'fy2025': 1159, 'growth': 0.002, 'margin': 15.1}
}

for segment, data in segments.items():
    ttm_revenue = data['fy2025'] * (1 + data['growth'] * 0.25)  # Approximate quarterly impact
    ttm_ebitda = ttm_revenue * (data['margin'] / 100)
    print(f"\n{segment}:")
    print(f"  TTM Revenue: ${ttm_revenue:.1f}M")
    print(f"  TTM EBITDA: ${ttm_ebitda:.1f}M ({data['margin']}% margin)")

print("\n" + "=" * 80)
print("NOTE: Q1 FY2026 10-Q not yet available at time of analysis.")
print("These are estimates based on earnings call guidance and historical patterns.")
print("UPDATE WITH ACTUAL Q1 FY2026 DATA WHEN 10-Q IS RELEASED!")
print("=" * 80)

# Save TTM data
ttm_data = {
    'TTM_Revenue': ttm_sales,
    'TTM_Operating_Income': ttm_operating_income,
    'TTM_Net_Earnings': ttm_net_earnings,
    'TTM_Operating_Margin': ttm_operating_margin,
    'TTM_Net_Margin': ttm_net_margin,
    'Segments': segments
}

import json
with open('TTM_CALCULATIONS.json', 'w') as f:
    json.dump(ttm_data, f, indent=2)

print("\n✓ Saved TTM_CALCULATIONS.json")
