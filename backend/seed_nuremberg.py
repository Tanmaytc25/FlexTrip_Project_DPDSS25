from app import create_app
from app.extensions import db
from app.models.poi import PointOfInterest

app = create_app()
app.app_context().push()

nuremberg_pois = [
    PointOfInterest(
        name="Nuremberg Castle",
        description="A group of medieval fortified buildings dating back to the Holy Roman Empire.",
        latitude=49.4582,
        longitude=11.0773,
        location="Nuremberg",
        interests=["history", "architecture"],
        duration_minutes=90,
        opening_time="09:00",
        closing_time="18:00",
        estimated_cost=7.0,
        price_range="€"
    ),
    PointOfInterest(
        name="Documentation Center Nazi Party Rally Grounds",
        description="Museum on the history of the Nazi regime with permanent and temporary exhibitions.",
        latitude=49.4236,
        longitude=11.1181,
        location="Nuremberg",
        interests=["history", "education"],
        duration_minutes=120,
        opening_time="10:00",
        closing_time="18:00",
        estimated_cost=6.0,
        price_range="€"
    ),
    PointOfInterest(
        name="Nuremberg Toy Museum",
        description="Museum showcasing toys from the past 600 years.",
        latitude=49.4551,
        longitude=11.0772,
        location="Nuremberg",
        interests=["culture", "family", "nostalgia"],
        duration_minutes=60,
        opening_time="10:00",
        closing_time="17:00",
        estimated_cost=4.0,
        price_range="€"
    ),
    PointOfInterest(
        name="Nuremberg Zoo",
        description="Large zoo with over 300 animal species in spacious enclosures.",
        latitude=49.4270,
        longitude=11.1520,
        location="Nuremberg",
        interests=["animals", "family", "nature"],
        duration_minutes=120,
        opening_time="09:00",
        closing_time="17:00",
        estimated_cost=16.0,
        price_range="€€"
    ),
    PointOfInterest(
        name="Hauptmarkt",
        description="Historic market square with shops and the iconic Schöner Brunnen fountain.",
        latitude=49.4556,
        longitude=11.0787,
        location="Nuremberg",
        interests=["shopping", "culture", "food"],
        duration_minutes=45,
        opening_time="09:00",
        closing_time="20:00",
        estimated_cost=10.0,
        price_range="€€"
    ),
]

try:
    db.session.bulk_save_objects(nuremberg_pois)
    db.session.commit()
    print("✅ Nuremberg POIs seeded successfully.")
except Exception as e:
    db.session.rollback()
    print(f"❌ Error seeding Nuremberg POIs: {e}")
