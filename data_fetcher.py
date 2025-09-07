import requests
import pandas as pd

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

