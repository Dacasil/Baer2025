from pathlib import Path

import fitz # PyMuPDF
import pymupdf
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_CLIENT = DATA_DIR / "external/Deficient/client_501"


def parse_pdf(pdf_path, out_path=None) -> pd.DataFrame:
    """
    Extracts form widget fields from each page.

    Returns:
        A DataFrame containing the field names and values.
    """
    pymupdf.TOOLS.mupdf_display_errors(False)

    # Open the PDF
    doc = fitz.open(pdf_path)
    form_data = []

    # Loop through each page and collect widget (form field) data.
    for page in doc:
        widgets = page.widgets()  # per-page widgets (form fields)
        if widgets:
            for widget in widgets:
                key = widget.field_name
                value = widget.field_value
                form_data.append((key, value))

    # Create a DataFrame
    df = pd.DataFrame(form_data, columns=["Field", "Value"])

    if out_path:
        # Save the DataFrame to a CSV file
        df.to_csv(out_path, index=False)

    return df


if __name__ == "__main__":
    client_folder_name = SAMPLE_CLIENT.name

    # Test pdf_to_table function
    pdf_path = SAMPLE_CLIENT / "account.pdf"
    output_csv_path = DATA_DIR / "parsed" / client_folder_name / "account.csv"
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    account_df = parse_pdf(pdf_path)