from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BookableUnit(Base):
    __tablename__ = 'bookable_unit'

    id = Column(Integer, primary_key=True) # Bookable Unit id
    product_id = Column(Integer, index=True)
    date = Column(Date, index=True)
    count_available_bookings = Column(Integer) # Renamed; From capacity
    count_optional_bookings = Column(Integer) # Renamed; From capacity
    feature_bedrooms = Column(Integer) # From bookings; every product_id has the same feature_1 value


class Booking(Base):
    __tablename__ = 'bookings'

    # TODO: Drop duplicates first
    id = Column(Integer, primary_key=True, index=True) # Prüfen, ob selbst vergeben oder übernehmen
    booking_id = Column(Integer) # Renamed bkg to booking # TODO: set unique=True?!
    bookable_unit_id = Column(Integer, ForeignKey('bookable_units.id'))

    booking_creation_date = Column(Date) # Convert to Date Object
    status = Column(String) # Filter out cancelled bookings
    gross_revenue = Column(Float)
    net_revenue = Column(Float)
    discount_amount = Column(Float)
    base_currency = Column(String)
    booking_nights = Column(Integer) # Renamed
    # No feature_2


class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, index=True) # Create a new one
    bookable_unit_id = Column(Integer, ForeignKey('bookable_units.id')) # Is the original 'id' column
    current_price = Column(Float)
    length_of_stay = Column(String) # String because of XN

