import psycopg2
import random
import string
from tqdm import tqdm

DB_HOST = "rds-migration.cvik8accw2tk.ap-south-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "rds_migration"
DB_USER = "postgres"
DB_PASS = "Admin1234"

TABLE_NAME = "large_data"
ROWS = 1000000  # Adjust for ~4-5GB depending on row size
CHUNK_SIZE = 1000

def random_string(length=4000):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def main():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            data TEXT
        );
    """)
    conn.commit()

    for _ in tqdm(range(0, ROWS, CHUNK_SIZE)):
        records = [(random_string(),) for _ in range(CHUNK_SIZE)]
        args_str = ','.join(cur.mogrify("(%s)", x).decode("utf-8") for x in records)
        cur.execute(f"INSERT INTO {TABLE_NAME} (data) VALUES {args_str}")
        conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()