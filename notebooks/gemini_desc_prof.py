import os
import pandas as pd
import google.generativeai as genai

def load_structured_profile(filepath):
    df = pd.read_csv(filepath)
    return dict(zip(df["Field"], df["Value"]))

def load_narrative(filepath):
    df = pd.read_csv(filepath)
    return dict(zip(df["Label"], df["Text"]))

def format_profile(profile):
    """
    Converts the structured profile dictionary to readable sentences.
    """
    lines = [f"{key}: {value}" for key, value in profile.items()]
    return "\n".join(lines)

def format_narrative(narrative):
    """
    Combines labeled narrative text into a formatted sectioned summary.
    """
    sections = [f"{label}:\n{text.strip()}" for label, text in narrative.items()]
    return "\n\n".join(sections)

def build_prompt_2(text):
    return f"""You are a senior compliance analyst at a private bank.

Your job is to determine whether the discrepancy described below qualifies as a **SERIOUS contradiction** — meaning a **clear, direct factual conflict** or **evidence of misreporting or potential fraud**.

You must **only return TRUE** if at least one of the following applies:
- There is a fact in one document that is directly **refuted** by the other
- There is an obvious **data conflict**, not explainable by phrasing or rounding
- There is a mismatch in core facts such as age, employment status, or assets that **cannot logically be reconciled**

You must **return FALSE** if:
- The issue is a **minor inconsistency**, rounding, vague phrasing, or missing fields
- The discrepancy is reasonable or can be explained by timing (e.g., retirement year vs current age)
- The difference is a **possible reporting ambiguity**, not a contradiction

Please return only **TRUE** or **FALSE** — no extra explanation.

Discrepancy to evaluate:
{text}
"""


def build_prompt(profile_text, narrative_text):
    return f"""
You are a professional onboarding auditor at a private bank.

Your job is to check for **material factual contradictions** between two sources:
1. A structured profile (form fields)
2. A narrative description (free-text summary)

You must only report issues that are:
- Clearly conflicting facts (e.g. one says "married", the other "divorced")
- Direct contradictions that cannot both be true (e.g. says "owns a company", but elsewhere says "never worked")
- Indicators of misreporting or falsified data (e.g. birthdate and age don't match)

🚫 Do **NOT** report things that are:
- Small differences in numbers (e.g. EUR 548,000 vs '500,000–1M')
- Slightly ambiguous or missing narrative details (e.g. inheritance not restated)
- Common form-vs-text mismatches (e.g. no property checkbox ticked but not mentioned in summary)
- Reasonable omissions due to formatting (e.g. unclear income after retirement)

👉 You should only report **material, irreconcilable conflicts** — not data that may just require clarification.

---

📝 Output format:
Report per section (e.g., Family, Education, Occupation, Wealth). 
If no serious conflicts are found, return exactly: **Everything appears consistent.**

---

**Structured Profile:**
{profile_text}

---

**Narrative Background:**
{narrative_text}
"""

def check_consistency_with_gemini(profile, narrative, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-pro")  # or use 'gemini-pro'

    profile_text = format_profile(profile)
    narrative_text = format_narrative(narrative)
    prompt = build_prompt(profile_text, narrative_text)

    response = model.generate_content(prompt)
    print(response.text)
    p2 = build_prompt_2(response.text)
    response = model.generate_content(p2)
    return response.text

# ---- MAIN ----
if __name__ == "__main__":
    profile_csv = "profile_preprocessed.csv"
    narrative_csv = "description_split.csv"

    profile_data = load_structured_profile(profile_csv)
    narrative_data = load_narrative(narrative_csv)

    # Get your Gemini API key from environment
    api_key = "..."
    if not api_key:
        raise Exception("Please set the GEMINI_API_KEY environment variable.")

    result = check_consistency_with_gemini(profile_data, narrative_data, api_key)
    print("\n🎯 Gemini Consistency Check Result:\n")
    print(result)
