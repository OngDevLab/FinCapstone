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

# Comprehensive grid covering all regions
REGIONS = {
    'continental_us': {'lat': range(25, 50, 3), 'lng': range(-125, -65, 3)},
    'alaska': {'lat': range(55, 72, 5), 'lng': range(-170, -130, 5)},
    'hawaii': {'lat': range(19, 23, 2), 'lng': range(-161, -154, 2)},
    'canada': {'lat': range(42, 70, 4), 'lng': range(-141, -52, 4)},
    'mexico': {'lat': range(14, 33, 3), 'lng': range(-118, -86, 3)},
    'caribbean': {'lat': range(10, 28, 3), 'lng': range(-85, -60, 3)},
    'central_america': {'lat': range(7, 18, 3), 'lng': range(-93, -77, 3)},
    'south_america': {'lat': range(-35, 13, 5), 'lng': range(-82, -34, 5)},
    'middle_east': {'lat': range(12, 42, 5), 'lng': range(34, 60, 5)},
    'asia': {'lat': range(-10, 55, 5), 'lng': range(95, 145, 5)}
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

def scrape_brand_complete(brand_name, brand_url):
    """Scrape all locations worldwide for a brand"""
    print(f"\n{'='*80}")
    print(f"Scraping {brand_name.upper()} - WORLDWIDE")
    print(f"{'='*80}")
    
    all_restaurants = {}
    
    for region_name, coords in REGIONS.items():
        print(f"\nSearching {region_name}...")
        lat_range = coords['lat']
        lng_range = coords['lng']
        
        for lat, lng in product(lat_range, lng_range):
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
                        country = addr.get('country', '')
                        print(f"  ✓ {name} - {city}, {state}, {country}")
            
            time.sleep(0.2)
    
    restaurants_list = list(all_restaurants.values())
    
    # Save to file
    filename = f'{brand_name}_locations_complete.json'
    with open(filename, 'w') as f:
        json.dump(restaurants_list, f, indent=2)
    
    # Print country breakdown
    countries = {}
    for r in restaurants_list:
        addr = r.get('contactDetail', {}).get('address', {})
        country = addr.get('country', 'Unknown')
        countries[country] = countries.get(country, 0) + 1
    
    print(f"\n✓ {brand_name}: {len(restaurants_list)} total locations")
    print("  By country:")
    for country, count in sorted(countries.items()):
        print(f"    {country}: {count}")
    
    return restaurants_list

def scrape_all_brands_complete():
    """Scrape all Darden brands worldwide"""
    all_data = {}
    
    for brand_name, brand_url in BRANDS.items():
        try:
            restaurants = scrape_brand_complete(brand_name, brand_url)
            all_data[brand_name] = restaurants
        except Exception as e:
            print(f"✗ Error scraping {brand_name}: {e}")
            all_data[brand_name] = []
    
    # Save combined file
    with open('all_darden_locations_complete.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    # Print summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY - ALL DARDEN BRANDS WORLDWIDE")
    print(f"{'='*80}")
    total = 0
    for brand, restaurants in all_data.items():
        count = len(restaurants)
        total += count
        print(f"{brand:20s}: {count:4d} locations")
    print(f"{'='*80}")
    print(f"{'TOTAL':20s}: {total:4d} locations")
    print(f"\n✓ All data saved to all_darden_locations_complete.json")

if __name__ == "__main__":
    print("Scraping ALL Darden restaurant brands WORLDWIDE...")
    print("This will take 2-3 hours to complete")
    print()
    scrape_all_brands_complete()
