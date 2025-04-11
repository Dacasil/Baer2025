import requests
import base64
import json


url = "https://hackathon-api.mlo.sehlat.io/game/start"
payload = {
    "player_name": "FiveNeutrons"
}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": ""
}
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
else:
    print("Fehler:", response.status_code)
    print(response.text)

class LoadData:
    @staticmethod
    def passport(data):
        passport_data = base64.b64decode(data["client_data"]["passport"])
        with open("passport.png", "wb") as f:
            f.write(passport_data)
        print("saved")

class Data:
    def __init__(self,data):
        Passport = LoadData.passport(data)



Data.PassPort