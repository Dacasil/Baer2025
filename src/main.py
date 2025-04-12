import random
from time import sleep

from api.client import ApiInterface


def make_dummy_decision(client_data: dict) -> str:
    """
    Placeholder decision logic. 
    This will later be replaced with document analysis + consistency check.
    """
    return random.choice(["Accept", "Reject"])  # Dummy logic


if __name__ == "__main__":
    client = ApiInterface()
    client.start_game()

    while True:
        print(f"\n📂 Saving client documents...")
        client.save_client_data()

        decision = make_dummy_decision(client.client_data)
        print(f"🧠 Decision: {decision}")

        client.send_decision(decision)
        print(f"✅ Decision sent! Current score: {client.score}")

        if client.status == "gameover":
            print("\n💀 Game Over!")
            print(f"🏆 Final Score: {client.score}")
            break

        # Optional Delay
        sleep(1)
