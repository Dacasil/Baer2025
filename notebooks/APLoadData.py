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
        with open(f"sessions/{file}/raw.txt", "r", encoding="utf-8") as input_file:
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

        self.path = "sessions/"

# !!! Example/Test Functions

    ### =========== SAVING ===========
    def saveAllToFile(self):
        """

        :return: saves data to file in dic, name: "path/type/session_id.extension"
        """


        entries = {
            "passport": (self.passport, "png"),
            "profile": (self.profile, "docx"),
            "description": (self.description, "txt"),
            "account": (self.account, "pdf"),
            "raw": (self.raw, "txt")
        }
        try:
            os.makedirs(f"{self.path}{self.session_id}", exist_ok=True)
        except:
            print("FileExistsError - Fix!")

        for name, (data, extension) in entries.items():
            if name != "raw":
                file = base64.b64decode(data)
                with open(f"{self.path}{self.session_id}/{name}.{extension}", "wb") as f:
                    f.write(file)
            else:
                with open(f"{self.path}{self.session_id}/{name}.txt", "w", encoding="utf-8") as output_file:
                    output_file.write(json.dumps(self.raw, indent=4))

    # Funktionen hier aktuell noch überflüssig -> müssten dann für jeden modifiziert werden, evlt nur return "richtiger Datentyp"
    def saveRawData(self):
        """

        :return: saves raw data to file for later use, file name == SessionID
        """
        with open(f"sessions/{self.session_id}.txt", "w", encoding="utf-8") as output_file:
            output_file.write(json.dumps(self.raw, indent=4))

    def getAccount(self,save = False):
        """
        :param: self
        :return: writes account in file / returns data in base64 decoded
        """
        data = self.account
        file = base64.b64decode(data)
        if save:
            with open("account.pdf", "wb") as f:
                f.write(file)
        return file

    def getDescription(self,save = False):
        """
        :param: self
        :return: writes description in file / returns data in base64 decoded
        """
        data = self.profile
        file = base64.b64decode(data)
        if save:
            with open("description.docx", "wb") as f:
                f.write(file)
        return file


    def getProfilePDF(self, save = False):
        """
        :param: self
        :return: writes profile in file / returns data in base64 decoded
        """
        data = self.profile
        file = base64.b64decode(data)
        if save:
            with open("profile.docx", "wb") as f:
                f.write(file)
        return file

    def getPassportPicture(self, save = False):
        """
        :param: self
        :return: writes passport in file / returns data in base64 decoded
        """

        data = self.passport
        file = base64.b64decode(data)

        if save:
            with open("passport.png", "wb") as f:
                f.write(file)
        return file

    ### ===========  ===========

    def printMessage(self):
        print(self.message)


obj = Data(APICall())
obj.saveAllToFile()
# Examples
obj.getAccount(True)
obj.getPassportPicture(True)
