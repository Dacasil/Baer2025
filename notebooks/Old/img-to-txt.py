from paddleocr import PaddleOCR
import cv2
import re
import os
import re
from PIL import Image, ImageFilter
import platform
from datetime import datetime
import csv


# Initialize ONCE at the start of your script
ocr = PaddleOCR(use_angle_cls=True, lang="en")  # Slow only the first time


def extract_with_paddleocr(image_path):

    # Preprocess
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    processed_img = clahe.apply(gray)

    # Extract text
    result = ocr.ocr(processed_img, cls=True)
    extracted_texts = [line[1][0] for line in result[0]]  # Extract text only

    # Filter MRZ
    mrz_regex = r"[A-Z0-9<]{44}"
    mrz = [
        text
        for text in extracted_texts
        if re.fullmatch(mrz_regex, text.replace(" ", ""))
    ]

    return {"all_text": extracted_texts, "mrz": mrz}


def text_to_data(text):
    info = {}
    patterns = {
        "passport_number": r"\b[A-Z]{2}[0-9]{7}\b",
        "nationality": r"\b[A-Z]{3}\b",
        "names (P< format)": r"P<[A-Z]{3}([A-Z]+)<<([A-Z<]+)",
        "sex": r"\b[MFO]\b",
        "dates": r"\b[0-9]{2}-[A-Za-z]{3}-[0-9]{4}\b",
    }

    # Extract fields
    info["passport_number"] = re.search(patterns["passport_number"], text).group()
    info["nationality"] = re.search(patterns["nationality"], text).group()
    info["sex"] = re.search(patterns["sex"], text).group()

    if name_match := re.search(patterns["names (P< format)"], text):
        info["surname"] = name_match.group(1).replace("<", " ").strip()
        info["name"] = name_match.group(2).replace("<", " ").strip()
        # info["full_name"] = f"{info['surname']} {info['name']}"

    if dates_match := re.findall(patterns["dates"], text):
        info["date_of_birth"] = datetime.strptime(dates_match[0], "%d-%b-%Y").strftime(
            "%d%m%Y"
        )
        info["issue_date"] = datetime.strptime(dates_match[1], "%d-%b-%Y").strftime(
            "%d%m%Y"
        )
        info["expiration_date"] = datetime.strptime(
            dates_match[2], "%d-%b-%Y"
        ).strftime("%d%m%Y")

    # Write the dictionary to a CSV file
    with open("test.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Field", "Value"])  # Write header
        for key, value in info.items():
            writer.writerow([key, value])
    # return info


# Run
result = extract_with_paddleocr("passport.png")
# print("MRZ:", result["mrz"])
# print("All text:", result["all_text"])

text_to_data(" ".join(result["all_text"]))
