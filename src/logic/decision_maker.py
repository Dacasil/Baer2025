from utils.file_parser import parse_all
from logic.consistency_checker import check_consistency


def make_decision(client_data: dict) -> str:
    parsed_data = parse_all(client_data)
    is_consistent = check_consistency(parsed_data)
    return "Accept" if is_consistent else "Reject"