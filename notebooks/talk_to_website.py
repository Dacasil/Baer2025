from src.utils.APWebsite import start_website
from threading import Thread

# Start the Flask app in a separate thread
flask_thread = Thread(target=start_website)
flask_thread.start()

print("start")
def work():
    print("yes")

start_website()
var = False

while True:
    if var:  # Check if the button was pressed
        work()
        break  # Exit the loop after executing the function


print("end")

