import RPi.GPIO as GPIO
import json
from pprint import pprint
import urllib.request

# Set numbering scheme to BCM
GPIO.setmode(GPIO.BCM)

# Initialize GPIO17 (Pin 11), which controls the relay
# Should be an output and set high, because relay is active-low
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)

# Initialize GPIO27 (Pin 13), which is connected to one of the magnet sensor wires
# [the other magnet sensor wire is connected to ground on pin 9]
# Should be an input with the pull-up resistor enabled
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Need to get the current desired configuration from the cloud app
# Retrieve the JSON file
i = 6212
response = urllib.request.urlopen("http://devops-tutorial-1-jploewen-1945.mybluemix.net/garages/" + str(i))
# Decode response with proper charset
output = response.read().decode('utf-8')
# Load output string into JSON
data = json.loads(output)

# Clean up GPIO on exit
GPIO.cleanup()