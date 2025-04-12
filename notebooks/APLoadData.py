import requests
import base64
import json
import csv
import os
from dotenv import load_dotenv
import random
load_dotenv()

"""
HOW TO USE

create file structure

notebooks
-sample_sessions <- copy all unpacked clients in here
- -client_1
- -client_2
... 

execute

obj = Data(RealData = False) <- for demo files, otherwise True for real Data
print(obj.description) example

"""



"""
-get data via APICall (raw data)
-transform into object 
-write simple functions for object (image transform, save to file etc)

!!! Import API Key and add below
"""





class Data:
    def __init__(self,RealData = True):
        """
        :param: raw data

        :return: structured object with raw data
        """

        if RealData == False:

            self.path = "sample_sessions/"
            self.session_id = "Sample"
            data = Data.loadAllFromFile(self)[0]
            self.raw = "Sample"
            self.message = "Sample"
            self.player_id = "Sample"
            self.client_id = "Sample"
            self.score = "Sample"

            self.passport = data["passport"]
            self.profile = data["profile"]
            self.description = data["description"]
            self.account = data["account"]
        else:
            self.path = "sessions/"
            data = Data.APICall()
            self.raw = data
            self.session_id = data["session_id"]
            self.message = data["message"]
            self.player_id = data["player_id"]
            self.client_id = data["client_id"]
            self.score = data["message"]

            self.passport = base64.b64decode(data["client_data"]["passport"])
            self.profile = base64.b64decode(data["client_data"]["profile"])
            self.description = base64.b64decode(data["client_data"]["description"])
            self.account = base64.b64decode(data["client_data"]["account"])

        print(f"sessionID: {self.session_id}")

    ### =========== SAVING ===========
    # save session
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
        # create session folder if not existing yet
        os.makedirs(f"{self.path[:-1]}", exist_ok=True)
        # create session folder - named "sessionid"
        try:
            os.makedirs(f"{self.path}{self.session_id}", exist_ok=True)
        except:
            print("FileExistsError - Fix!")

        for name, (data, extension) in entries.items():
            if name != "raw":
                with open(f"{self.path}{self.session_id}/{name}.{extension}", "wb") as f:
                    f.write(data)
            else:
                with open(f"{self.path}{self.session_id}/{name}.txt", "w", encoding="utf-8") as output_file:
                    output_file.write(json.dumps(self.raw, indent=4))

    # load from API
    def APICall():
        """
        :param loadExisiting: to test without using "new" datasets
        :return: raw Data

        Calls the API to get the Data
        """

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
            # print(list(data.keys()))
            # print(list(data["client_data"].keys()))

        else:
            print("Fehler:", response.status_code)
            print(response.text)
        return data

    # load single file
    def loadAllFromFile(self):
        """
        Reads the saved data from files in the session folder and returns it as a dictionary.
        """

        folders = os.listdir(self.path)
        allFolders = []
        loaded_data = {}

        entries = {
            "passport": "png",
            "profile": "docx",
            "description": "txt",
            "account": "pdf",
            "raw": "txt"
        }
        for folder in folders:
            if folder == ".DS_Store":
                continue
            # to identify folder name
            self.session_id = folder
            files = os.listdir(f"{self.path}/{folder}")
            for val in files:
                if val == ".DS_Store":
                    continue
                # auslesen der einzelnen Dateien
                if val in ["passport.png", "account.pdf", "profile.docx"]:  # Binary files
                    with open(f"{self.path}/{folder}/{val}", "rb") as f:
                        loaded_data[f"{val.split('.')[0]}"] = f.read()

                elif val == "description.txt":  # Text files
                    with open(f"{self.path}/{folder}/{val}", "r", encoding="utf-8") as f:
                        loaded_data[f"{val.split('.')[0]}"] = f.read()
            allFolders.append(loaded_data)
        return allFolders

    # load a random (sample) session
    def loadAllFromFile(self):
        """
        Reads the saved data from files in the session folder and returns it as a dictionary.
        """

        folders = os.listdir(self.path)
        allFolders = []
        loaded_data = {}

        entries = {
            "passport": "png",
            "profile": "docx",
            "description": "txt",
            "account": "pdf",
            "raw": "txt"
        }
        for folder in folders:
            if folder == ".DS_Store":
                continue
            # to identify folder name
            self.session_id = folder
            files = os.listdir(f"{self.path}/{folder}")
            for val in files:
                if val == ".DS_Store":
                    continue
                # auslesen der einzelnen Dateien
                if val in ["passport.png", "account.pdf", "profile.docx"]:  # Binary files
                    with open(f"{self.path}/{folder}/{val}", "rb") as f:
                        loaded_data[f"{val.split('.')[0]}"] = f.read()

                elif val == "description.txt":  # Text files
                    with open(f"{self.path}/{folder}/{val}", "r", encoding="utf-8") as f:
                        loaded_data[f"{val.split('.')[0]}"] = f.read()
            allFolders.append(loaded_data)
        return allFolders


    def loadRandomFile(self):
        pass



    # Funktionen hier aktuell noch überflüssig -> müssten dann für jeden modifiziert werden, evlt nur return "richtiger Datentyp"

    # !!! Example/Test Functions

    def saveRawData(self):
        """

        :return: saves raw data to file for later use, file name == SessionID
        """
        with open(f"{self.path}{self.session_id}.txt", "w", encoding="utf-8") as output_file:
            output_file.write(json.dumps(self.raw, indent=4))

    def getAccount(self,save = False):
        """
        :param: self
        :return: writes account in file / returns data in base64 decoded
        """
        data = self.account
        if save:
            with open("account.pdf", "wb") as f:
                f.write(data)
        return data

    def getDescription(self,save = False):
        """
        :param: self
        :return: writes description in file / returns data in base64 decoded
        """
        data = self.profile
        if save:
            with open("description.docx", "wb") as f:
                f.write(data)
        return data


    def getProfilePDF(self, save = False):
        """
        :param: self
        :return: writes profile in file / returns data in base64 decoded
        """
        data = self.profile
        if save:
            with open("profile.docx", "wb") as f:
                f.write(data)
        return data

    def getPassportPicture(self, save = False):
        """
        :param: self
        :return: writes passport in file / returns data in base64 decoded
        """

        data = self.passport

        if save:
            with open("passport.png", "wb") as f:
                f.write(data)
        return data

    ### ===========  ===========

    def printMessage(self):
        print(self.message)


client = Data(RealData = False)
print(client.description)
#obj.saveAllToFile()
# Examples
#obj.getAccount(True)
#obj.getPassportPicture(True)



"""
Ordner struktur für Json

samples:
name: {timestamp-clientid}






"""