import os
import pandas as pd
import google.generativeai as genai
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def build_prompt(profile_text, narrative_text):
    return f"""
You are a consistency-checking assistant for a financial institution.

Here is the client's **structured profile**:
{profile_text}

Here is the client's **narrative background**:
{narrative_text}

Please identify any inconsistencies between the structured profile and the narrative summary. 
Be specific and list them per section if possible (e.g., Family, Education, Wealth). 
If everything is consistent, say so.
"""


def check_consistency_with_gemini(profile, narrative, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")  # or use 'gemini-pro'
    prompt = build_prompt(profile, narrative)
    response = model.generate_content(prompt)
    return response.text


# ---- MAIN ----
if __name__ == "__main__":
    current_folder = os.getcwd()
    file_path = os.path.join(current_folder, f"FileComparisonData/")

    passport = pd.read_csv(f"{file_path}passport_info_same_name.csv")
    profile = pd.read_csv(f"{file_path}profile_preproc_same_name.csv")
    account = pd.read_csv(f"{file_path}pdf_prepro.csv")
    data = f"Passport: \n{passport}\n\nProfile: \n{profile}\n\nAccount: \n{account}"
    prompt = """
    Analyze the following documents of a person (ID card text, CV/resume, other documents) for:
    1. **Consistency & Accuracy**: Do the name, date of birth, address, and other personal details match across all documents? Are there any obvious typos or discrepancies?
    2. **Trustworthiness**: Are there signs of fraudulent intent (e.g., fake data, contradictory information)?
    3. **Completeness**: Are all required fields present and correctly filled?

    **Output Format**:
    - If **no errors or inconsistencies** are found and the person is deemed trustworthy:
      **"Accept"**
    - If **errors, inconsistencies, or doubts about trustworthiness** exist:
      **"Reject"**

    **Rules**:
    - No explanations, reasoning, or additional text—only "Accept" or "Reject" add a "," and the reason behind.
    - Be very strict: Even a minor error leads to "Reject".
    - Prioritize data consistency across all documents.

    **Documents to Analyze**:
    {input_documents}
    """

    # Get your Gemini API key from environment

    if not API_KEY:
        raise Exception("Please set the GEMINI_API_KEY environment variable.")

    result = check_consistency_with_gemini(prompt, data, API_KEY)
    print("\n🎯 Gemini Consistency Check Result:\n")
    print(result)
