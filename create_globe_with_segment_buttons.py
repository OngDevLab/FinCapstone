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

SEGMENTS = {
    'Olive Garden': ['olivegarden'],
    'LongHorn Steakhouse': ['longhornsteakhouse'],
    'Fine Dining': ['ruthschris', 'thecapitalgrille', 'eddiev'],
    'Other Business': ['cheddars', 'chuys', 'yardhouse', 'bahamabreeze', 'seasons52']
}

def create_globe_with_buttons():
    """Create globe with segment buttons + individual brand toggles"""
    
    with open('all_darden_locations_with_franchises.json', 'r') as f:
        all_data = json.load(f)
    
    fig = go.Figure()
    
    # Track which brands belong to which segment
    brand_to_segment = {}
    for segment, brands in SEGMENTS.items():
        for brand in brands:
            brand_to_segment[brand] = segment
    
    # Add each brand as separate trace
    for brand_name, restaurants in all_data.items():
        if not restaurants:
            continue
        
        segment = brand_to_segment.get(brand_name, 'Other')
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
            name=brand_name.replace('_', ' ').title(),
            mode='markers',
            marker=dict(
                size=6,
                color=BRAND_COLORS.get(brand_name, '#808080'),
                opacity=0.8,
                line=dict(width=0.5, color='rgba(255,255,255,0.4)')
            ),
            hovertemplate='%{text}<extra></extra>',
            meta={'segment': segment}  # Store segment info
        ))
    
    # Create visibility arrays for each segment button
    all_visible = [True] * len(all_data)
    
    buttons = []
    
    # "All" button
    buttons.append(dict(
        label="All Brands",
        method="update",
        args=[{"visible": all_visible}]
    ))
    
    # Segment buttons
    for segment_name, segment_brands in SEGMENTS.items():
        visible = [brand in segment_brands for brand in all_data.keys()]
        buttons.append(dict(
            label=segment_name,
            method="update",
            args=[{"visible": visible}]
        ))
    
    # Dark theme globe
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
        showsubunits=True,
        subunitcolor="#606060",
        subunitwidth=0.5,
        bgcolor="#000000",
        resolution=110
    )
    
    fig.update_layout(
        title=dict(
            text='<b>Darden Restaurants</b><br><sub>Use buttons to filter by segment | Click legend to toggle brands</sub>',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='white')
        ),
        height=900,
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.72,  # Slightly lower to avoid overlap
            xanchor="left",
            x=0.017,
            bgcolor='rgba(0,0,0,0.8)',
            bordercolor='#404040',
            borderwidth=1,
            font=dict(color='white', size=10),
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                x=0.01,
                y=0.99,
                xanchor="left",
                yanchor="top",
                bgcolor='rgba(0,0,0,0.9)',
                bordercolor='#606060',
                borderwidth=2,
                font=dict(color='white', size=12),
                active=0,
                showactive=True,  # Show which button is active
                buttons=buttons,
                pad=dict(r=10, t=10, b=10, l=10)
            )
        ],
        font=dict(color='white')
    )
    
    fig.write_html('darden_globe_with_buttons.html')
    
    # Add custom CSS to fix button highlighting
    with open('darden_globe_with_buttons.html', 'r') as f:
        html = f.read()
    
    custom_css = """
    <style>
    /* Fix active button styling - target the rect element */
    .updatemenu-item-rect[style*="fill: rgb(244, 250, 255)"] {
        fill: rgba(138, 43, 226, 0.8) !important;
    }
    .updatemenu-item-rect:hover {
        fill: rgba(100, 100, 100, 0.8) !important;
    }
    </style>
    """
    
    html = html.replace('</head>', custom_css + '</head>')
    
    with open('darden_globe_with_buttons.html', 'w') as f:
        f.write(html)
    
    print("✓ Globe with segment buttons created: darden_globe_with_buttons.html")
    print("\n✓ Controls:")
    print("  BUTTONS (top left):")
    print("    - All Brands: Show everything")
    print("    - Olive Garden: Show only Olive Garden")
    print("    - LongHorn Steakhouse: Show only LongHorn")
    print("    - Fine Dining: Show only fine dining brands")
    print("    - Other Business: Show only other brands")
    print("\n  LEGEND (left side):")
    print("    - Click any brand: Toggle that brand on/off")
    print("    - Double-click: Isolate that brand")
    print("\n✓ Use buttons for segment selection, legend for individual brands!")

if __name__ == "__main__":
    create_globe_with_buttons()
