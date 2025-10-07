import requests
from bs4 import BeautifulSoup
import json
import time

def check_for_location_data():
    """Check common endpoints for location data"""
    
    base_urls = [
        "https://www.olivegarden.com/locations/sitemap",
        "https://www.olivegarden.com/api/locations",
        "https://www.olivegarden.com/locations.json",
        "https://www.olivegarden.com/locations/all",
    ]
    
    for url in base_urls:
        try:
            response = requests.get(url, timeout=10)
            print(f"{url}: {response.status_code}")
            if response.status_code == 200:
                print(f"  Found! Content type: {response.headers.get('content-type')}")
                print(f"  First 200 chars: {response.text[:200]}")
        except Exception as e:
            print(f"{url}: Error - {e}")
        time.sleep(1)

if __name__ == "__main__":
    print("Checking for Olive Garden location data endpoints...\n")
    check_for_location_data()
    
    print("\n" + "="*80)
    print("INSTRUCTIONS:")
    print("1. Go to olivegarden.com/locations/location-search")
    print("2. Open DevTools (F12) -> Network tab")
    print("3. Clear the network log")
    print("4. Search for 'New York' or any city")
    print("5. Look for requests that return restaurant data (NOT mapbox)")
    print("6. Share the URL of that request")
