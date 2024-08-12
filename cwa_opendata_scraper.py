from pprint import pprint 
import requests
import json
import os

hearder = {
    "Accept":  'application/json'
}
parameters = {
    'Authorization': os.getenv("CWA_KEY", None),
    'locationName': ["臺中市", "新竹縣", "新竹市", "臺南市"]
}

url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'

response = requests.get(url, headers=hearder, params=parameters)
if response.status_code == 200:
    weather = response.json()
    # pprint(weather['records']['location'])
else:
    print("Connect False")

weather_element_name = {
    'CI': '舒適度',
    'MaxT': '最高溫度',
    'MinT': '最低溫度',
    'PoP': '降雨機率',
    'Wx': '天氣現象'
}

cities_weather = dict()
for location in weather['records']['location']:
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
    
    cities_weather[location['locationName']] = city_weather

pprint(cities_weather)