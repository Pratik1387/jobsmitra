from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

education_levels = ["10th", "12th", "Graduate"]

def calculate_age(dob):
    today = datetime.today()
    dob = datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name")
        dob = request.form.get("dob")
        education = request.form.get("education")
        state = request.form.get("state")
        category = request.form.get("category")

        age = calculate_age(dob)

        with open("jobs.json") as f:
            jobs = json.load(f)

        eligible_jobs = []

        for job in jobs:

            min_age = job["min_age"]
            max_age = job["max_age"]

            # Apply category relaxation
            if category == "SC":
                max_age += 5
            elif category == "ST":
                max_age += 5
            elif category == "OBC":
                max_age += 3

            # Age check
            if min_age <= age <= max_age:

                # Education check
                user_level = education_levels.index(education)
                job_levels = [education_levels.index(e) for e in job["education"]]

                if user_level >= min(job_levels):

                    # State check
                    if job["state"] == "All" or job["state"] == state:

                        eligible_jobs.append(job)

        return render_template("result.html", jobs=eligible_jobs)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

