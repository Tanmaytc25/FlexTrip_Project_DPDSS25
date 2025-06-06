import datetime
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key
SERVICE_ACCOUNT_FILE = 'credentials/flextrip-calendar-key.json'

# The calendar ID (usually your own Gmail or a shared calendar ID)
CALENDAR_ID = 'primary'  # You can replace with a specific ID if needed

# Define required scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)


def add_trip_events(trip_data, start_date=None):
    """
    trip_data: List of POIs with 'name', 'duration_minutes', 'opening_time', etc.
    start_date: Optional datetime.date object. Defaults to today.
    """

    if start_date is None:
        start_date = datetime.date.today()

    current_time = datetime.datetime.combine(start_date, datetime.time(hour=9, minute=0))

    for poi in trip_data:
        duration = poi.get("duration_minutes", 60)
        start = current_time
        end = start + datetime.timedelta(minutes=duration)

        event = {
            'summary': poi['name'],
            'location': poi['location'],
            'description': poi['description'],
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'Europe/Berlin',
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'Europe/Berlin',
            },
        }

        event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"✅ Event created: {event_result.get('htmlLink')}")

        current_time = end + datetime.timedelta(minutes=15)  # Buffer between POIs
if __name__ == "__main__":
    sample_trip = [
        {
            "name": "Munich Residenz",
            "description": "Former royal palace of the Wittelsbach monarchs.",
            "location": "Munich",
            "duration_minutes": 90,
            "opening_time": "09:00",
            "closing_time": "18:00"
        },
        {
            "name": "Deutsches Museum",
            "description": "World’s largest museum of science and technology.",
            "location": "Munich",
            "duration_minutes": 120,
            "opening_time": "09:00",
            "closing_time": "17:00"
        }
    ]

    add_trip_events(sample_trip)
