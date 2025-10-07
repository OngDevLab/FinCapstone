import requests
import json
import time
from itertools import product

BRANDS = {
    'olivegarden': 'https://www.olivegarden.com/api/restaurants',
    'longhornsteakhouse': 'https://www.longhornsteakhouse.com/api/restaurants',
    'cheddars': 'https://www.cheddars.com/api/restaurants',
    'chuys': 'https://www.chuys.com/api/restaurants',
    'yardhouse': 'https://www.yardhouse.com/api/restaurants',
    'ruthschris': 'https://www.ruthschris.com/api/restaurants',
    'thecapitalgrille': 'https://www.thecapitalgrille.com/api/restaurants',
    'seasons52': 'https://www.seasons52.com/api/restaurants',
    'eddiev': 'https://www.eddiev.com/api/restaurants',
    'bahamabreeze': 'https://www.bahamabreeze.com/api/restaurants'
}

def get_restaurants_at_location(brand_url, lat, lng, results_per_page=100):
    """Get restaurants near a coordinate"""
    params = {
        'locale': 'en_US',
        'latitude': lat,
        'longitude': lng,
        'resultsPerPage': results_per_page
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': brand_url.replace('/api/restaurants', '/'),
        'X-Source-Channel': 'WEB',
        'X-Api-Id': '-2065913831',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(brand_url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def scrape_brand(brand_name, brand_url):
    """Scrape all locations for a brand"""
    print(f"\n{'='*80}")
    print(f"Scraping {brand_name.upper()}...")
    print(f"{'='*80}")
    
    # Grid covering US
    lat_range = range(25, 50, 3)
    lng_range = range(-125, -65, 3)
    
    all_restaurants = {}
    
    for i, (lat, lng) in enumerate(product(lat_range, lng_range)):
        if i % 20 == 0:
            print(f"Progress: {i}/{len(lat_range) * len(lng_range)}")
        
        data = get_restaurants_at_location(brand_url, lat, lng, 100)
        
        if data and 'restaurants' in data:
            for restaurant in data['restaurants']:
                rest_id = restaurant.get('restaurantNumber')
                if rest_id and rest_id not in all_restaurants:
                    all_restaurants[rest_id] = restaurant
                    addr = restaurant.get('contactDetail', {}).get('address', {})
                    name = restaurant.get('restaurantName', 'Unknown')
                    city = addr.get('city', '')
                    state = addr.get('stateCode', '')
                    print(f"  ✓ {name} - {city}, {state}")
        
        time.sleep(0.3)
    
    restaurants_list = list(all_restaurants.values())
    
    # Save to file
    filename = f'{brand_name}_locations.json'
    with open(filename, 'w') as f:
        json.dump(restaurants_list, f, indent=2)
    
    print(f"\n✓ {brand_name}: {len(restaurants_list)} locations saved to {filename}")
    return restaurants_list

def scrape_all_brands():
    """Scrape all Darden brands"""
    all_data = {}
    
    for brand_name, brand_url in BRANDS.items():
        try:
            restaurants = scrape_brand(brand_name, brand_url)
            all_data[brand_name] = restaurants
        except Exception as e:
            print(f"✗ Error scraping {brand_name}: {e}")
            all_data[brand_name] = []
    
    # Save combined file
    with open('all_darden_locations.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    total = 0
    for brand, restaurants in all_data.items():
        count = len(restaurants)
        total += count
        print(f"{brand:20s}: {count:4d} locations")
    print(f"{'='*80}")
    print(f"{'TOTAL':20s}: {total:4d} locations")
    print(f"\n✓ All data saved to all_darden_locations.json")

if __name__ == "__main__":
    print("Scraping ALL Darden restaurant brands...")
    print("This will take 1-2 hours to complete")
    print()
    scrape_all_brands()
