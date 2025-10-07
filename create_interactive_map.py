import json
import folium
from folium.plugins import MarkerCluster

def create_interactive_map():
    """Create an interactive map of Olive Garden locations"""
    
    # Load the scraped data
    with open('olive_garden_locations.json', 'r') as f:
        restaurants = json.load(f)
    
    # Create base map centered on US
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Add marker cluster for better performance
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add each restaurant as a marker
    for restaurant in restaurants:
        addr = restaurant.get('contactDetail', {}).get('address', {})
        coords = addr.get('coordinates', {})
        
        lat = coords.get('latitude')
        lng = coords.get('longitude')
        
        if lat and lng:
            name = restaurant.get('restaurantName', 'Olive Garden')
            street = addr.get('street1', '')
            city = addr.get('city', '')
            state = addr.get('stateCode', '')
            zipcode = addr.get('zipCode', '')
            phone = restaurant.get('contactDetail', {}).get('phoneDetail', [{}])[0].get('phoneNumber', '')
            
            popup_html = f"""
            <b>{name}</b><br>
            {street}<br>
            {city}, {state} {zipcode}<br>
            Phone: {phone}
            """
            
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{name}",
                icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
            ).add_to(marker_cluster)
    
    # Save map
    m.save('olive_garden_map.html')
    print(f"✓ Interactive map created: olive_garden_map.html")
    print(f"✓ Total locations mapped: {len(restaurants)}")
    print("\nOpen olive_garden_map.html in your browser to view the map!")

if __name__ == "__main__":
    create_interactive_map()
