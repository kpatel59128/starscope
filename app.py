from flask import Flask, render_template, request
import datetime
import json

app = Flask(__name__)

# Load horoscope data
with open("horoscope_data.json") as file:
    horoscopes = json.load(file)

zodiac_signs = {
    "aries": (3, 21, 4, 19),
    "taurus": (4, 20, 5, 20),
    "gemini": (5, 21, 6, 20),
    "cancer": (6, 21, 7, 22),
    "leo": (7, 23, 8, 22),
    "virgo": (8, 23, 9, 22),
    "libra": (9, 23, 10, 22),
    "scorpio": (10, 23, 11, 21),
    "sagittarius": (11, 22, 12, 21),
    "capricorn": (12, 22, 1, 19),
    "aquarius": (1, 20, 2, 18),
    "pisces": (2, 19, 3, 20),
}

def get_sign_by_date(month, day):
    for sign, (start_month, start_day, end_month, end_day) in zodiac_signs.items():
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return sign
    return "aries"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    if 'birthdate' in request.form:
        date = datetime.datetime.strptime(request.form['birthdate'], "%Y-%m-%d")
        sign = get_sign_by_date(date.month, date.day)
    else:
        sign = request.form.get("sign")

    prediction = horoscopes.get(sign, {})
    return render_template("result.html", sign=sign.title(), prediction=prediction)

@app.route("/compatibility", methods=["POST"])
def compatibility():
    sign1 = request.form["sign1"].lower()
    sign2 = request.form["sign2"].lower()
    compatible = "Good Match!" if sign1[0] == sign2[0] else "Can Work with Effort"
    return render_template("compatibility.html", sign1=sign1.title(), sign2=sign2.title(), result=compatible)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
