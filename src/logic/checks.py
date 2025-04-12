from random import randint
from utils.file_parser import parse_passport

def trivial_check(passport_path) -> bool:
    parsed_data = parse_passport(passport_path)

    return True # Always returns True for testing purposes