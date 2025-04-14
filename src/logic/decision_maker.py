from logic.checks import trivial_check
from logic.APFileComparison import comparePrecise
from logic.gemini_checker import gemini_checker


def make_decision(client) -> str:
    # Do all checks
    check_results = []
    check_results.append(
        comparePrecise(
            account=client.pdf_df.copy(),
            profile=client.docx_df.copy(),
            passport=client.png_df.copy(),
        )
    )
    if not check_results[-1]:
        return "Reject"
    try:
        check_results.append(
            gemini_checker(
                client.docx_df, client.pdf_df, client.pdf_df
            )  # client.png_df
        )
    except:
        print("skipped AI")
    
    #check_results.append(gemini_checker(client.docx_df, client.pdf_df, client.png_df))

    # Add more checks as needed

    # Aggregate all checks
    print(f"results: {check_results}")
    is_accept = all(check_results)

    decision = "Accept" if is_accept else "Reject"
    return decision
