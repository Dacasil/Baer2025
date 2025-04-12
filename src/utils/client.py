import base64
import json
import os
import sys
from pathlib import Path

from .utils import timestamp
from .parse_docx import parse_docx
from .parse_pdf import parse_pdf
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

    def __init__(self, client_data: dict, client_id: str = None, session_id: str = None):
        self.client_name = str(f"{timestamp()}_client-id_{client_id}")
        self.client_id = client_id
        self.session_id = session_id
        self.label = None

        client_folder = BASE_DIR / "data" / "samples" / self.client_name
        client_folder.mkdir(parents=True, exist_ok=True)

        self.png_path = client_folder / "passport.png"
        self.docx_path = client_folder / "profile.docx"
        self.pdf_path = client_folder / "account.pdf"
        self.txt_path = client_folder / "description.txt"
        self.info_path = client_folder / "info.json"

        Client.save_client_json(self, client_data)


    def save_client_json(self, client_data) -> None:
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
                f.write(base64.b64decode(client_data[key]))

    def parse_samples(self) -> None:
        """Parses the samples."""

        self.pdf_df = parse_pdf(self.pdf_path)
        self.docx_df = parse_docx(self.docx_path)
        # self.txt_df = parse_txt(self.txt_path)
        # self.png_df = parse_png(self.png_path)