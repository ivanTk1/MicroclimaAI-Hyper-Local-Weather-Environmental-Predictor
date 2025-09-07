import pandas as pd
import time
from data_fetcher import fetch_sf_microclimate

# List of SF districts with coordinates
districts = {
    "Mission": (37.7599, -122.4148),
    "SOMA": (37.7786, -122.4057),
    "Sunset": (37.7534, -122.4940),
    "Marina": (37.8033, -122.4368),
    "Richmond": (37.7802, -122.4869),
    "Chinatown": (37.7941, -122.4078),
    "North Beach": (37.8021, -122.4107),
    "Castro": (37.7625, -122.4350),
    "Haight-Ashbury": (37.7701, -122.4469),
    "Tenderloin": (37.7831, -122.4125)
}

# Loop over all districts and combine data
all_data = []

for name, (lat, lon) in districts.items():
    try:
        df = fetch_sf_microclimate(lat, lon)
        df['district'] = name
        all_data.append(df)
        time.sleep(1)  # small delay to avoid overloading API
    except Exception as e:
        print(f"Error fetching {name}: {e}")

# Combine into a single DataFrame
sf_df = pd.concat(all_data)

# Preview
print(sf_df.head(10000))
print(sf_df['district'].unique())  # Should show all districts
