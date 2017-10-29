import RPi.GPIO as GPIO
import json
from pprint import pprint
import urllib.request
import random
import time
import sys

# Initialize GPIO for garage door communication
# Set numbering scheme to BCM
GPIO.setmode(GPIO.BCM)

# Initialize GPIO17 (Pin 11), which controls the relay
# Should be an output and set high, because relay is active-low
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)

# Initialize GPIO27 (Pin 13), which is connected to one of the magnet sensor wires
# [the other magnet sensor wire is connected to ground on pin 9]
# Should be an input with the pull-up resistor enabled
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Make sure desiredState is valid, exit if it isn't
if desired["desiredState"] != 'closed' and desired["desiredState"] != 'open':
    # Exit program for safety
    GPIO.cleanup()
    sys.exit()

# Process the data that comes back
# If status and desiredState are not the same, activate the relay to correct it
if desired["desiredState"] != status:
    # Activate the relay
    GPIO.output(17,GPIO.LOW)
    time.sleep(0.4)
    GPIO.output(17,GPIO.HIGH)

# Clean up GPIO on exit
GPIO.cleanup()