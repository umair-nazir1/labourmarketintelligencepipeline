

import os

import requests
import json
import time
from dotenv import load_dotenv
load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

search_terms = ["python", "data engineer", "sql", "aws"]

all_jobs = []

for term in search_terms:
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={app_key}&results_per_page=10&what={term}"

    response = requests.get(url)
    print(term,"-> status code:", response.status_code)
    data = response.json()
    if "results" not in data:
        print("API error",term)
        continue
    jobs = data["results"]

    for job in jobs:
        job["search_term"] = term

    all_jobs.extend(jobs)

    print(f"Fetched {len(jobs)} jobs for '{term}'")

    time.sleep(1)

with open("data/raw_jobs.json", "w") as f:
    json.dump(all_jobs, f, indent=2)

print(f"Saved {len(all_jobs)} total jobs to data/raw_jobs.json")