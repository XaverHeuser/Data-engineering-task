from src.database.database import close_database_connection, connect_to_database

from .extraction import extract_data
from .load import load_data_to_database
from .transformation import transform_data


def process_ingestion(folder_path: str):
    """This function processes the ingestion of the data to the db."""
    files = extract_data(folder_path)
    if not files:
        print('No files found in the given folder path')
        return
    cur, conn = connect_to_database()

    try:
        # Load every file raw data to the db staging tables
        print(10 * '=')
        print('Start data loading ...')
        for file in files:
            load_data_to_database(file, cur)
        conn.commit()
        print('Raw files successfully loaded and committed')

        # Transform data from staging tables to final tables
        transform_data(cur)
        conn.commit()
        print('Transformation successfully committed')

    except Exception as e:
        print(f'Error: {e}. Transaction rolled back.')

    finally:
        close_database_connection(cur, conn)
