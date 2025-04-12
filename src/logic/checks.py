import os
import sys
from pathlib import Path

from utils.client import Client

BASE_DIR = Path(__file__).resolve().parent.parent.parent
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR / "src")

def trivial_check(passport_path) -> bool:
    return True # Always returns True for testing purposes

def gemini_check(client) -> bool:
    # Placeholder for Gemini check logic

    pdf_df = client.pdf_df
    docx_df = client.docx_df

    print(pdf_df.head())
    print(docx_df.head())


    # SPIELPLATZ FÜR AMON

if __name__ == "__main__":
    # Example usage
    sample_client_folder = next(BASE_DIR.rglob("data/samples/*client-id_*"))

    client = Client(*Client.load_client(sample_client_folder))
    client.parse_samples()

    # Run the checks
    print(trivial_check(client.pdf_path))
    gemini_check(client)