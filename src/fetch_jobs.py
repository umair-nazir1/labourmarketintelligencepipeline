# import requests
# import json
# app_id= "aca09c72"
# app_key= "16bc38a270b9ccc74bf0134d5808d066"
# url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={app_key}&results_per_page=5&what=python"
# response = requests.get(url)
# print(response.status_code)
# data= response.json()
# # print(json.dumps(data, indent=2))
# jobs = data['results']
# for job in jobs:
#     title = job["title"]
#     company = job["company"]["display_name"]
#     location = job["location"]["display_name"]
#     salary_min = job.get("salary_min")
#     salary_max = job.get("salary_max")

#     print(f"Title: {title}")
#     print(f"Company: {company}")
#     print(f"Location: {location}")
#     print(f"Salary: {salary_min} - {salary_max}")
#     print("---")

# with open("data/raw_jobs.json", "w") as f:
#     json.dump(jobs, f, indent=2)
# print("Job data saved to raw_jobs.json")

import requests
import json
import time

app_id = "aca09c72"
app_key = "16bc38a270b9ccc74bf0134d5808d066"

search_terms = ["python", "data engineer", "sql", "aws"]

all_jobs = []

for term in search_terms:
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={app_key}&results_per_page=10&what={term}"

    response = requests.get(url)
    data = response.json()
    jobs = data["results"]

    for job in jobs:
        job["search_term"] = term

    all_jobs.extend(jobs)

    print(f"Fetched {len(jobs)} jobs for '{term}'")

    time.sleep(1)

with open("data/raw_jobs.json", "w") as f:
    json.dump(all_jobs, f, indent=2)

print(f"Saved {len(all_jobs)} total jobs to data/raw_jobs.json")