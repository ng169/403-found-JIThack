import pickle
import requests
import json
import smtplib
from pymongo import MongoClient

my_email = "k6318214@gmail.com"
password = "zxrzukfpjhkvfbwe"
model = pickle.load(open("model.pickle", "rb"))
API_KEY = "WFD9YL5C7FKXVCWWDK765ZHHW"


PASSWORD = "DHPwruNBxDzK7pjC"
client = MongoClient(f"mongodb+srv://ng169:{PASSWORD}@cluster0.nxsy2lf.mongodb.net/?retryWrites=true&w=majority")

db = client["jitUserDB"]

col = db["users"]

cur = col.find({})


def get_forecast(lat, long):
    final_data = [0, 0, 0, 0, 0]
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat}%2C{long}?unitGroup=us&elements=datetime%2Ctemp%2Chumidity%2Cprecip%2Cprecipprob%2Cwindspeed%2Ccloudcover&include=days%2Cobs%2Cremote%2Cfcst&key={API_KEY}&contentType=json"
    response = requests.get(url).json()
    print(json.dumps(response, indent=1))
    data = response["days"]
    for i in data:
        final_data[0] += i["temp"]
        final_data[1] += i["windspeed"]
        final_data[2] += i["cloudcover"]
        final_data[3] += i["precip"]
        final_data[4] += i["humidity"]

    final_data = [i / 15 for i in final_data]
    final_data[3] *= 1500
    return final_data


def get_result(lat, long):
    forecast = get_forecast(lat, long)
    return model.predict([forecast])[0]


for doc in cur:
    res = get_result(doc["lat"], doc["long"])
    if res == 1:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()  # tls - transport layer security
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=doc["email"],
                msg=f"Subject:Flood Warning Alert\n\nThis mail is to inform you that there is probability of occurence of a flood near you. Please stay safe and take necessary precautions"
            )
            connection.close()
