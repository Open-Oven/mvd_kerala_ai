import pandas as pd
import numpy as np
import geopandas as gop
from geopy.geocoders import Nominatim
import folium as fo


# Read csv

df = pd.read_csv("mvd_ai_cams.csv", encoding='utf-8')

# convert just columns "Lat" and "Long"
df[["Lat", "Long"]] = df[["Lat", "Long"]].apply(pd.to_numeric)

# drop nans
df1 = df.dropna()

# Add map layer
n = fo.Map(location=[8, 77], tiles='openstreetmap', zoom_start=6)

# add marker one by one on the map
for i in range(0,len(df1)):
    html=f""" 
        <h1> MVD,Kerala - AI camera location  </h1>
        <h2> {df1.iloc[i]['Unique_id']}</h2>
        <h3> District: {df1.iloc[i]['District']}</h3>
        <h3 style="color:red;"> Location: {df1.iloc[i]['Location']}</h3>
        <h4> Type:  {df1.iloc[i]['Type']}</h4>
        
        <p>Made with ❤️ <a href="https://arungopi.gitlab.io">Arun Gopinath.</a> 
        <br> Take a look at <a href="https://github.com/Open-Oven/mvd_kerala_ai">Source code. </br> 
        </p>
        """
    iframe = fo.IFrame(html=html, width=200, height=200)
    popup = fo.Popup(iframe, max_width=2650)
    fo.Marker(
        location=[df1.iloc[i]['Lat'], df1.iloc[i]['Long']],
        popup=popup,
        icon=fo.DivIcon(html=f"""
            <div>
            <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" fill="currentColor" class="bi bi-camera" viewBox="0 0 16 16">
            <path d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1v6zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4H2z"/>
            <path d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5zm0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0z"/>
            </svg>
            </div>""")
    ).add_to(n)

# Add district boundary
fo.GeoJson('https://raw.githubusercontent.com/geohacker/kerala/master/geojsons/district.geojson', name="geojson").add_to(n)

fo.LayerControl().add_to(n)
# Save the map 

n.save('index.html')


