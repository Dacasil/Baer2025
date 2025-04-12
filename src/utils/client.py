import base64
import json
import os
import sys
from pathlib import Path

from utils.myutils import timestamp
from utils.parse_docx import parse_docx
from utils.parse_pdf import parse_pdf
# from .parse_txt import parse_txt
# from .parse_png import parse_png


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR / "src")



class Client:
    """
    Client is a Python class that represents a raw client from the company.
    It contains methods to save and load client data in JSON format.
    
    Attributes:
    """

    def __init__(self, client_data: dict, client_id: str, session_id: str, client_folder: str = None) -> None:
        if not client_folder:
            self.client_name = str(f"{timestamp()}_client-id_{client_id}")
            self.client_folder = BASE_DIR / "data" / "samples" / self.client_name
        else:
            self.client_name = client_folder.name
            self.client_folder = client_folder
        self.client_id = client_id
        self.session_id = session_id
        self.label = None
        self.client_data = client_data

        self.client_folder.mkdir(parents=True, exist_ok=True)

        self.png_path = self.client_folder / "passport.png"
        self.docx_path = self.client_folder / "profile.docx"
        self.pdf_path = self.client_folder / "account.pdf"
        self.txt_path = self.client_folder / "description.txt"
        self.info_path = self.client_folder / "info.json"

        # parsed attributes (added by parse_samples function)
        self.parsed_folder = None
        self.parsed_pdf_path = None
        self.parsed_docx_path = None
        self.pdf_df = None
        self.docx_df = None
        # self.txt_df = None
        # self.png_df = None

    def save_client_json(self) -> None:
        """Saves the client data as a JSON file."""

        client_info = {
            "client_name": self.client_name,
            "client_id": self.client_id,
            "session_id": self.session_id,
            "label": self.label,
        }
        with open(self.info_path, "w", encoding="utf-8") as json_file:
            json.dump(client_info, json_file, indent=4)

        files = [
            (self.pdf_path, "account"),
            (self.txt_path, "description"),
            (self.png_path, "passport"),
            (self.docx_path, "profile"),
        ]

        for path, key in files:
            with open(path, "wb") as f:
                f.write(base64.b64decode(self.client_data[key]))

        self.parse_samples()

    def parse_samples(self) -> None:
        """Parses the samples."""

        self.parsed_folder = DATA_DIR / "parsed" / self.client_name
        self.parsed_folder.mkdir(parents=True, exist_ok=True)
        self.parsed_pdf_path = self.parsed_folder / "parsed_pdf.csv"
        self.parsed_docx_path = self.parsed_folder / "parsed_docx.csv"


        self.pdf_df = parse_pdf(self.pdf_path, self.parsed_pdf_path)
        self.docx_df = parse_docx(self.docx_path, self.parsed_docx_path)
        # self.txt_df = parse_txt(self.txt_path)
        # self.png_df = parse_png(self.png_path)

    def load_client(client_folder):
        """Loads the client data from the JSON file."""

        try:
            with open(client_folder / "info.json", "r", encoding="utf-8") as json_file:
                client_info = json.load(json_file)
            client_id = client_info["client_id"]
            session_id = client_info["session_id"]
        except FileNotFoundError:
            client_id = client_folder.name.split("_")[-1]
            session_id = None

        with open(client_folder / "account.pdf", "rb") as f:
            account_data = base64.b64encode(f.read()).decode()
        with open(client_folder / "description.txt", "rb") as f:
            description_data = base64.b64encode(f.read()).decode()
        with open(client_folder / "passport.png", "rb") as f:
            passport_data = base64.b64encode(f.read()).decode()
        with open(client_folder / "profile.docx", "rb") as f:
            profile_data = base64.b64encode(f.read()).decode()

        client_data = {
            "account": account_data,
            "description": description_data,
            "passport": passport_data,
            "profile": profile_data,
        }

        return client_data, client_id, session_id, client_folder


if __name__== "__main__":
    sample_client_folder = DATA_DIR / "external/Deficient/client_501"

    client = Client(*Client.load_client(sample_client_folder))
    client.parse_samples()
