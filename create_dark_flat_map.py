import json
import folium
from folium.plugins import MarkerCluster

BRAND_COLORS = {
    'olivegarden': 'red',
    'longhornsteakhouse': 'orange',
    'cheddars': 'blue',
    'chuys': 'green',
    'yardhouse': 'purple',
    'ruthschris': 'darkred',
    'thecapitalgrille': 'darkblue',
    'seasons52': 'lightgreen',
    'eddiev': 'cadetblue',
    'bahamabreeze': 'lightblue'
}

def create_dark_flat_map():
    """Create dark-themed flat map with clustering"""
    
    with open('all_darden_locations_with_franchises.json', 'r') as f:
        all_data = json.load(f)
    
    # Create dark map
    m = folium.Map(
        location=[39.8283, -98.5795],
        zoom_start=4,
        tiles='CartoDB dark_matter'  # Dark theme
    )
    
    # Add each brand as a layer
    for brand_name, restaurants in all_data.items():
        if not restaurants:
            continue
        
        brand_config = BRAND_COLORS.get(brand_name, 'gray')
        feature_group = folium.FeatureGroup(name=brand_name.replace('_', ' ').title())
        marker_cluster = MarkerCluster().add_to(feature_group)
        
        for restaurant in restaurants:
            addr = restaurant.get('contactDetail', {}).get('address', {})
            coords = addr.get('coordinates', {})
            lat, lng = coords.get('latitude'), coords.get('longitude')
            
            if lat and lng:
                name = restaurant.get('restaurantName', brand_name)
                street = addr.get('street1', '')
                city = addr.get('city', '')
                state = addr.get('stateCode', '')
                zipcode = addr.get('zipCode', '')
                
                popup_html = f"""
                <div style="font-family: Arial; min-width: 200px;">
                    <h4 style="margin: 0 0 10px 0; color: #333;">{brand_name.upper()}</h4>
                    <b>{name}</b><br>
                    {street}<br>
                    {city}, {state} {zipcode}
                </div>
                """
                
                folium.CircleMarker(
                    location=[lat, lng],
                    radius=3,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{brand_name}: {name}",
                    color=brand_config,
                    fill=True,
                    fillColor=brand_config,
                    fillOpacity=0.7,
                    weight=1
                ).add_to(marker_cluster)
        
        feature_group.add_to(m)
    
    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Save
    m.save('darden_dark_flat_map.html')
    
    total = sum(len(r) for r in all_data.values())
    print(f"✓ Dark flat map created: darden_dark_flat_map.html")
    print(f"✓ Total locations: {total}")
    print("✓ Features:")
    print("  - Dark theme background")
    print("  - Tiny circle markers")
    print("  - Clustering for performance")
    print("  - Toggle brands with layer control")

if __name__ == "__main__":
    create_dark_flat_map()
