def build_prompt(profile_text, narrative_text, passport_text):
    """
    Builds a prompt for Gemini to check consistency across three sources.
    Returns tuple: (TRUE/FALSE, reasoning)
    """
    return f"""
You are a forensic data consistency analyst at a financial institution. Analyze these three sources:

1. PROFILE DATA (structured form):
{profile_text}

2. NARRATIVE (free-text explanation):
{narrative_text}

3. PASSPORT (machine-readable ID data):
{passport_text}

Flag as TRUE ONLY if there is an UNEXPLAINABLE CONTRADICTION in CORE IDENTITY FIELDS:
- Full legal name (ignore formatting/capitalization differences)
- Date of birth (must match exactly in YYYY-MM-DD format)
- Passport number (exact character match required)
- Nationality is the same in all documents(country names)
- Obvious TYPOS in the name

CRITICAL RULES:
1. Date formats: Accept any unambiguous format if numbers match (e.g., 1967-08-19 vs 19/08/1967)
2. Name variations: Allow for diacritic differences (Kovar/Kovář) and capitalization
3. Passport numbers: Require EXACT alphanumeric match - any discrepancy is critical
4. Formatting errors: Only flag if they create ambiguity (e.g., "19081967" is acceptable if matching other sources when parsed as DDMMYYYY)
5. Wrong country codes are not sufficient for returning TRUE

Output STRICTLY in this format:
[VERDICT]
TRUE/FALSE
[REASONING]
Concise technical explanation of contradictions or confirmation of consistency

Examples of VALID responses:

FALSE
All core identity fields match across sources. Passport date format (DDMMYYYY) differs from profile (YYYY-MM-DD) but represents same calendar date.

TRUE
Passport shows nationality=DE while profile states=FR - country codes conflict.

TRUE
Passport number differs: P<UTOERIK<<SVEN<<<<<<<<<<<<<<< vs P<UTOERIK<<SVEN<<<<<<<<<<<<<<<<< (extra '<' character)
"""
