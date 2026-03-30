import os

from dotenv import load_dotenv
import psycopg


load_dotenv()


def connect_to_database():
    """This function connects to the database."""
    try:
        conn = psycopg.connect(
            host='127.0.0.1',
            port=5432,
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            connect_timeout=60,
        )
        print('Successfully connected to the database')
        cur = conn.cursor()

    except Exception as e:
        print(f'Error connecting to database: {e}')
        raise

    return cur, conn


def close_database_connection(cur, conn):
    """This function closes the database connection."""
    cur.close()
    conn.close()
