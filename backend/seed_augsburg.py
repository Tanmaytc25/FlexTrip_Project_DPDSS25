from app import create_app
from app.extensions import db
from app.models.poi import PointOfInterest

app = create_app()
app.app_context().push()

augsburg_pois = [
    PointOfInterest(
        name="Fuggerei",
        description="World’s oldest social housing complex still in use, founded in 1521.",
        latitude=48.3651,
        longitude=10.9037,
        location="Augsburg",
        interests=["history", "architecture", "culture"],
        duration_minutes=60,
        opening_time="09:00",
        closing_time="18:00",
        estimated_cost=6.5,
        price_range="€"
    ),
    PointOfInterest(
        name="Augsburg Cathedral",
        description="A magnificent Romanesque cathedral dating back to the 11th century.",
        latitude=48.3731,
        longitude=10.8998,
        location="Augsburg",
        interests=["architecture", "religion", "history"],
        duration_minutes=45,
        opening_time="08:00",
        closing_time="18:00",
        estimated_cost=0.0,
        price_range="Free"
    ),
    PointOfInterest(
        name="Augsburg Puppet Theater Museum",
        description="Unique museum dedicated to marionettes, including the famous 'Augsburger Puppenkiste'.",
        latitude=48.3674,
        longitude=10.9025,
        location="Augsburg",
        interests=["family", "arts", "entertainment"],
        duration_minutes=60,
        opening_time="10:00",
        closing_time="17:00",
        estimated_cost=5.0,
        price_range="€"
    ),
    PointOfInterest(
        name="Botanical Garden Augsburg",
        description="Serene garden with themed areas, perfect for a relaxing nature walk.",
        latitude=48.3417,
        longitude=10.9314,
        location="Augsburg",
        interests=["nature", "relaxation", "walking"],
        duration_minutes=90,
        opening_time="09:00",
        closing_time="19:00",
        estimated_cost=3.5,
        price_range="€"
    ),
    PointOfInterest(
        name="Maximilianstraße",
        description="Elegant boulevard with historical buildings, shops, and cafes.",
        latitude=48.3670,
        longitude=10.8980,
        location="Augsburg",
        interests=["shopping", "food", "culture"],
        duration_minutes=60,
        opening_time="10:00",
        closing_time="20:00",
        estimated_cost=0.0,
        price_range="€ – €€€"
    ),
]

try:
    db.session.bulk_save_objects(augsburg_pois)
    db.session.commit()
    print("✅ Augsburg POIs seeded successfully.")
except Exception as e:
    db.session.rollback()
    print(f"❌ Error seeding Augsburg POIs: {e}")
