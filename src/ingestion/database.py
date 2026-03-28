# Connect to database
import os

from dotenv import load_dotenv
import psycopg


load_dotenv()


def connect_to_database():
    """This function connects to the database."""
    conn = psycopg.connect(
        host='127.0.0.1',
        port=5433,
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('DB_USERNAME'),
        password='admin123!',
    )
    cur = conn.cursor()

    return cur, conn


def close_database_connection(cur, conn):
    """This function closes the database connection."""
    cur.close()
    conn.close()
