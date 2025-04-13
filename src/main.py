import os
import sys
from pathlib import Path
from time import sleep
import threading
import webbrowser

from api.interface import ApiInterface
from logic.decision_maker import make_decision
from utils.client import Client
from notebooks.APWebsite import start_website


BASE_DIR = Path(__file__).resolve().parent.parent
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR / "src")

game_run = input("Do you want to run the Algorithm or view the Website?\nType 'Algorithm' for the Algorithm\nType 'Website' for the Website\n->")
if game_run == 'Website':
    start_website()
    print("Website gestartet. Warte auf Buttonpress...")
    exit()
elif game_run == 'Algorithm':
    pass
else:
    print("Wrong Input")
    exit()

def run():
    api_interface = ApiInterface()
    client_id, client_data = api_interface.start_game()

    while True:

        client = Client(client_data, client_id, api_interface.session_id)
        client.save_client_json()
        client.parse_samples()

        decision = make_decision(client)
        print(f"⚖  Decision: {decision}")

        next_client_id, next_client_data, current_label = api_interface.send_decision(
            client_id, decision
        )
        print(f"✉  Decision sent! Current score: {api_interface.score}")
        # client.add_label(current_label) # maybe later

        client_id = next_client_id
        client_data = next_client_data

        if api_interface.status != "active":
            print("\n💀 Game Over!")
            print(f"🏆 Final Score: {api_interface.score}")
            print(f"Status: {api_interface.status}")
            break

        # Optional Delay
        sleep(1)

if __name__ == "__main__":
    run()
