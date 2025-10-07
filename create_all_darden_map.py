import json
import folium
from folium.plugins import MarkerCluster

BRAND_COLORS = {
    'olivegarden': {'color': 'red', 'icon': 'cutlery'},
    'longhornsteakhouse': {'color': 'orange', 'icon': 'cutlery'},
    'cheddars': {'color': 'blue', 'icon': 'cutlery'},
    'chuys': {'color': 'green', 'icon': 'cutlery'},
    'yardhouse': {'color': 'purple', 'icon': 'beer'},
    'ruthschris': {'color': 'darkred', 'icon': 'cutlery'},
    'thecapitalgrille': {'color': 'darkblue', 'icon': 'cutlery'},
    'seasons52': {'color': 'lightgreen', 'icon': 'leaf'},
    'eddiev': {'color': 'cadetblue', 'icon': 'cutlery'},
    'bahamabreeze': {'color': 'lightblue', 'icon': 'umbrella'}
}

def create_all_darden_map():
    """Create interactive map with all Darden brands"""
    
    # Load data
    with open('all_darden_locations_with_franchises.json', 'r') as f:
        all_data = json.load(f)
    
    # Create map
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Create layer for each brand
    for brand_name, restaurants in all_data.items():
        if not restaurants:
            continue
            
        brand_config = BRAND_COLORS.get(brand_name, {'color': 'gray', 'icon': 'info-sign'})
        feature_group = folium.FeatureGroup(name=brand_name.replace('_', ' ').title())
        
        for restaurant in restaurants:
            addr = restaurant.get('contactDetail', {}).get('address', {})
            coords = addr.get('coordinates', {})
            
            lat = coords.get('latitude')
            lng = coords.get('longitude')
            
            if lat and lng:
                name = restaurant.get('restaurantName', brand_name)
                street = addr.get('street1', '')
                city = addr.get('city', '')
                state = addr.get('stateCode', '')
                zipcode = addr.get('zipCode', '')
                
                popup_html = f"""
                <b>{brand_name.upper()}</b><br>
                <b>{name}</b><br>
                {street}<br>
                {city}, {state} {zipcode}
                """
                
                folium.Marker(
                    location=[lat, lng],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{brand_name}: {name}",
                    icon=folium.Icon(
                        color=brand_config['color'],
                        icon=brand_config['icon'],
                        prefix='fa'
                    )
                ).add_to(feature_group)
        
        feature_group.add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Save
    m.save('all_darden_map.html')
    
    # Print summary
    total = sum(len(r) for r in all_data.values())
    print(f"✓ Interactive map created: all_darden_map.html")
    print(f"✓ Total locations mapped: {total}")
    print("\nBrands included:")
    for brand, restaurants in all_data.items():
        print(f"  - {brand}: {len(restaurants)} locations")
    print("\nOpen all_darden_map.html in your browser!")
    print("Use the layer control (top right) to toggle brands on/off")

if __name__ == "__main__":
    create_all_darden_map()
