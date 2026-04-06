import io

import numpy as np
import pandas as pd

from src.database.database import close_database_connection, connect_to_database


COLS_TO_SAVE = [
    'id',
    'product_id',
    'date',
    'count_available_bookings',
    'count_optional_bookings',
    'total_available_bookings',
    'max_capacity',
    'occupancy_rate',
    'days_until_start',
    'days_factor',
    'price_adjustment_pct',
]


def price_recommendations():
    """This function calculates price recommendations for each product."""
    print(10 * '=')
    print('Start calculating price recommendations ...')

    cur, conn = connect_to_database()

    # Get data from bookable_units table
    cur.execute(
        'SELECT id, product_id, date, count_available_bookings, count_optional_bookings FROM bookable_units'
    )
    data = cur.fetchall()

    # Create dataframe
    column_names = [desc[0] for desc in cur.description]
    df_bookable_units = pd.DataFrame(data, columns=column_names)
    print(f'Shape of df_bookable_units: {df_bookable_units.shape}')

    if df_bookable_units.empty:
        print('No data found in bookable_units table')
        close_database_connection(cur, conn)
        return

    # Handle dates
    df_bookable_units['date'] = pd.to_datetime(df_bookable_units['date'])
    current_date = pd.Timestamp.now().normalize()
    print(f'Current date: {current_date}')

    # Calculate max capacity per product
    df_bookable_units['total_available_bookings'] = (
        df_bookable_units['count_available_bookings']
        + df_bookable_units['count_optional_bookings']
    )
    df_bookable_units['max_capacity'] = df_bookable_units.groupby('product_id')[
        'total_available_bookings'
    ].transform('max')

    # Get data in future
    df_future = df_bookable_units[df_bookable_units['date'] >= current_date].copy()
    print(f'Len of df_future: {len(df_future)}')

    # Calculate current occupancy rate
    occupancy_numerator = (
        df_future['max_capacity'] - df_future['total_available_bookings']
    )
    df_future['occupancy_rate'] = np.where(
        df_future['max_capacity'] > 0,
        occupancy_numerator / df_future['max_capacity'],
        0.0,
    )

    # Calculate days until travel start
    df_future['days_until_start'] = (df_future['date'] - current_date).dt.days
    df_future['days_factor'] = df_future['days_until_start'] / 300

    # Apply formula for price adjustment
    df_future['price_adjustment_pct'] = (
        0.15
        * (df_future['occupancy_rate'] - 0.5)
        * (0.5 + df_future['days_factor'])
        * 100
    )

    # Delete existing data in table
    cur.execute('TRUNCATE TABLE recommendations RESTART IDENTITY')
    try:
        output = io.StringIO()
        df_future[COLS_TO_SAVE].to_csv(output, index=False, header=True)
        output.seek(0)

        copy_sql = f'COPY recommendations ({", ".join(COLS_TO_SAVE)}) FROM STDIN WITH (FORMAT CSV, HEADER True)'

        with cur.copy(copy_sql) as c:
            while data := output.read(8192):
                c.write(data)

        conn.commit()
        print('Successfully calculated and stored price recommendations')

    except Exception as e:
        conn.rollback()
        print(f'Error saving to database: {e}')

    finally:
        close_database_connection(cur, conn)


def calculate_max_recommendation():
    """This function calculates the max price recommendation."""
    print(10 * '=')
    print('Start calculating max recommendation ...')

    cur, conn = connect_to_database()

    try:
        cur.execute(
            """
            SELECT * FROM recommendations
            ORDER BY price_adjustment_pct DESC
            LIMIT 1
            """
        )
        result = cur.fetchone()

        if not result:
            print('No recommendations found in the database.')
            close_database_connection(cur, conn)
            return

        headers = [desc[0] for desc in cur.description]
        max_recommendation = dict(zip(headers, result, strict=False))
        print(f'max_recommendation: {max_recommendation}')
        return max_recommendation

    except Exception as e:
        print(f'Error fetching max recommendation from database: {e}')
        return {'error': str(e)}

    finally:
        close_database_connection(cur, conn)
