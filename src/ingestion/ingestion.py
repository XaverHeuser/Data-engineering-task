import psycopg

conn = psycopg.connect(
    host="127.0.0.1",
    port=5433,
    dbname="task_db",
    user="admin",
    password="admin123!"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        email TEXT,
        name TEXT,
        address TEXT
    )
""")

conn.commit()
cur.close()
conn.close()