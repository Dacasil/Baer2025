"""Module to interact with the game API."""

import base64
import os
from pathlib import Path
from typing import Dict
from datetime import datetime

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
os.chdir(BASE_DIR)

load_dotenv()
PLAYER_NAME = os.getenv("PLAYER_NAME")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://hackathon-api.mlo.sehlat.io"
DATA_DIR = BASE_DIR / "data"

def timestamp():
    """Returns the current timestamp in ISO format."""
    return datetime.now().isoformat(timespec="seconds").replace(":", "").replace("-", "")

class ApiInterface:
    """
    ApiInterface is a Python class that interacts with a game API to start a game and send decisions.

    Attributes:
        session_id (str): The session ID for the current game session.
        session_timestamp (str): The timestamp of the current game session.
        self.score (int): The score of the current game session.
        status (str): The status of the current game session.
        headers (dict): The headers to be used in API requests.
    """

    def __init__(self):
        """Initializes the ApiInterface instance, and sets up request headers."""
        self.session_id = None
        self.session_timestamp = None
        self.score = None
        self.status = None
        self.headers = None

        self.headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

    def start_game(self):
        """Starts a new game by sending a request to the API."""
        
        start_game_url = f"{BASE_URL}/game/start"
        response = requests.post(start_game_url, headers=self.headers, json={
            "player_name": PLAYER_NAME
        })

        if response.status_code == 200:
            data = response.json()
            print(data["message"])

            self.session_id = data.get("session_id")
            self.session_timestamp = timestamp()
            self.score = data.get("score")
            self.status = "active"

            client_id = data["client_id"]
            client_data = data["client_data"]
            return client_id, client_data
        else:
            raise Exception(f"Error starting the game: {response.status_code}, {response.text}")

    def send_decision(self, client_id, decision):
        """Sends a decision to the API, and receives the next game state and client data."""
        
        decision_url = f"{BASE_URL}/game/decision"
        response = requests.post(decision_url, headers=self.headers, json={
            "decision": decision,
            "session_id": self.session_id,
            "client_id": client_id
        })

        if response.status_code == 200:
            data = response.json()
            self.status = data["status"]
            self.score = data["score"]

            next_client_id = data["client_id"]
            next_client_data = data["client_data"]

            # calculate current_label 
            bool_decision = decision == "Accept"
            is_correct_decision = self.status == "active"
            current_bool_label = bool_decision if is_correct_decision else not bool_decision
            current_label = "Accept" if current_bool_label else "Reject"

            return next_client_id, next_client_data, current_label 
        else:
            raise Exception(f"Error sending the decision: {response.status_code}, {response.text}")

    def save_client_data(self) -> None:
        """Saves client-related data (e.g., account, description, passport, profile) into files."""

        session_folder_name = f"{self.session_timestamp}_session-id_{self.session_id}"
        client_folder_name = f"{timestamp()}_client-id_{self.client_id}"

        output_dir = DATA_DIR / "samples" / session_folder_name / client_folder_name
        
        output_dir.mkdir(parents=True, exist_ok=True)

        output_files = {
            "account": output_dir / "account.pdf",
            "description": output_dir / "description.txt",
            "passport": output_dir / "passport.png",
            "profile": output_dir / "profile.docx"
        }

        for key, file_path in output_files.items():
            encoded_data = self.client_data.get(key)
            if encoded_data:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as file:
                    file.write(base64.b64decode(encoded_data))
                # print(f"{key.capitalize()} saved to {file_path}")
            else:
                print(f"No data found for {key}")


if __name__=="__main__":

    # Testing the API interface
    client = ApiInterface()

    client.start_game()
    print("GAME STARTED SUCCESSFULLY")

    client.send_decision("Accept")
    print("DECISION SENT SUCCESSFULLY")

    client.save_client_data()
    
