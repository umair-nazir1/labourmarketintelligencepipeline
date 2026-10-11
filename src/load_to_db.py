"""Load cleaned job postings from JSON into the PostgreSQL `jobs` table.

Pipeline stage: LOAD (the "L" in ETL).
Input : data/cleaned_jobs.json (produced by clean_jobs.py)
Output: rows in the `jobs` table of the `labour_market` database

The script is idempotent: running it twice does not create duplicates.
"""

import os
import json

import pg8000.dbapi
from dotenv import load_dotenv

# Step 1: Read secrets (DB_PASSWORD) from the .env file into environment variables.
# This must run before os.getenv() is used below.
load_dotenv()

# Step 2: Read the cleaned data. `jobs` is a list with one dictionary per job.
with open("data/cleaned_jobs.json", "r") as f:
    jobs = json.load(f)

# Step 3: Connect to PostgreSQL with pg8000, a pure-Python driver (no compiled
# binary, so it is not blocked by Windows Smart App Control).
# The password comes from .env, never from the code.
conn = pg8000.dbapi.connect(
    host="localhost",
    database="labour_market",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    port=5432,
)

# A cursor is the object that sends SQL commands over the connection.
cursor = conn.cursor()

# Step 4: The INSERT template. Each %s is a placeholder that the driver fills in later.
# Placeholders (a parameterized query) protect against SQL injection.
# %s::timestamptz explicitly casts the date text to a timestamp with time zone.
# ON CONFLICT (id) DO NOTHING skips a job whose id already exists (the primary key),
# which is what keeps this script idempotent.
insert_query = """
INSERT INTO jobs (id, title, company, location, salary_min, salary_max, avg_salary, search_term, created)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::timestamptz)
ON CONFLICT (id) DO NOTHING;
"""

# Counters for the summary printed at the end.
inserted = 0
skipped = 0

# Step 5: Insert one job at a time.
for job in jobs:
    # The order of this tuple must match the column order in the INSERT above.
    # None values (jobs without a salary) are stored as NULL.
    cursor.execute(insert_query, (
        job["id"],
        job["title"],
        job["company"],
        job["location"],
        job["salary_min"],
        job["salary_max"],
        job["avg_salary"],
        job["search_term"],
        job["created"],
    ))

    # rowcount is 1 if a new row was inserted, 0 if ON CONFLICT skipped it.
    if cursor.rowcount == 1:
        inserted += 1
    else:
        skipped += 1

# Step 6: Commit once, so all inserts become permanent together (one transaction).
# If the script crashed before this line, nothing would be saved.
conn.commit()

print(f"Inserted {inserted} new jobs, skipped {skipped} already existing")

# Sanity check: count the rows now in the table.
cursor.execute("SELECT COUNT(*) FROM jobs;")
total = cursor.fetchone()[0]  # fetchone() returns one row; [0] is its first value
print(f"Total jobs in table: {total}")

# Release database resources.
cursor.close()
conn.close()