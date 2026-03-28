from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class StagingBookings(Base):
    __tablename__ = 'staging_bookings'

    id_new = Column(
        Integer, primary_key=True, index=True
    )  # new unique id for staging table
    id = Column(Integer)  # Original id
    bkg_id = Column(Integer)
    cust_id = Column(Integer)
    product_id = Column(String)
    date = Column(Integer)
    booking_creation_date = Column(Integer)
    status = Column(String)
    cancellation_date = Column(Float)
    gross_revenue = Column(Float)
    net_revenue = Column(Float)
    discount_amount = Column(Float)
    base_currency = Column(String)
    bkg_nights = Column(Integer)
    feature_1 = Column(String)
    feature_2 = Column(String)


class StagingCapacity(Base):
    __tablename__ = 'staging_capacity'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String)
    calendar_date = Column(Integer)
    is_bookable = Column(Integer)
    is_option = Column(Integer)


class StagingPrices(Base):
    __tablename__ = 'staging_prices'

    id_new = Column(
        Integer, primary_key=True, index=True
    )  # new unique id for staging table
    id = Column(Integer)
    product_id = Column(String)
    current_price = Column(Float)
    length_of_stay = Column(String)
