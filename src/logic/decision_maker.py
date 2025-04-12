from logic.checks import trivial_check


def make_decision(client) -> str:
    # Do all checks
    check_results = []
    check_results.append( trivial_check(client.pdf_path) ) # Example check
    check_results.append( trivial_check(client.pdf_path) ) # Example check
    check_results.append( trivial_check(client.pdf_path) ) # Example check
    check_results.append( trivial_check(client.pdf_path) ) # Example check
    # Add more checks as needed

    # Aggregate all checks
    is_accept = all(check_results)

    decision = "Accept" if is_accept else "Reject"
    return decision