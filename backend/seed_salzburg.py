from app import create_app
from app.extensions import db
from app.models.poi import PointOfInterest

app = create_app()
app.app_context().push()

salzburg_pois = [
    PointOfInterest(
        name="Hohensalzburg Fortress",
        description="One of the largest medieval castles in Europe with panoramic city views.",
        latitude=47.7967,
        longitude=13.0476,
        location="Salzburg",
        interests=["history", "architecture", "viewpoints"],
        duration_minutes=90,
        opening_time="09:00",
        closing_time="17:00",
        estimated_cost=12.0,
        price_range="€€"
    ),
    PointOfInterest(
        name="Mozart's Birthplace",
        description="Museum in the house where Mozart was born, filled with personal memorabilia.",
        latitude=47.8009,
        longitude=13.0430,
        location="Salzburg",
        interests=["music", "history", "culture"],
        duration_minutes=60,
        opening_time="09:00",
        closing_time="17:30",
        estimated_cost=11.0,
        price_range="€€"
    ),
    PointOfInterest(
        name="Mirabell Palace and Gardens",
        description="Baroque palace with beautifully landscaped gardens, featured in The Sound of Music.",
        latitude=47.8058,
        longitude=13.0437,
        location="Salzburg",
        interests=["nature", "film", "architecture"],
        duration_minutes=45,
        opening_time="08:00",
        closing_time="18:00",
        estimated_cost=0.0,
        price_range="Free"
    ),
    PointOfInterest(
        name="Getreidegasse",
        description="Historic shopping street with charming old signage and boutiques.",
        latitude=47.8006,
        longitude=13.0427,
        location="Salzburg",
        interests=["shopping", "sightseeing", "walking"],
        duration_minutes=60,
        opening_time="10:00",
        closing_time="19:00",
        estimated_cost=0.0,
        price_range="€ – €€€"
    ),
    PointOfInterest(
        name="Salzach River Promenade",
        description="Relaxing riverside walk with cafes and scenic bridges.",
        latitude=47.8000,
        longitude=13.0440,
        location="Salzburg",
        interests=["relaxation", "walking", "nature"],
        duration_minutes=30,
        opening_time="00:00",
        closing_time="23:59",
        estimated_cost=0.0,
        price_range="Free"
    ),
]

try:
    db.session.bulk_save_objects(salzburg_pois)
    db.session.commit()
    print("✅ Salzburg POIs seeded successfully.")
except Exception as e:
    db.session.rollback()
    print(f"❌ Error seeding Salzburg POIs: {e}")
