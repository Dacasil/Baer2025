from datetime import datetime


def timestamp():
    """Returns the current timestamp in ISO format."""
    return datetime.now().isoformat(timespec="seconds").replace(":", "").replace("-", "")
