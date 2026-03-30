from sqlalchemy import BigInteger, Column, Float, Identity, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class StagingBookings(Base):
    __tablename__ = 'staging_bookings'

    id = Column(BigInteger)  # Original id -> not unique
    bkg_id = Column(BigInteger)  # Rename
    cust_id = Column(BigInteger)  # Ignore
    product_id = Column(String, index=True)  # Replace with bookable_unit_id
    date = Column(Integer, index=True)  # Replace with bookable_unit_id
    booking_creation_date = Column(Integer)
    status = Column(String)  # Drop cancelled bookings
    cancellation_date = Column(Float)  # Drop because of correlation to status
    gross_revenue = Column(Float)
    net_revenue = Column(Float)
    discount_amount = Column(Float)
    base_currency = Column(String)
    bkg_nights = Column(Integer)  # Rename
    feature_1 = Column(String)  # Rename and convert content to int
    feature_2 = Column(String)  # Ignore
    id_new = Column(
        BigInteger, Identity(always=False), primary_key=True
    )  # new unique id


class StagingCapacity(Base):
    __tablename__ = 'staging_capacity'

    id = Column(String, primary_key=True, index=True)  # bookable_unit_id
    product_id = Column(String, index=True)  # first element of bookable_unit_id
    calendar_date = Column(
        Integer
    )  # second element of bookable_unit_id; Rename and convert
    is_bookable = Column(Integer)  # Rename
    is_option = Column(Integer)  # Rename


class StagingPrices(Base):
    __tablename__ = 'staging_prices'

    id = Column(String, index=True)  # bookable_unit_id -> not unique here
    product_id = Column(String)  # Not needed because of bookable_unit_id
    date = Column(Integer)  # Not needed because of bookable_unit_id
    current_price = Column(Float)
    length_of_stay = Column(String)  # String because of XN
    id_new = Column(
        BigInteger, Identity(always=False), primary_key=True
    )  # new unique id
