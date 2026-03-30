from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Float,
    Identity,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class BookableUnit(Base):
    # From capacity table
    __tablename__ = 'bookable_units'

    id = Column(String, primary_key=True)  # Bookable Unit id
    product_id = Column(String, index=True)
    date = Column(Date, index=True)
    count_available_bookings = Column(Integer)  # Renamed; From capacity
    count_optional_bookings = Column(Integer)  # Renamed; From capacity
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Booking(Base):
    # From bookings table + bookable_unit (id)
    __tablename__ = 'bookings'

    booking_id = Column(BigInteger)  # Renamed bkg to booking
    bookable_unit_id = Column(String, index=True)
    booking_creation_date = Column(Date)  # Convert to Date Object
    status = Column(String)  # Filter out cancelled bookings
    gross_revenue = Column(Float)
    net_revenue = Column(Float)
    discount_amount = Column(Float)
    base_currency = Column(String)
    booking_nights = Column(Integer)  # Renamed
    feature_bedrooms = Column(Integer)  # Renamed feature_1
    id = Column(BigInteger, Identity(always=False), primary_key=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Price(Base):
    # From prices table
    __tablename__ = 'prices'

    bookable_unit_id = Column(String, index=True)  # Is the original 'id' column
    current_price = Column(Float)
    length_of_stay = Column(String)  # String because of XN
    id = Column(BigInteger, Identity(always=False), primary_key=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
