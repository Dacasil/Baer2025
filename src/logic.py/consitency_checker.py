class ConsistencyChecker:
    def __init__(self, extracted_data: dict):
        self.data = extracted_data

    def is_consistent(self) -> bool:
        ...

    def get_inconsistencies(self) -> list[str]:
        ...
