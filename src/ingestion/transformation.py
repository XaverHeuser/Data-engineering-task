def transform_data(cur):
    """This function includes the trasformation logic."""
    print(10 * '=')
    print('Starting data transformation ...')

    try:
        # Drop existing data for daily refresh
        cur.execute('TRUNCATE TABLE bookings, prices, bookable_units CASCADE')

        # Tranformation for bookable_units
        cur.execute(
            """
            INSERT INTO bookable_units (id, product_id, date, count_available_bookings, count_optional_bookings)
            SELECT
                id,
                product_id,
                TO_DATE(calendar_date::text, 'YYYYMMDD'),
                is_bookable,
                is_option
            FROM staging_capacity
            """
        )

        # Transformation for prices
        cur.execute(
            """
            INSERT INTO prices (bookable_unit_id, current_price, length_of_stay)
            SELECT
                id,
                current_price,
                length_of_stay
            FROM staging_prices
            """
        )

        # Transformation for bookings
        cur.execute(
            """
            INSERT INTO bookings (booking_id, bookable_unit_id, booking_creation_date, status, gross_revenue, net_revenue, discount_amount, base_currency, booking_nights, feature_bedrooms)
            SELECT DISTINCT ON (bkg.bkg_id)
                bkg.bkg_id,
                bu.id,
                TO_DATE(bkg.booking_creation_date::text, 'YYYYMMDD'),
                bkg.status,
                bkg.gross_revenue,
                bkg.net_revenue,
                bkg.discount_amount,
                bkg.base_currency,
                bkg.bkg_nights,
                NULLIF(regexp_replace(feature_1, '[^0-9]', '', 'g'), '')::INTEGER
            FROM staging_bookings bkg
            JOIN bookable_units bu ON bkg.product_id = bu.product_id
                AND TO_DATE(bkg.date::text, 'YYYYMMDD') = bu.date
            WHERE LOWER(bkg.status) != 'cancelled'
            """
        )

    except Exception as e:
        print(f'Error during data transformation: {e}')
        raise
