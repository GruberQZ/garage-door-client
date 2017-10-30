import RPi.GPIO as GPIO
import requests

# Initialize GPIO for garage door communication
# Set numbering scheme to BCM
GPIO.setmode(GPIO.BCM)

# Initialize GPIO27, which is connected to one of the magnet sensor wires
# [the other magnet sensor wire is connected to ground on pin 9]
# Should be an input with the pull-up resistor enabled
# When the garage door is open and the magnet is not near the sensor, GPIO27 will be 1
# When the garage door is closed and the magnet is near the sensor, GPIO27 will be 0
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# # Define connection to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client.garage
# log_collection = db.log

# Define interrupt functions that trigger when the door opens or closes
def update_door_log(channel):
	# Door just opened
	if GPIO.input(27):
		print("Door just opened!")
		# # Post to the log API that the door has opened
		# r = requests.post('http://localhost/activitylog', data = {"status": "open"})
		# # Print return message from API for debugging purposes
		# print(r.json().message)
	# Door just closed
	else:
		print("Door just closed!")
		# # Post to the log API that the door has closed
		# r = requests.post('http://localhost/activitylog', data = {"status": "closed"})
		# # Print return message from API for debugging purposes
		# print(r.json().message)

# Configure interrupt for door opening
GPIO.add_event_detect(27, GPIO.BOTH, callback = update_door_log, bouncetime = 600)

# Run infinitely until keyboard interrupt or system shutdown
try:
	print("Ready to detect door state changes...")
	# Print initial state
	if GPIO.input(27):
		print("Initial door state: open")
	else:
		print("Initial door state: closed")
	while True:
		pass
except:
	print("Shutting down...")
	GPIO.cleanup()
