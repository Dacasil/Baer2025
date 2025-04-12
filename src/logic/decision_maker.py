from logic.checks import trivial_check
from logic.gemini_checker import gemini_checker


def make_decision(client) -> str:
    # Do all checks
    check_results = []
    check_results.append( gemini_checker(client) )
    # Add more checks as needed

    # Aggregate all checks
    is_accept = all(check_results)

    decision = "Accept" if is_accept else "Reject"
    return decision