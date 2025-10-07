import json
import plotly.graph_objects as go

BRAND_COLORS = {
    'olivegarden': '#FF0000',
    'longhornsteakhouse': '#FF8C00',
    'cheddars': '#0000FF',
    'chuys': '#00FF00',
    'yardhouse': '#800080',
    'ruthschris': '#8B0000',
    'thecapitalgrille': '#00008B',
    'seasons52': '#90EE90',
    'eddiev': '#5F9EA0',
    'bahamabreeze': '#87CEEB'
}

def create_static_views():
    """Create static images for PowerPoint"""
    
    with open('all_darden_locations_with_franchises.json', 'r') as f:
        all_data = json.load(f)
    
    # Prepare data
    all_lats, all_lons, all_texts, all_colors = [], [], [], []
    
    for brand_name, restaurants in all_data.items():
        for restaurant in restaurants:
            addr = restaurant.get('contactDetail', {}).get('address', {})
            coords = addr.get('coordinates', {})
            lat, lng = coords.get('latitude'), coords.get('longitude')
            
            if lat and lng:
                all_lats.append(lat)
                all_lons.append(lng)
                all_colors.append(BRAND_COLORS.get(brand_name, '#808080'))
                
                name = restaurant.get('restaurantName', brand_name)
                city = addr.get('city', '')
                all_texts.append(f"{brand_name}: {name}, {city}")
    
    # View 1: US Focus
    fig1 = go.Figure(go.Scattergeo(
        lon=all_lons, lat=all_lats, text=all_texts,
        mode='markers',
        marker=dict(size=3, color=all_colors, line=dict(width=0.5, color='white'))
    ))
    fig1.update_geos(
        projection_type="albers usa",
        showland=True, landcolor="rgb(250, 250, 250)",
        showlakes=True, lakecolor="rgb(230, 245, 255)"
    )
    fig1.update_layout(title='Darden US Locations (2,200+)', height=600)
    fig1.write_image('darden_us_map.png', width=1920, height=1080)
    print("✓ Created: darden_us_map.png (US focus)")
    
    # View 2: Global View
    fig2 = go.Figure(go.Scattergeo(
        lon=all_lons, lat=all_lats, text=all_texts,
        mode='markers',
        marker=dict(size=4, color=all_colors, line=dict(width=0.5, color='white'))
    ))
    fig2.update_geos(
        projection_type="natural earth",
        showland=True, landcolor="rgb(243, 243, 243)",
        showocean=True, oceancolor="rgb(230, 245, 255)"
    )
    fig2.update_layout(title='Darden Worldwide Locations (2,353)', height=600)
    fig2.write_image('darden_world_map.png', width=1920, height=1080)
    print("✓ Created: darden_world_map.png (World view)")
    
    # View 3: Globe - Americas
    fig3 = go.Figure(go.Scattergeo(
        lon=all_lons, lat=all_lats, text=all_texts,
        mode='markers',
        marker=dict(size=4, color=all_colors, line=dict(width=0.5, color='white'))
    ))
    fig3.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=-100, lat=40),
        showland=True, landcolor="rgb(243, 243, 243)",
        showocean=True, oceancolor="rgb(230, 245, 255)"
    )
    fig3.update_layout(title='Darden Globe View - Americas', height=800)
    fig3.write_image('darden_globe_americas.png', width=1920, height=1080)
    print("✓ Created: darden_globe_americas.png (Globe - Americas)")
    
    print("\n✓ All static images created!")
    print("  Use these in PowerPoint slides")
    print("  High resolution: 1920x1080")

if __name__ == "__main__":
    create_static_views()
