from datetime import datetime

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
    
    def __init__(self, client_data: dict, client_id: str, session_id: str):
        self.account = None
        self.description = None
        self.passport = None
        self.profile = None

        self.client_name = None
        self.label = None
        self.client_id = None
        self.session_id = None

        # TODO: von client_logic alles initialisieren. 

        self.client_name = f"{timestamp()}_client-id_{self.client_id}"

    def save_client_json(self) -> None:
        """Saves the client data as a JSON file."""
        # Implement saving logic here

    # EXAMPLE
    # def save_client_data(self) -> None:
    #     """Saves client-related data (e.g., account, description, passport, profile) into files."""

    #     session_folder_name = f"{self.session_timestamp}_session-id_{self.session_id}"
    #     client_folder_name = f"{timestamp()}_client-id_{self.client_id}"

    #     output_dir = DATA_DIR / "samples" / session_folder_name / client_folder_name
        
    #     output_dir.mkdir(parents=True, exist_ok=True)

    #     output_files = {
    #         "account": output_dir / "account.pdf",
    #         "description": output_dir / "description.txt",
    #         "passport": output_dir / "passport.png",
    #         "profile": output_dir / "profile.docx"
    #     }

    #     for key, file_path in output_files.items():
    #         encoded_data = self.client_data.get(key)
    #         if encoded_data:
    #             os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #             with open(file_path, "wb") as file:
    #                 file.write(base64.b64decode(encoded_data))
    #             # print(f"{key.capitalize()} saved to {file_path}")
    #         else:
    #             print(f"No data found for {key}")


    def load_client_json(self) -> dict:
        """Loads the client data from a JSON file and gives client_data.
        example:
            client = Client(Client.load_json("client_data.json"))
        Used later in Training."""
        # Implement loading logic here

        # muss auch client_id und session_id zurückgeben, damit für __init__



class ClientParsed:
    ...



if __name__ == "__main__":
    client = ClientRaw(ClientRaw.load_json("client_data.json"))