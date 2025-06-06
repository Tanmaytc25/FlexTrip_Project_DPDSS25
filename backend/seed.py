from app import create_app
from app.extensions import db
from app.models.poi import PointOfInterest

app = create_app()

with app.app_context():
    db.session.query(PointOfInterest).delete()  # Optional: clear existing POIs

    pois = [
        PointOfInterest(
            name="Munich Residenz",
            description="Former royal palace of the Wittelsbach monarchs.",
            latitude=48.1391,
            longitude=11.5802,
            category="Historical Site",
            location="Munich",
            duration_minutes=90,
            estimated_cost=12,
            price_range="low",
            opening_time="09:00",
            closing_time="18:00",
            interests=["history", "architecture"]
        ),
        PointOfInterest(
            name="Englischer Garten",
            description="One of the largest urban parks in the world.",
            latitude=48.1590,
            longitude=11.6036,
            category="Park",
            location="Munich",
            duration_minutes=120,
            estimated_cost=0,
            price_range="free",
            opening_time="06:00",
            closing_time="21:00",
            interests=["nature", "relaxation"]
        ),
        PointOfInterest(
            name="Deutsches Museum",
            description="World's largest museum of science and technology.",
            latitude=48.1303,
            longitude=11.5820,
            category="Museum",
            location="Munich",
            duration_minutes=120,
            estimated_cost=14,
            price_range="medium",
            opening_time="09:00",
            closing_time="17:00",
            interests=["science", "history"]
        ),
    ]

    db.session.bulk_save_objects(pois)
    db.session.commit()

    print("✅ Sample POIs seeded successfully.")
