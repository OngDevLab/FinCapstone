import json
import plotly.graph_objects as go

BRAND_COLORS = {
    'olivegarden': '#FF4444',
    'longhornsteakhouse': '#FFA500',
    'cheddars': '#4169E1',
    'chuys': '#32CD32',
    'yardhouse': '#9370DB',
    'ruthschris': '#DC143C',
    'thecapitalgrille': '#1E90FF',
    'seasons52': '#98FB98',
    'eddiev': '#20B2AA',
    'bahamabreeze': '#87CEEB'
}

def create_dark_globe():
    """Create dark-themed 3D globe with tiny markers"""
    
    with open('all_darden_locations_with_franchises.json', 'r') as f:
        all_data = json.load(f)
    
    fig = go.Figure()
    
    # Add each brand
    for brand_name, restaurants in all_data.items():
        if not restaurants:
            continue
        
        lats, lons, texts = [], [], []
        
        for restaurant in restaurants:
            addr = restaurant.get('contactDetail', {}).get('address', {})
            coords = addr.get('coordinates', {})
            lat, lng = coords.get('latitude'), coords.get('longitude')
            
            if lat and lng:
                lats.append(lat)
                lons.append(lng)
                name = restaurant.get('restaurantName', brand_name)
                city = addr.get('city', '')
                state = addr.get('stateCode', '')
                country = addr.get('country', '')
                texts.append(f"<b>{brand_name.upper()}</b><br>{name}<br>{city}, {state}, {country}")
        
        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            text=texts,
            name=brand_name.replace('_', ' ').title(),
            mode='markers',
            marker=dict(
                size=6,  # Bigger markers
                color=BRAND_COLORS.get(brand_name, '#808080'),
                opacity=0.8,
                line=dict(width=0.5, color='rgba(255,255,255,0.4)')
            ),
            hovertemplate='%{text}<extra></extra>'
        ))
    
    # Dark theme globe
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor="#1a1a1a",
        coastlinecolor="#404040",
        showocean=True,
        oceancolor="#0a0a0a",
        showcountries=True,
        countrycolor="#303030",
        countrywidth=0.5,
        showlakes=True,
        lakecolor="#0a0a0a",
        bgcolor="#000000"
    )
    
    fig.update_layout(
        title=dict(
            text='<b>Darden Restaurants Worldwide</b><br><sub>2,353 Locations Across 10 Brands</sub>',
            x=0.5,
            xanchor='center',
            font=dict(size=24, color='white')
        ),
        height=900,
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.7)',
            bordercolor='#404040',
            borderwidth=1,
            font=dict(color='white', size=11)
        ),
        font=dict(color='white')
    )
    
    fig.write_html('darden_dark_globe.html')
    
    print("✓ Dark theme globe created: darden_dark_globe.html")
    print("✓ Features:")
    print("  - Dark background for modern look")
    print("  - Tiny markers (size 3)")
    print("  - Rotate by dragging")
    print("  - Zoom with scroll wheel")
    print("  - Toggle brands in legend")
    print(f"✓ Total locations: {sum(len(r) for r in all_data.values())}")

if __name__ == "__main__":
    create_dark_globe()
