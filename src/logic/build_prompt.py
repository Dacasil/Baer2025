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

Remeber:
- A client born in 2000 can be both 24 and 25 years old in 2025
- Consistency of formats like of dates or other items is not enforced and my differ between sources

Answer ONLY with either:
"TRUE" – if a material, non-explainable contradiction exists,
or "FALSE" – if any differences are minor or easily explainable.
"""
