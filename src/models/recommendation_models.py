from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Recommendations(Base):
    __tablename__ = 'recommendations'

    id = Column(String, primary_key=True)  # Is bookable_unit_id
    product_id = Column(String, index=True)
    date = Column(Date, index=True)
    count_available_bookings = Column(Integer)
    count_optional_bookings = Column(Integer)
    total_available_bookings = Column(Integer)
    max_capacity = Column(Integer)
    occupancy_rate = Column(Float)
    days_until_start = Column(Integer)
    days_factor = Column(Float)
    price_adjustment_pct = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
