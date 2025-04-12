from time import sleep

from api.client import ApiInterface
from logic.decision_maker import make_decision


def main():
    api_interface = ApiInterface()
    api_interface.start_game()

    while True:
        print(f"\n📂 Saving client documents...")
        api_interface.save_client_data()

        decision = make_decision(api_interface.client_data)
        print(f"🧠 Decision: {decision}")

        api_interface.send_decision(decision)
        print(f"✅ Decision sent! Current score: {api_interface.score}")

        if api_interface.status == "gameover":
            print("\n💀 Game Over!")
            print(f"🏆 Final Score: {api_interface.score}")
            break

        # Optional Delay
        sleep(1)


if __name__ == "__main__":
    main()