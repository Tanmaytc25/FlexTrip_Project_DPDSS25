# backend/app/scripts/seed_real_pois.py

from app.extensions import db
from app.models.poi import PointOfInterest

def seed_pois():
    pois = [
        {"name": "Eiffel Tower", "location": "Paris", "category": "Monument"},
        {"name": "Louvre Museum", "location": "Paris", "category": "Museum"},
        {"name": "Statue of Liberty", "location": "New York", "category": "Monument"},
        {"name": "Central Park", "location": "New York", "category": "Park"},
    ]

    for poi_data in pois:
        poi = PointOfInterest(**poi_data)
        db.session.add(poi)
    
    db.session.commit()
    print(f"{len(pois)} points of interest seeded.")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_pois()
