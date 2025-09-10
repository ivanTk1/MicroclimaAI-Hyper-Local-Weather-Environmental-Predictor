import requests
import pandas as pd
import time

# Modified fetch function
def fetch_sf_microclimate(latitude, longitude):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        f"&timezone=America/Los_Angeles"
    )
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if 'hourly' not in data:
        raise ValueError(f"No hourly data returned: {data}")
    
    hourly = data['hourly']
    df = pd.DataFrame({
        'temperature_C': hourly['temperature_2m'],
        'humidity_%': hourly['relativehumidity_2m'],
        'wind_speed_m_s': hourly['windspeed_10m']
    })
    df['time'] = pd.to_datetime(hourly['time'])
    df.set_index('time', inplace=True)
    return df

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
# Save all data to a text file
sf_df.to_csv('sf_microclimate_data.csv', sep='\t', index=False)
