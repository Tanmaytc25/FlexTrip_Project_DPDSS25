from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class PointOfInterest(db.Model):
    __tablename__ = "points_of_interest"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    category = db.Column(db.String)
    location = db.Column(db.String, nullable=False)
    interests = db.Column(db.ARRAY(db.String), nullable=False)  # PostgreSQL ARRAY
    duration_minutes = db.Column(db.Integer)
    opening_time = db.Column(db.String)  # You can use db.Time if you're consistent
    closing_time = db.Column(db.String)
    estimated_cost = db.Column(db.Float)
    price_range = db.Column(db.String)
