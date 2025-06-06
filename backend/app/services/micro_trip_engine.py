# app/services/micro_trip_engine.py

from app.models.simulated_place import SimulatedPlace
from app.services.location_utils import calculate_distance

def generate_micro_trip(user_location, interests, all_places, max_distance_km=10):
    """
    Suggest micro-trips based on user location, interests, and a list of available places.

    Args:
        user_location (tuple): A tuple of (latitude, longitude) representing the user's current location.
        interests (list): A list of category strings the user is interested in.
        all_places (list): A list of SimulatedPlace objects.
        max_distance_km (float): Maximum allowed distance for a place to be considered nearby.

    Returns:
        list: Filtered list of suggested SimulatedPlace objects.
    """
    suggested = []

    for place in all_places:
        if place.category in interests:
            distance = calculate_distance(user_location, (place.latitude, place.longitude))
            if distance <= max_distance_km:
                suggested.append(place)

    return suggested
