# backend/app/models/itinerary.py

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class ItineraryItem(Base):  # <-- Renamed to match your import
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    trip = relationship("Trip", back_populates="itinerary_items")
