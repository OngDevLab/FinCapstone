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

def create_globe_map():
    """Create 3D globe visualization with all Darden locations"""
    
    # Load data
    with open('all_darden_locations_with_franchises.json', 'r') as f:
        all_data = json.load(f)
    
    fig = go.Figure()
    
    # Add each brand as a separate trace
    for brand_name, restaurants in all_data.items():
        if not restaurants:
            continue
        
        lats = []
        lons = []
        texts = []
        
        for restaurant in restaurants:
            addr = restaurant.get('contactDetail', {}).get('address', {})
            coords = addr.get('coordinates', {})
            
            lat = coords.get('latitude')
            lng = coords.get('longitude')
            
            if lat and lng:
                lats.append(lat)
                lons.append(lng)
                
                name = restaurant.get('restaurantName', brand_name)
                city = addr.get('city', '')
                state = addr.get('stateCode', '')
                country = addr.get('country', '')
                
                texts.append(f"{brand_name.upper()}<br>{name}<br>{city}, {state}, {country}")
        
        # Add trace for this brand
        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            text=texts,
            name=brand_name.replace('_', ' ').title(),
            mode='markers',
            marker=dict(
                size=4,
                color=BRAND_COLORS.get(brand_name, '#808080'),
                line=dict(width=0.5, color='white')
            ),
            hovertemplate='%{text}<extra></extra>'
        ))
    
    # Update layout for globe projection
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        coastlinecolor="rgb(204, 204, 204)",
        showocean=True,
        oceancolor="rgb(230, 245, 255)",
        showcountries=True,
        countrycolor="rgb(204, 204, 204)"
    )
    
    fig.update_layout(
        title=dict(
            text='Darden Restaurants Worldwide - 2,353 Locations',
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        height=800,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Save as HTML
    fig.write_html('darden_globe_map.html')
    
    print("✓ 3D Globe map created: darden_globe_map.html")
    print("✓ Features:")
    print("  - Rotate by dragging")
    print("  - Zoom with scroll wheel")
    print("  - Toggle brands on/off in legend")
    print("  - Hover over markers for details")
    print(f"✓ Total locations: {sum(len(r) for r in all_data.values())}")

if __name__ == "__main__":
    create_globe_map()
