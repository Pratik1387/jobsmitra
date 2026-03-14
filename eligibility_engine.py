import csv
from datetime import datetime

jobs = []

with open("jobs.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        jobs.append(row)

print("\nEnter your details\n")

name = input("Name: ")
dob_input = input("DOB (YYYY-MM-DD): ")
education = input("Education (10th / 12th / Graduate): ")
state = input("State: ")
category = input("Category (General / OBC / SC / ST): ")

dob = datetime.strptime(dob_input, "%Y-%m-%d")
today = datetime.today()

age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

relaxation = 0

if category == "OBC":
    relaxation = 3
elif category == "SC":
    relaxation = 5
elif category == "ST":
    relaxation = 5

adjusted_age = age - relaxation

eligible = []
expiring = []
expired = []

for job in jobs:

    min_age = int(job["min_age"])
    max_age = int(job["max_age"])
    last_date = datetime.strptime(job["last_date"], "%Y-%m-%d")

    if adjusted_age >= min_age and adjusted_age <= max_age:

        if job["state"] == "All" or job["state"] == state:

            if job["qualification"] == education or job["qualification"] == "Any":

                days_left = (last_date - today).days

                if days_left < 0:
                    expired.append(job)

                elif days_left <= 7:
                    expiring.append(job)

                else:
                    eligible.append(job)

print("\nUser:", name)
print("Age:", age)
print("Category:", category)
print("Education:", education)
print("State:", state)

print("\n========== ELIGIBLE JOBS ==========\n")

for job in eligible:
    print(job["job_name"], "| Last Date:", job["last_date"])

print("\n========== EXPIRING SOON ==========\n")

for job in expiring:
    print(job["job_name"], "| Last Date:", job["last_date"])

print("\n========== EXPIRED ==========\n")

for job in expired:
    print(job["job_name"], "| Last Date:", job["last_date"])