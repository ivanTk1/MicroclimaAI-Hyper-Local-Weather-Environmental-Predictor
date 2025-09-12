import pandas as pd
import folium
from folium.features import DivIcon
from districts import districts
from utils import current_time_rounded
from branca.colormap import LinearColormap

# Load CSV data
sf_df = pd.read_csv("sf_microclimate_data.csv", sep="\t")

# Convert temperature column from C → F
sf_df["temperature_F"] = sf_df["temperature_C"] * 9/5 + 32

# Get current time (rounded)
current_time = current_time_rounded()

# Create folium map
sf_map = folium.Map(location=[37.7749, -122.4194], zoom_start=12, tiles="CartoDB positron")

# Find min/max temps for color scale (in °F)
min_temp, max_temp = sf_df["temperature_F"].min(), sf_df["temperature_F"].max()
colormap = LinearColormap(
    colors=["blue", "lightblue", "yellow", "orange", "red"],
    vmin=min_temp,
    vmax=max_temp,
    caption="Temperature (°F)"   # <-- changed caption
)
colormap.add_to(sf_map)

# Loop through districts
for district, coords in districts.items():
    row = sf_df[(sf_df["district"] == district) & (sf_df["time"] == current_time)]
    
    if not row.empty:
        temp_F = row.iloc[0]["temperature_F"]
        color = colormap(temp_F)

        # Draw a colored circle
        folium.CircleMarker(
            location=coords,
            radius=25,  # size of circle
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
        ).add_to(sf_map)

        # Add text label (temperature value in °F)
        folium.map.Marker(
            coords,
            icon=DivIcon(
                icon_size=(50, 50),     # make a square area
                icon_anchor=(25, 25),   # anchor at the middle of that square
                html=f'''
                <div style="
                    width:50px;
                    height:50px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:14px;
                    font-weight:bold;
                    color:black;
                    text-align:center;
                ">
                    {temp_F:.1f}°F
                </div>
                ''',
            )
        ).add_to(sf_map)
    else:
        # Show "No data" as gray circle
        folium.CircleMarker(
            location=coords,
            radius=20,
            color="gray",
            fill=True,
            fill_color="gray",
            fill_opacity=0.6,
        ).add_to(sf_map)


# Save map
sf_map.save("sf_district_temps.html")
print("Map saved as sf_district_temps.html")
