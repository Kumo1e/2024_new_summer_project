from pprint import pprint 
import requests, json, os

weather_element_name = {
        'CI': '舒適度',
        'MaxT': '最高溫度',
        'MinT': '最低溫度',
        'PoP': '降雨機率',
        'Wx': '天氣現象'
    }

def get_cyties_weather(cwa_key: str, location_name: list) -> dict:

    hearder = {
        "Accept":  'application/json'
    }
    parameters = {
        'Authorization': cwa_key,  
        'locationName': location_name
    }

    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'

    response = requests.get(url, headers=hearder, params=parameters)
    if response.status_code == 200:
        weather = response.json()
    else:
        print("Connect False")

    cities_weather = dict()
    for location in weather['records']['location']:
        city_weather = dict()
        city_weather = get_city_weather(location)
        cities_weather[location['locationName']] = city_weather

    return cities_weather

def get_city_weather(location):
    city_weather = dict()
    for weather_element in location['weatherElement']:
        element_name = weather_element["elementName"]
        if element_name in ['MaxT', 'MinT']:
            parameterUnit = "°C"
        elif element_name in ['PoP']:
            parameterUnit = "%"
        else:
            parameterUnit = ""

        element_value = weather_element["time"][0]["parameter"]["parameterName"]
        city_weather[weather_element_name[element_name]] = element_value + parameterUnit

    return city_weather


if __name__ == "__main__":
    cwa_key = os.getenv("CWA_KEY", None)
    location_name = ["臺中市", "新竹縣", "新竹市", "臺南市"]
    if cwa_key:
        pprint(get_cyties_weather(cwa_key, location_name))
    else:
        print("CWA API key is not found")