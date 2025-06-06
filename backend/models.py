from sqlalchemy import Column, Integer, String, Time, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class POI(Base):
    __tablename__ = 'pois'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text)
    interests = Column(String)
    estimated_cost = Column(Integer)
    price_range = Column(String)
    duration_minutes = Column(Integer)
    opening_time = Column(Time)
    closing_time = Column(Time)
