import json
import os
import sys
from pathlib import Path

from utils.client import Client

BASE_DIR = Path(__file__).resolve().parent.parent
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR / "src")


if __name__ == "__main__":
    with open("tests/sample_start_response.json", "r") as file:
        response = json.load(file)
        client_data = response["client_data"]
        client_id = response["client_id"]
        session_id = response["session_id"]

    client = Client(client_data, client_id, session_id)
    