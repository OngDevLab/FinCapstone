import requests
import json
import time
from itertools import product

def get_restaurants_at_location(lat, lng, results_per_page=100):
    """Get Olive Garden restaurants near a coordinate"""
    url = "https://www.olivegarden.com/api/restaurants"
    params = {
        'locale': 'en_US',
        'latitude': lat,
        'longitude': lng,
        'resultsPerPage': results_per_page
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'Referer': 'https://www.olivegarden.com/',
        'X-Source-Channel': 'WEB',
        'X-Api-Id': '-2065913831',
        'Accept': 'application/json, text/plain, */*'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error at ({lat}, {lng}): {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception at ({lat}, {lng}): {e}")
        return None

def scrape_all_olive_gardens():
    """Scrape all Olive Garden locations by covering the US with a grid"""
    
    # Create a grid covering the continental US
    # Lat: ~25 to 49, Lng: ~-125 to -66
    lat_range = range(25, 50, 3)  # Every 3 degrees (~200 miles)
    lng_range = range(-125, -65, 3)
    
    all_restaurants = {}
    
    print(f"Searching {len(lat_range) * len(lng_range)} grid points...")
    
    for i, (lat, lng) in enumerate(product(lat_range, lng_range)):
        print(f"Progress: {i+1}/{len(lat_range) * len(lng_range)} - Checking ({lat}, {lng})")
        
        data = get_restaurants_at_location(lat, lng, results_per_page=100)
        
        if data and 'restaurants' in data:
            for restaurant in data['restaurants']:
                # Use restaurant number as key to avoid duplicates
                rest_id = restaurant.get('restaurantNumber')
                if rest_id and rest_id not in all_restaurants:
                    all_restaurants[rest_id] = restaurant
                    addr = restaurant.get('contactDetail', {}).get('address', {})
                    name = restaurant.get('restaurantName', 'Unknown')
                    city = addr.get('city', '')
                    state = addr.get('stateCode', '')
                    print(f"  Found: {name} - {city}, {state}")
        
        time.sleep(0.5)  # Be respectful
    
    # Convert to list
    restaurants_list = list(all_restaurants.values())
    
    # Save to file
    with open('olive_garden_locations.json', 'w') as f:
        json.dump(restaurants_list, f, indent=2)
    
    print(f"\n✓ Total unique locations found: {len(restaurants_list)}")
    print(f"✓ Saved to olive_garden_locations.json")
    
    return restaurants_list

if __name__ == "__main__":
    print("Scraping Olive Garden locations...")
    print("This will take ~10-15 minutes to cover the entire US")
    print()
    
    restaurants = scrape_all_olive_gardens()
    
    # Print summary
    states = {}
    for r in restaurants:
        addr = r.get('contactDetail', {}).get('address', {})
        state = addr.get('stateCode', 'Unknown')
        states[state] = states.get(state, 0) + 1
    
    print("\nLocations by state:")
    for state, count in sorted(states.items(), key=lambda x: x[1], reverse=True):
        print(f"  {state}: {count}")
