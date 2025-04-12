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

import os
import sys
from pathlib import Path

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

from utils.client import Client

BASE_DIR = Path(__file__).resolve().parent.parent.parent
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR / "src")


def convert_df_to_text(df, key_field="Field", value_field="Value", delimiter=": "):
    lines = []
    for _, row in df.iterrows():
        key = str(row[key_field])
        value = str(row[value_field])
        lines.append(f"{key}{delimiter}{value}")
    return "\n".join(lines)


def build_prompt(profile_text, narrative_text, passport_text):
    """
    Builds a prompt for Gemini to check consistency across three sources:
      1) profile_text
      2) narrative_text
      3) passport_text

    Only output "TRUE" if there is a clear, irreconcilable conflict;
    otherwise, output "FALSE".
    """
    return f"""
You are a senior consistency auditor at a private bank.

Below are three sources of information regarding a single client:

1. **Profile Data** (from a form):
{profile_text}

2. **Narrative Data** (free-text explanation):
{narrative_text}

3. **Passport Data** (official ID fields):
{passport_text}

Please analyze these sources and determine if there is any **material factual contradiction** 
among them. For example, flag a contradiction only if there are clear, unexplainable conflicts 
in key facts (e.g., conflicting dates, employment status, or wealth figures).

Do NOT flag minor differences such as:
- Rounding differences (e.g., €548,000 vs. a range of €500,000–1,000,000)
- Slight differences in phrasing or formatting
- Inconsistencies due to placeholder terms (like "Business" vs "Investments")
- Normal omissions in any one source that do not conflict

Answer ONLY with either:
"TRUE" – if a material, non-explainable contradiction exists,
or "FALSE" – if any differences are minor or easily explainable.
"""


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
    response = model.generate_content(prompt)
    # Return just the model's text output, stripped of whitespace.
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
    negated_string_result = check_consistency_with_gemini(profile_text, narrative_text, passport_text, api_key)
    result = not bool(negated_string_result)

    return result


if __name__ == "__main__":
    # Example usage
    sample_client_folder = next(BASE_DIR.rglob("data/samples/*client-id_*"))

    client = Client(*Client.load_client(sample_client_folder))
    client.parse_samples()

    # Run the checks
    gemini_checker(client.docx_df, client.pdf_df, client.png_df)