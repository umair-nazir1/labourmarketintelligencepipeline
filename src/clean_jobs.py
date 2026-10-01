import json

with open("data/raw_jobs.json", "r") as f:
    jobs = json.load(f)

print(f"Total jobs loaded: {len(jobs)}")

seen_ids = set()
unique_jobs = []

for job in jobs:
    job_id = job["id"]

    if job_id not in seen_ids:
        unique_jobs.append(job)
        seen_ids.add(job_id)

print(f"Unique jobs after removing duplicates: {len(unique_jobs)}")
# print(unique_jobs)

cleaned_jobs = []

for job in unique_jobs:
    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")

    if salary_min and salary_max:
        avg_salary = (salary_min + salary_max) / 2
    else:
        avg_salary = None

    cleaned_job = {
        "id": job["id"],
        "title": job["title"],
        "company": job["company"]["display_name"],
        "location": job["location"]["display_name"],
        "salary_min": salary_min,
        "salary_max": salary_max,
        "avg_salary": avg_salary,
        "search_term": job["search_term"],
        "created": job["created"]
    }

    cleaned_jobs.append(cleaned_job)

print(f"Cleaned jobs ready: {len(cleaned_jobs)}")


with open("data/cleaned_jobs.json", "w") as f:
    json.dump(cleaned_jobs, f, indent=2)

print("Saved to data/cleaned_jobs.json")