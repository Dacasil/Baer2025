from pathlib import Path

import fitz # PyMuPDF
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_CLIENT = DATA_DIR / "external/Deficient/client_501"


def parse_png(png_path, out_path=None) -> pd.DataFrame:
    """
    Extracts passport widget fields from each page.
    Takes a PNG file as input and returns a DataFrame.
    Optionally it can save the DataFrame to a CSV file.
    """
    
    ...



if __name__ == "__main__":
    client_folder_name = SAMPLE_CLIENT.name

    # Test pdf_to_table function
    pdf_path = SAMPLE_CLIENT / "account.pdf"
    output_csv_path = DATA_DIR / "parsed" / client_folder_name / "account.csv"
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    account_df = parse_png(pdf_path)
