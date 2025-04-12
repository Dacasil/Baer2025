from datetime import datetime
import os
import json
import base64


def timestamp():
    """Returns the current timestamp in ISO format."""
    return datetime.now().isoformat(timespec="seconds").replace(":", "").replace("-", "")


class ClientRaw:
    """
    Client is a Python class that represents a raw client from the company.
    It contains methods to save and load client data in JSON format.
    
    Attributes:
        account (str): The account name of the client.
        description (str): A description of the client.
        passport (str): The passport number of the client.
        profile (str): The profile information of the client.
        client_name (str): The name of the client.
        label (str): The label assigned to the client.
        client_id (str): The ID of the client.
        session_id (str): The session ID for the current game session.
    """

    def __init__(self, client_data: dict, client_id: str = None, session_id: str = None):
        self.account = client_data["account"]
        self.description = client_data["description"]
        self.passport = client_data["passport"]
        self.profile = client_data["profile"]

        self.client_name = str(f"{timestamp()}_client-id_{client_id}")
        self.client_id = client_id
        self.session_id = session_id
        self.label = None

        self.passport_path = None
        self.profile_path = None
        self.account_path = None
        self.description_path = None


        # TODO: von client_logic alles initialisieren. 

        ClientRaw.save_client_json(self)
    def save_client_json(self) -> None:
        """Saves the client data as a JSON file."""
        # Implement saving logic here
        current_folder = os.getcwd()
        file_path = os.path.join(current_folder, f"data/samples/")


        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        os.makedirs(f"{file_path}/{self.client_name}", exist_ok=True)
        file_path_json = os.path.join(file_path, f"{self.client_name}/info.json")
        file_path = os.path.join(file_path, f"{self.client_name}")

        self.passport_path = f"{file_path}passport.png"
        self.profile_path = f"{file_path}profile.docx"
        self.account_path = f"{file_path}account.pdf"
        self.description_path = f"{file_path}description.txt"

        client_data = {
            "client_name": self.client_name,
            "client_id": self.client_id,
            "session_id": self.session_id,
            "label": self.label,
        }


        with open(file_path_json, "w", encoding="utf-8") as json_file:
            json.dump(client_data, json_file, indent=4)



        entries = {
            "passport": (self.passport, "png"),
            "profile": (self.profile, "docx"),
            "description": (self.description, "txt"),
            "form": (self.account, "pdf"),
        }

        for name, (data, extension) in entries.items():
            with open(f"{file_path}/{name}.{extension}", "wb") as f:
                f.write(base64.b64decode(data))





class ClientParsed:
    ...



