from pathlib import Path

import pandas as pd

from .database import connect_to_database


def process_ingestion(folder_path: str):
    """This function processes the data ingestion."""
    files = load_data(folder_path)

    cur, conn = connect_to_database()

    for file in files:
        load_data_to_database(file, cur, conn)

    # conn.commit()
    # close_database_connection(cur, conn)
    return


def load_data(folder_path_str: str):
    """This function ..."""
    print(f'Processing folder: {folder_path_str}')
    clean_path = folder_path_str.strip().strip('"')

    folder_path = Path(clean_path)

    if not folder_path.exists():
        print(f'Error: The directory {folder_path} does not exist.')
        return

    files = []
    folder_path = Path(folder_path_str)
    for file in folder_path.iterdir():
        if file.is_file() and file.suffix == '.csv':
            print(file)
            files.append(file)
    print(f'Found {len(files)} CSV files in the directory.')
    return files


def load_data_to_database(file, cur, conn):
    """This function ..."""
    df = pd.read_csv(file)
    print(f'df shape: {df.shape}')
