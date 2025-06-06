from calendar_utils import add_trip_events
import requests

# Replace this if you're testing inside the container
API_URL = "http://localhost:5000/api/microtrip/generate"

payload = {
    "current_location": "Munich",         # ✅ Use any city you seeded
    "interests": ["history", "architecture"],
    "budget": 50                          # optional
}

response = requests.post(API_URL, json=payload)
data = response.json()

recommended_pois = data.get("recommended", [])
if recommended_pois:
    print(f"✅ Retrieved {len(recommended_pois)} POIs. Adding to calendar...")
    add_trip_events(recommended_pois)
    print("✅ Events added to Google Calendar.")
else:
    print("❌ No POIs received from API.")
