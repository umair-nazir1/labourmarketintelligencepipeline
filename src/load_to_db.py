import os

import psycopg2
import json

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

print("Connected to database successfully!")

cursor.close()
conn.close()