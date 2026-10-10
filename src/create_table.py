import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    dbname="labour_market",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    port="5432"
)

cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    avg_salary NUMERIC,
    search_term TEXT,
    created TIMESTAMPTZ
);
"""

cursor.execute(create_table_query)
conn.commit()

print("Table 'jobs' is ready!")

cursor.close()
conn.close()