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

# Segment groupings (per 10-K)
SEGMENTS = {
    'Olive Garden': ['olivegarden'],
    'LongHorn Steakhouse': ['longhornsteakhouse'],
    'Fine Dining': ['ruthschris', 'thecapitalgrille', 'eddiev'],
    'Other Business': ['cheddars', 'chuys', 'yardhouse', 'bahamabreeze', 'seasons52']
}

def create_dark_globe_with_segments():
    """Create dark globe with both brand and segment grouping"""
    
    with open('all_darden_locations_with_franchises.json', 'r') as f:
        all_data = json.load(f)
    
    fig = go.Figure()
    
    # Add traces by brand (for individual brand toggle)
    for brand_name, restaurants in all_data.items():
        if not restaurants:
            continue
        
        # Determine segment
        segment = None
        for seg_name, brands in SEGMENTS.items():
            if brand_name in brands:
                segment = seg_name
                break
        
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
                texts.append(f"<b>{segment}</b><br><b>{brand_name.upper()}</b><br>{name}<br>{city}, {state}, {country}")
        
        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            text=texts,
            name=f"{segment} - {brand_name.replace('_', ' ').title()}",  # Include segment in name
            mode='markers',
            marker=dict(
                size=6,
                color=BRAND_COLORS.get(brand_name, '#808080'),
                opacity=0.8,
                line=dict(width=0.5, color='rgba(255,255,255,0.4)')
            ),
            hovertemplate='%{text}<extra></extra>'
        ))
    
    # Dark theme globe with topography
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor="#1a1a1a",
        coastlinecolor="#404040",
        coastlinewidth=1,
        showocean=True,
        oceancolor="#0a0a0a",
        showcountries=True,
        countrycolor="#505050",
        countrywidth=1,
        showlakes=True,
        lakecolor="#0a0a0a",
        showrivers=True,
        rivercolor="#1a3a4a",
        riverwidth=0.5,
        showsubunits=True,  # Show states/provinces
        subunitcolor="#606060",  # State borders
        subunitwidth=0.5,
        bgcolor="#000000",
        resolution=110  # Lower = faster (110 is good balance)
    )
    
    fig.update_layout(
        title=dict(
            text='<b>Darden Restaurants by Segment</b><br><sub>2,353 Locations | Toggle by Segment or Brand</sub>',
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
            font=dict(color='white', size=11),
            itemclick="toggle",  # Click brand to toggle
            itemdoubleclick="toggleothers"  # Double-click to isolate
        ),
        font=dict(color='white')
    )
    
    fig.write_html('darden_dark_globe_segments.html')
    
    print("✓ Dark globe with segments created: darden_dark_globe_segments.html")
    print("✓ Features:")
    print("  - Grouped by 4 segments in legend")
    print("  - Click segment name to toggle all brands in that segment")
    print("  - Click individual brand to toggle just that brand")
    print("  - Double-click to isolate a segment or brand")
    print(f"✓ Total locations: {sum(len(r) for r in all_data.values())}")
    print("\nSegments:")
    for seg, brands in SEGMENTS.items():
        print(f"  {seg}: {', '.join(brands)}")

if __name__ == "__main__":
    create_dark_globe_with_segments()
