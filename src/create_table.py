# import os

# import psycopg2
# from dotenv import load_dotenv

# load_dotenv()

# conn = psycopg2.connect(
#     host="localhost",
#     dbname="labour_market",
#     user="postgres",
#     password=os.getenv("DB_PASSWORD"),
#     port="5432"
# )

# cursor = conn.cursor()

# create_table_query = """
# CREATE TABLE IF NOT EXISTS jobs (
#     id TEXT PRIMARY KEY,
#     title TEXT,
#     company TEXT,
#     location TEXT,
#     salary_min NUMERIC,
#     salary_max NUMERIC,
#     avg_salary NUMERIC,
#     search_term TEXT,
#     created TIMESTAMPTZ
# );
# """

# cursor.execute(create_table_query)
# conn.commit()

# print("Table 'jobs' is ready!")

# cursor.close()
# conn.close()


#  above is used to create table using psycopg2 in database and it is working fine.

"""Create the `jobs` table in the `labour_market` database.

Pipeline stage: setup (run once before the first load).
Safe to run many times: CREATE TABLE IF NOT EXISTS makes it idempotent.
"""

import os

import pg8000.dbapi
from dotenv import load_dotenv

# Read DB_PASSWORD from the .env file into environment variables.
load_dotenv()

# pg8000 is a pure-Python PostgreSQL driver, so it works even where a compiled
# driver such as psycopg2 is blocked (for example by Windows Smart App Control).
conn = pg8000.dbapi.connect(
    host="localhost",
    database="labour_market",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    port=5432,
)

# A cursor is the object that sends SQL commands over the connection.
cursor = conn.cursor()

# The schema: one column per field of a cleaned job posting.
# `id` is the PRIMARY KEY, so the database itself rejects duplicate ids.
# Salary columns allow NULL because many postings do not publish a salary.
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

# Make the change permanent (without commit it is rolled back when the connection closes).
conn.commit()

print("Table 'jobs' is ready!")

cursor.close()
conn.close()