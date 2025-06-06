# backend/app/models.py

from .models.user import User
from .models.trip import Trip
from .models.accommodation import Accommodation
from .models.poi import POI
from .models.simulated_place import SimulatedPlace
from .models.oauth_token import OAuthToken
from .models.emergency import Emergency
from .models.itinerary import Itinerary

__all__ = [
    'User',
    'Trip',
    'Accommodation',
    'POI',
    'SimulatedPlace',
    'OAuthToken',
    'Emergency',
    'Itinerary',
]
