#!/usr/bin/env python3
"""
gemini_consistency_check.py

This script loads three CSV files:
  1. profile_preproc.csv   (structured profile fields) with columns "Field", "Value"
  2. pdf_preprocessed.csv  (narrative data) with columns "Field", "Value"
  3. passport_data.csv     (passport fields) with columns "Field", "Value"

It then converts each file into a text summary, builds a prompt for Gemini to compare
all three data sources, and returns a simple TRUE/FALSE answer — where TRUE indicates
a material, non-explainable contradiction among them, and FALSE indicates any
differences are minor or explainable.

IMPORTANT:
- Make sure you have the `google-generativeai` package installed.
- Optionally, set your Gemini API key as an environment variable named GEMINI_API_KEY
  or manually specify in code for testing.
"""

import json
import os
import sys
import time
from pathlib import Path

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

from logic.build_prompt import build_prompt
from utils.client import Client

BASE_DIR = Path(__file__).resolve().parent.parent.parent
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR / "src")

MAX_RETRIES = 5
RETRY_DELAY = 5



def convert_df_to_text(df, key_field="Field", value_field="Value", delimiter=": "):
    lines = []
    for _, row in df.iterrows():
        key = str(row[key_field])
        value = str(row[value_field])
        lines.append(f"{key}{delimiter}{value}")
    return "\n".join(lines)


def check_consistency_with_gemini(profile_text, narrative_text, passport_text, api_key):
    """
    Configures Gemini, builds the prompt, and sends it for content generation.

    Returns:
        str: The Gemini-generated result (expected to be "TRUE" or "FALSE").
    """
    # Configure the Gemini API with your API key.
    genai.configure(api_key=api_key)
    # Adjust the model name if needed. "gemini-1.5-pro" is an example.
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Build the multi-source prompt.
    prompt = build_prompt(profile_text, narrative_text, passport_text)

    # Send the prompt to Gemini and capture the response.

    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(prompt)
            break
        except ResourceExhausted as e:
            try:
                details = str(e.details[-1])
                print(details)
                retry_delay = int(details.split("seconds: ")[-1].split("\n")[0])
            except (IndexError, ValueError):
                retry_delay = RETRY_DELAY
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay+10)

    return response.text.strip()



def gemini_checker(docx_df, pdf_df, png_df):

    # Convert each CSV into a text representation.
    profile_text = convert_df_to_text(docx_df)
    narrative_text = convert_df_to_text(pdf_df)
    passport_text = convert_df_to_text(png_df)

    # Get your Gemini API key. If you want, you can store it in an env var named GEMINI_API_KEY.
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception(
            "No Gemini API key found. Set GEMINI_API_KEY as an environment variable or place it in the code.")

    # Call Gemini to check consistency.
    gemini_result = check_consistency_with_gemini(profile_text, narrative_text, passport_text, api_key)
    print(f"Gemini result: {gemini_result}")

    gemini_result_lower = gemini_result.lower()
    true_count = gemini_result_lower.count("true")
    false_count = gemini_result_lower.count("false")

    # Determine the result based on counts
    if true_count > false_count:
        negated_result = True
    elif false_count > true_count:
        negated_result = False
    else:
        raise ValueError("Equal occurrences of 'TRUE' and 'FALSE' detected. Unable to determine result.")

    result = not negated_result
    return result


if __name__ == "__main__":
    # Example usage
    sample_client_folder = next(BASE_DIR.rglob("data/samples/*client-id_*"))

    client = Client(*Client.load_client(sample_client_folder))
    client.parse_samples()

    # Run the checks
    for i in range(100):
        result = gemini_checker(client.docx_df, client.pdf_df, client.png_df)
        print(f"Gemini result: {result}")