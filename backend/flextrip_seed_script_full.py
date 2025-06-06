import random
from datetime import time
from app import create_app
from app.extensions import db
from app.models.poi import PointOfInterest

app = create_app()
app.app_context().push()

sample_categories = ['food', 'culture', 'nature', 'religion', 'shopping', 'arts', 'history', 'nightlife']
sample_locations = ['Munich', 'Nuremberg', 'Regensburg', 'Augsburg', 'Passau', 'Landshut', 'Bamberg', 'Salzburg', 'Deggendorf', 'Pfarrkirchen', 'Eggenfelden']
sample_interests_pool = ['nature', 'history', 'culture', 'architecture', 'art', 'food', 'nightlife', 'shopping', 'religion', 'sports']

def random_time(start_hour=8, end_hour=18):
    hour = random.randint(start_hour, end_hour)
    minute = random.choice([0, 15, 30, 45])
    return time(hour=hour, minute=minute)

def generate_poi(index):
    return PointOfInterest(
        name=f"Sample POI {index + 1}",
        description=f"This is a detailed description of Sample POI {index + 1}.",
        latitude=round(random.uniform(48.0, 49.5), 6),
        longitude=round(random.uniform(11.0, 13.5), 6),
        category=random.choice(sample_categories),
        location=random.choice(sample_locations),
        duration_minutes=random.choice([30, 45, 60, 75, 90]),
        estimated_cost=round(random.uniform(0, 25), 2),
        price_range=random.choice(['€', '€€', '€€€']),
        interests=random.sample(sample_interests_pool, k=random.randint(1, 3)),
        opening_time=random_time(8, 11),
        closing_time=random_time(17, 23)
    )

try:
    pois = [generate_poi(i) for i in range(105)]
    db.session.bulk_save_objects(pois)
    db.session.commit()
    print("🎉 Successfully inserted 105 POIs!")
except Exception as e:
    db.session.rollback()
    print(f"❌ Failed to insert POIs: {e}")
