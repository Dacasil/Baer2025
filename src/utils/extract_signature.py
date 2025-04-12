import contextlib
import os
from pathlib import Path

import fitz # PyMuPDF
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_CLIENT = DATA_DIR / "external/Good/client_1"

SIGNATURE_ANCHOR_TEXT = "Specimen Signature:"


def extract_signature(pdf_path, anchor_text, output_image_path):
    """
    Extracts the signature area from the PDF. This function first searches for the
    anchor text (e.g. "Specimen Signature:"), defines a rectangle below it that includes
    the signature box, then insets that rectangle to remove the drawn border lines,
    and finally renders the clipped region to an image file.
    """
    # We will suppress MuPDF's internal warnings by temporarily redirecting stderr.
    with open(os.devnull, "w") as fnull, contextlib.redirect_stderr(fnull):
        doc = fitz.open(pdf_path)

        for page_index, page in enumerate(doc):
            # Get text blocks from the page (each block returns (x0, y0, x1, y1, text, ...))
            blocks = page.get_text("blocks")
            for b in blocks:
                x0, y0, x1, y1, text = b[:5]

                # Look for the anchor text to locate the signature box
                if anchor_text in text:
                    # These offsets and dimensions should be tweaked to match your document.
                    LEFT_OFFSET = 0
                    TOP_OFFSET = 5
                    WIDTH = 150  # outer box width
                    HEIGHT = 40  # outer box height

                    # Define the outer rectangle that includes the entire signature box (with borders)
                    outer_rect = fitz.Rect(
                        x0 + LEFT_OFFSET,  # left
                        y1 + TOP_OFFSET,  # top
                        x0 + LEFT_OFFSET + WIDTH,  # right
                        y1 + TOP_OFFSET + HEIGHT  # bottom
                    )

                    # Inset the rectangle to remove the drawn border lines.
                    # Adjust BORDER_INSET as needed (e.g., 3 pixels).
                    BORDER_INSET = 3
                    clip_rect = fitz.Rect(
                        outer_rect.x0 + BORDER_INSET,
                        outer_rect.y0 + BORDER_INSET,
                        outer_rect.x1 - BORDER_INSET,
                        outer_rect.y1 - BORDER_INSET,
                    )

                    # Render the region (you can increase the zoom factor for better resolution)
                    zoom_factor = 2
                    matrix = fitz.Matrix(zoom_factor, zoom_factor)
                    pix = page.get_pixmap(matrix=matrix, clip=clip_rect)
                    pix.save(output_image_path)
                    # print(f"Signature extracted on page {page_index + 1} → {output_image_path}")
                    return  # Stop after the first occurrence

        print("Did not find the anchor text on any page.")
        return





if __name__ == "__main__":
    client_folder_name = SAMPLE_CLIENT.name

    # Test extract_signature function
    pdf_path = SAMPLE_CLIENT / "account.pdf"
    output_image_path = DATA_DIR / "parsed" / client_folder_name / "signature_extracted.png"
    output_image_path.parent.mkdir(parents=True, exist_ok=True)
    extract_signature(pdf_path, SIGNATURE_ANCHOR_TEXT, output_image_path)
