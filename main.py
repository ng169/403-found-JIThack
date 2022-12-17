from flask import Flask, render_template, request, redirect, url_for
from predict import get_result
from geopy.geocoders import Nominatim
from pymongo import MongoClient

app = Flask(__name__)

geolocator = Nominatim(user_agent="MyApp")

PASSWORD = "DHPwruNBxDzK7pjC"
client = MongoClient(f"mongodb+srv://ng169:{PASSWORD}@cluster0.nxsy2lf.mongodb.net/?retryWrites=true&w=majority")
db = client["jitUserDB"]
col = db["users"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        loc_name = request.form["location"]
        location = geolocator.geocode(loc_name)
        lat = location.latitude
        long = location.longitude
        doc = {
            'name': name,
            'email': email,
            'lat': lat,
            'long':long
        }
        print(doc)
        x = col.insert_one(doc)
        return redirect(url_for('home'))


@app.route("/api/", methods=["GET", "POST"])
def get_predict():
    loc_name = request.form["city"]
    location = geolocator.geocode(loc_name)
    lat = location.latitude
    long = location.longitude
    result = get_result(lat=lat, long=long)
    if result == 1:
        return redirect(url_for("one_flood"))
    else:
        return redirect(url_for("zero_flood"))


@app.route("/one")
def one_flood():
    return render_template("one.html")


@app.route("/zero")
def zero_flood():
    return render_template("zero.html")


if __name__ == "__main__":
    app.run(debug=True)
