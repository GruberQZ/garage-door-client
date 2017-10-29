#!/usr/bin/env python3

import RPi.GPIO as GPIO
import sys
import time

# Check arguments to see what the desired state is
# Exit if wrong number of arguments specified
if len(sys.argv) != 2:
	print("Wrong number of arguments specified!")
	sys.exit()

# Define the wrong position for the garage door to be in
# based on the desired position
desiredPosition = sys.argv[1].lower()
wrongPosition = None
if desiredPosition == "closed":
	wrongPosition = 1
elif desiredPosition == "open":
	wrongPosition = 0
else:
	print("Argument (desired state) should be \"open\" or \"closed\".")
	sys.exit()

# Turn off GPIO warnings
GPIO.setwarnings(False)

# Initialize GPIO for garage door communication
# Set numbering scheme to BCM
GPIO.setmode(GPIO.BCM)

# Initialize GPIO17 (Pin 11), which controls the relay
# Should be an output and set high, because relay is active-low
GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)

# Initialize GPIO27 (Pin 13), which is connected to one of the magnet sensor wires
# [the other magnet sensor wire is connected to ground on pin 9]
# Should be an input with the pull-up resistor enabled
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Read pin attached to GPIO27, which is connected to one of the magnet sensor wires
# Only activate the relay if the garage door is in the wrong position
if GPIO.input(27) == wrongPosition:
	# Activate the relay
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.6)
    GPIO.output(17, GPIO.HIGH)

