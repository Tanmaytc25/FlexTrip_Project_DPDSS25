# backend/app/services/itinerary_generator.py

from app.services.location_utils import calculate_distance
from app.models.simulated_place import SimulatedPlace

def generate_itinerary(user_preferences, available_places):
    itinerary = []
    for place in available_places:
        if place.category in user_preferences.get('interests', []):
            itinerary.append(place)
    return itinerary
