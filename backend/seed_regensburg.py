from app import create_app
from app.extensions import db
from app.models.poi import PointOfInterest

app = create_app()
app.app_context().push()

regensburg_pois = [
    PointOfInterest(
        name="Regensburg Cathedral (Dom St. Peter)",
        description="A stunning Gothic cathedral and symbol of the city.",
        latitude=49.0194,
        longitude=12.0976,
        location="Regensburg",
        interests=["architecture", "religion", "history"],
        duration_minutes=60,
        opening_time="09:00",
        closing_time="17:00",
        estimated_cost=0.0,
        price_range="Free"
    ),
    PointOfInterest(
        name="Stone Bridge (Steinerne Brücke)",
        description="12th-century bridge offering great views of the Danube and the old town.",
        latitude=49.0205,
        longitude=12.0957,
        location="Regensburg",
        interests=["sightseeing", "history", "walking"],
        duration_minutes=30,
        opening_time="00:00",
        closing_time="23:59",
        estimated_cost=0.0,
        price_range="Free"
    ),
    PointOfInterest(
        name="Old Town Hall (Altes Rathaus)",
        description="Historic town hall with guided tours of the medieval torture chamber and courtroom.",
        latitude=49.0197,
        longitude=12.0971,
        location="Regensburg",
        interests=["history", "culture", "architecture"],
        duration_minutes=45,
        opening_time="10:00",
        closing_time="16:00",
        estimated_cost=5.0,
        price_range="€"
    ),
    PointOfInterest(
        name="Thurn und Taxis Palace",
        description="Lavish Baroque palace with guided tours and a museum.",
        latitude=49.0157,
        longitude=12.0913,
        location="Regensburg",
        interests=["royalty", "culture", "architecture"],
        duration_minutes=90,
        opening_time="10:00",
        closing_time="17:00",
        estimated_cost=10.0,
        price_range="€€"
    ),
    PointOfInterest(
        name="Danube Riverside Walk",
        description="Peaceful walking path along the Danube with scenic views.",
        latitude=49.0200,
        longitude=12.0950,
        location="Regensburg",
        interests=["nature", "relaxation", "walking"],
        duration_minutes=45,
        opening_time="00:00",
        closing_time="23:59",
        estimated_cost=0.0,
        price_range="Free"
    ),
]

try:
    db.session.bulk_save_objects(regensburg_pois)
    db.session.commit()
    print("✅ Regensburg POIs seeded successfully.")
except Exception as e:
    db.session.rollback()
    print(f"❌ Error seeding Regensburg POIs: {e}")
