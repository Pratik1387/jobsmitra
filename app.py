from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

education_levels = [
"7th",
"10th",
"ITI",
"12th",
"Diploma",
"Graduate",
"Professional Graduate",
"Post Graduate",
"PhD"
]

def calculate_age(dob):
    today = datetime.today()
    dob = datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

@app.route("/", methods=["GET","POST"])
def home():

    jobs = []

    if request.method == "POST":

        dob = request.form["dob"]
        education = request.form["education"]
        state = request.form["state"]
        category = request.form["category"]

        age = calculate_age(dob)

        today = datetime.today()

        with open("jobs.json") as f:
            data = json.load(f)

        for job in data:

            min_age = job["min_age"]
            max_age = job["max_age"]

            if category == "SC":
                max_age += 5
            elif category == "ST":
                max_age += 5
            elif category == "OBC":
                max_age += 3

            if min_age <= age <= max_age:

                user_level = education_levels.index(education)
                job_level = education_levels.index(job["education_required"])

                if user_level >= job_level:

                    if job["state"] == "All" or job["state"] == state:

                        start = datetime.strptime(job["application_start"], "%Y-%m-%d")
                        end = datetime.strptime(job["application_end"], "%Y-%m-%d")

                        if start <= today <= end:
                            jobs.append(job)

        return render_template("result.html", jobs=jobs)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
