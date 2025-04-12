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
import pandas as pd
import google.generativeai as genai


def load_csv_as_text(file_path, key_field="Field", value_field="Value", delimiter=": "):
    """
    Loads a CSV file and converts each row into a line of text in the format:
      key [delimiter] value

    Parameters:
      file_path (str): Path to the CSV file.
      key_field (str): The name of the key column (default "Field").
      value_field (str): The name of the value column (default "Value").
      delimiter (str): The string to separate key and value.

    Returns:
      str: A text block representing the CSV content.
    """
    df = pd.read_csv(file_path)
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


def main():
    # Paths to your three CSV files.
    profile_csv = "profile_preprocessed.csv"  # columns: Field, Value
    narrative_csv = "pdf_preprocessed.csv"  # columns: Field, Value
    passport_csv = "passport_info.csv"  # columns: Field, Value

    # Convert each CSV into a text representation.
    profile_text = load_csv_as_text(profile_csv)
    narrative_text = load_csv_as_text(narrative_csv)
    passport_text = load_csv_as_text(passport_csv)

    # Get your Gemini API key. If you want, you can store it in an env var named GEMINI_API_KEY.
    api_key = "AIzaSyC41lPgNFNvt0TlpXIz5NeIhfGMLPTOKXo"
    if not api_key:
        raise Exception(
            "No Gemini API key found. Set GEMINI_API_KEY as an environment variable or place it in the code.")

    # Call Gemini to check consistency.
    result = check_consistency_with_gemini(profile_text, narrative_text, passport_text, api_key)
    print("Gemini Consistency Check Result:", result)


if __name__ == "__main__":
    main()
