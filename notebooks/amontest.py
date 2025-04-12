import requests
import base64
import json
import csv
import os
from dotenv import load_dotenv
load_dotenv()


"""
-get data via APICall (raw data)
-transform into object 
-write simple functions for object (image transform, save to file etc)

!!! Import API Key and add below
"""


def APICall(loadExisiting = None):
    """
    :param loadExisiting: to test without using "new" datasets
    :return: raw Data

    Calls the API to get the Data
    """


    if loadExisiting != None:
        files = os.listdir("sessions/")
        file = files[0]
        with open(f"sessions/{file}.txt", "r", encoding="utf-8") as input_file:
            raw_data = json.load(input_file)
        return raw_data

    url = "https://hackathon-api.mlo.sehlat.io/game/start"
    payload = {
        "player_name": "FiveNeutrons"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": os.getenv("API_KEY")
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #print(list(data.keys()))
        #print(list(data["client_data"].keys()))

    else:
        print("Fehler:", response.status_code)
        print(response.text)
    return data


class Data:
    def __init__(self,data):
        """
        :param: raw data

        :return: structured object with raw data
        """
        self.raw = data
        self.message = data["message"]
        self.session_id = data["session_id"]
        self.player_id = data["player_id"]
        self.client_id = data["client_id"]
        self.score = data["message"]

        self.passport = data["client_data"]["passport"]
        self.profile = data["client_data"]["profile"]
        self.description = data["client_data"]["description"]
        self.account = data["client_data"]["account"]

# !!! Example/Test Functions
    def saveRawData(self):
        """

        :return: saves raw data to file for later use, file name == SessionID
        """
        with open(f"sessions/{self.session_id}.txt", "w", encoding="utf-8") as output_file:
            output_file.write(json.dumps(self.raw, indent=4))

    def getPassportPicture(self, save = False):
        """
        :param: self
        :return: writes passport in file / returns data in base64
        """

        data = self.passport
        passport_data = base64.b64decode(data)

        if save:
            with open("passport.png", "wb") as f:
                f.write(passport_data)
        return passport_data

    def printMessage(self):
        print(self.message)


obj = Data(APICall())

# Examples
obj.getPassportPicture(True)
obj.printMessage()
obj.saveRawData()