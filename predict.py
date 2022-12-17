import pickle
import requests
import json

model = pickle.load(open("model.pickle", "rb"))
API_KEY = "WFD9YL5C7FKXVCWWDK765ZHHW"


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
