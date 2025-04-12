import os
import sys
from pathlib import Path
from time import sleep

from api.interface import ApiInterface
from logic.decision_maker import make_decision
from utils.client import ClientRaw

BASE_DIR = Path(__file__).resolve().parent.parent
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR / "src")

def run():
    api_interface = ApiInterface()
    client_id, client_data = api_interface.start_game()

    while True:

        client = ClientRaw(client_data, client_id, api_interface.session_id) # 4 Blobs & info.json gibt es schon, aber noch nicht label in info.json

        decision = make_decision(client)
        print(f"⚖ Decision: {decision}")
        
        next_client_id, next_client_data, current_label = api_interface.send_decision(client_id, decision)
        print(f"✉ Decision sent! Current score: {api_interface.score}")
        # client.add_label(current_label) # maybe later

        client_id = next_client_id
        client_data = next_client_data

        if api_interface.status == "gameover":
            print("\n💀 Game Over!")
            print(f"🏆 Final Score: {api_interface.score}")
            break

        # Optional Delay
        sleep(1)


if __name__ == "__main__":
    run()