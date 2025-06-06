from app import create_app
from app.extensions import db
from app.models.poi import PointOfInterest

app = create_app()
app.app_context().push()

# Clear existing POIs for clean seeding (optional)
# db.session.query(PointOfInterest).delete()

munich_pois = [
    PointOfInterest(
        name="Deutsches Museum",
        description="World's largest museum of science and technology.",
        latitude=48.1303,
        longitude=11.5820,
        location="Munich",
        interests=["science", "technology"],
        duration_minutes=90,
        opening_time="09:00",
        closing_time="17:00",
        estimated_cost=14.0,
        price_range="€€"
    ),
    PointOfInterest(
        name="English Garden",
        description="Large public park in the city center, ideal for relaxing walks.",
        latitude=48.1590,
        longitude=11.6036,
        location="Munich",
        interests=["nature", "relaxation"],
        duration_minutes=60,
        opening_time="06:00",
        closing_time="21:00",
        estimated_cost=0.0,
        price_range="Free"
    ),
    PointOfInterest(
        name="BMW Museum",
        description="Explore the history of the BMW brand.",
        latitude=48.1766,
        longitude=11.5593,
        location="Munich",
        interests=["cars", "history"],
        duration_minutes=90,
        opening_time="10:00",
        closing_time="18:00",
        estimated_cost=10.0,
        price_range="€€"
    ),
    PointOfInterest(
        name="Marienplatz",
        description="Central square in the heart of Munich with historical buildings.",
        latitude=48.1374,
        longitude=11.5755,
        location="Munich",
        interests=["history", "architecture"],
        duration_minutes=45,
        opening_time="00:00",
        closing_time="23:59",
        estimated_cost=0.0,
        price_range="Free"
    ),
    PointOfInterest(
        name="Viktualienmarkt",
        description="A daily food market and a square in the center of Munich.",
        latitude=48.1351,
        longitude=11.5769,
        location="Munich",
        interests=["food", "culture"],
        duration_minutes=60,
        opening_time="08:00",
        closing_time="20:00",
        estimated_cost=15.0,
        price_range="€€"
    ),
]

try:
    db.session.bulk_save_objects(munich_pois)
    db.session.commit()
    print("✅ Munich POIs seeded successfully.")
except Exception as e:
    db.session.rollback()
    print(f"❌ Error seeding Munich POIs: {e}")
