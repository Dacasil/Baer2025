from logic.checks import trivial_check
from notebooks.APGemini import gemini_check

def make_decision(client) -> str:
    # Do all checks
    check_results = []
    check_results.append( gemini_check(account = client.pdf_df,profile = client.docx_df) )

    # Add more checks as needed

    # Aggregate all checks
    print(f"results: {check_results}")
    is_accept = all(check_results)

    decision = "Accept" if is_accept else "Reject"
    return decision