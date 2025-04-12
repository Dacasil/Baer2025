def parse_passport(self, image_bytes: bytes) -> dict:
    ...

def parse_profile(self, docx_bytes: bytes) -> dict:
    ...

def parse_form(self, pdf_bytes: bytes) -> dict:
    ...

def parse_description(self, txt_bytes: bytes) -> dict:
    ...

def parse_all(self, client_data: dict) -> dict:
    """Parses all documents from the client data dictionary."""

    parsed_data = {}
    for key, value in client_data.items():
        if key == "passport":
            parsed_data[key] = parse_passport(value)
        elif key == "profile":
            parsed_data[key] = parse_profile(value)
        elif key == "form":
            parsed_data[key] = parse_form(value)
        elif key == "description":
            parsed_data[key] = parse_description(value)
    return parsed_data