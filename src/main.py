class GameEngine:
    def __init__(self, player_name: str):
        ...

    def run(self):
        while True:
            client_data = self.client.start_game()
            parsed_data = self.parser.parse_all(client_data)
            checker = ConsistencyChecker(parsed_data)
            decision = "Accept" if checker.is_consistent() else "Reject"
            result = self.client.send_decision(...)

            if result["status"] == "gameover":
                break
