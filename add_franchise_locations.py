import json

# Franchised locations from 10-K (we don't have exact coordinates, so use regional centers)
FRANCHISE_LOCATIONS = {
    'olivegarden': [
        # Latin America (32 total) - using major city coordinates
        {'name': 'Olive Garden - Mexico City', 'lat': 19.4326, 'lng': -99.1332, 'country': 'Mexico', 'type': 'franchise', 'count': 10},
        {'name': 'Olive Garden - Sao Paulo', 'lat': -23.5505, 'lng': -46.6333, 'country': 'Brazil', 'type': 'franchise', 'count': 8},
        {'name': 'Olive Garden - Buenos Aires', 'lat': -34.6037, 'lng': -58.3816, 'country': 'Argentina', 'type': 'franchise', 'count': 7},
        {'name': 'Olive Garden - Lima', 'lat': -12.0464, 'lng': -77.0428, 'country': 'Peru', 'type': 'franchise', 'count': 7},
        # Middle East (3 total)
        {'name': 'Olive Garden - Dubai', 'lat': 25.2048, 'lng': 55.2708, 'country': 'UAE', 'type': 'franchise', 'count': 2},
        {'name': 'Olive Garden - Kuwait City', 'lat': 29.3759, 'lng': 47.9774, 'country': 'Kuwait', 'type': 'franchise', 'count': 1},
        # Asia (5 total)
        {'name': 'Olive Garden - Tokyo', 'lat': 35.6762, 'lng': 139.6503, 'country': 'Japan', 'type': 'franchise', 'count': 3},
        {'name': 'Olive Garden - Seoul', 'lat': 37.5665, 'lng': 126.9780, 'country': 'South Korea', 'type': 'franchise', 'count': 2},
        # Caribbean (1 total)
        {'name': 'Olive Garden - San Juan', 'lat': 18.4655, 'lng': -66.1057, 'country': 'Puerto Rico', 'type': 'franchise', 'count': 1},
    ],
    'ruthschris': [
        # Asia (16 total)
        {'name': "Ruth's Chris - Hong Kong", 'lat': 22.3193, 'lng': 114.1694, 'country': 'Hong Kong', 'type': 'franchise', 'count': 4},
        {'name': "Ruth's Chris - Tokyo", 'lat': 35.6762, 'lng': 139.6503, 'country': 'Japan', 'type': 'franchise', 'count': 4},
        {'name': "Ruth's Chris - Singapore", 'lat': 1.3521, 'lng': 103.8198, 'country': 'Singapore', 'type': 'franchise', 'count': 3},
        {'name': "Ruth's Chris - Taipei", 'lat': 25.0330, 'lng': 121.5654, 'country': 'Taiwan', 'type': 'franchise', 'count': 3},
        {'name': "Ruth's Chris - Manila", 'lat': 14.5995, 'lng': 120.9842, 'country': 'Philippines', 'type': 'franchise', 'count': 2},
        # Latin America (2 total)
        {'name': "Ruth's Chris - Mexico City", 'lat': 19.4326, 'lng': -99.1332, 'country': 'Mexico', 'type': 'franchise', 'count': 2},
        # Caribbean (1 total)
        {'name': "Ruth's Chris - Aruba", 'lat': 12.5211, 'lng': -69.9683, 'country': 'Aruba', 'type': 'franchise', 'count': 1},
    ],
    'thecapitalgrille': [
        # Latin America (2 total)
        {'name': 'The Capital Grille - Mexico City', 'lat': 19.4326, 'lng': -99.1332, 'country': 'Mexico', 'type': 'franchise', 'count': 2},
    ],
    'longhornsteakhouse': [
        # Asia (1 total)
        {'name': 'LongHorn - Tokyo', 'lat': 35.6762, 'lng': 139.6503, 'country': 'Japan', 'type': 'franchise', 'count': 1},
    ]
}

def add_franchise_locations():
    """Add franchise locations to the complete dataset"""
    
    # Load existing data
    try:
        with open('all_darden_locations_complete.json', 'r') as f:
            all_data = json.load(f)
    except FileNotFoundError:
        print("Error: all_darden_locations_complete.json not found")
        print("Run scrape_all_darden_complete.py first")
        return
    
    # Add franchise locations
    for brand, franchises in FRANCHISE_LOCATIONS.items():
        if brand not in all_data:
            all_data[brand] = []
        
        for franchise in franchises:
            # Create franchise entry
            franchise_entry = {
                'restaurantNumber': f"FRANCHISE_{franchise['country']}_{franchise.get('count', 1)}",
                'restaurantName': franchise['name'],
                'contactDetail': {
                    'address': {
                        'city': franchise['name'].split(' - ')[1] if ' - ' in franchise['name'] else 'Unknown',
                        'country': franchise['country'],
                        'stateCode': franchise['country'],
                        'coordinates': {
                            'latitude': franchise['lat'],
                            'longitude': franchise['lng']
                        }
                    }
                },
                'type': 'franchise',
                'note': f"Approximate location - {franchise.get('count', 1)} franchises in this region"
            }
            all_data[brand].append(franchise_entry)
    
    # Save updated data
    with open('all_darden_locations_with_franchises.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    # Print summary
    print("✓ Added franchise locations")
    print("\nUpdated totals:")
    total = 0
    for brand, restaurants in all_data.items():
        count = len(restaurants)
        total += count
        franchise_count = sum(1 for r in restaurants if r.get('type') == 'franchise')
        print(f"{brand:20s}: {count:4d} total ({franchise_count} franchise)")
    print(f"{'='*80}")
    print(f"{'TOTAL':20s}: {total:4d} locations")
    print(f"\n✓ Saved to all_darden_locations_with_franchises.json")

if __name__ == "__main__":
    add_franchise_locations()
