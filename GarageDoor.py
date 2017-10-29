import RPi.GPIO as GPIO
import json
from pprint import pprint
import urllib.request
import random
import time
import sys

class GarageDoor:
    base_url = 'https://devops-tutorial-1-jploewen-1945.mybluemix.net/'
    previousState = None
    desiredState = None
    currentState = None

    # Ignore the sapce id for now
    space_id = None

    def __init__(self, space_id=None):
        self.space_id = space_id
        # self.userid = "extuser"
        # self.passwd = "DRiving4AWorking/sYstem2016"
        self.headers = {
            'Content-type': 'application/json',
            # 'X-TenantID': self.space_id,
        }

    def print_key(self):
        print(self.space_id)
        print(self.base_url)

    def getCloudConfig(self):
        # Need to get the current desired configuration from the cloud app
        # Retrieve the JSON file
        # i = 6211 + random.randint(1,4)
        response = urllib.request.urlopen("http://devops-tutorial-1-jploewen-1945.mybluemix.net/garages/6213")
        # Decode response with proper charset
        output = response.read().decode('utf-8')
        # Load output string into JSON
        jsondata = json.loads(output)
        self.desiredState = jsondata["desiredState"]

    def getPreviousState(self):
        # Reads the saved file to retrieve data about previous session
        pass

    def getCurrentState(self):
        # Reads the GPIO to determine the current status of the garage door
        # Get the current status of the door
        reading = GPIO.input(27)
        # If status is GPIO.LOW, magnet is close so door is closed
        # Else, magnet is not close, door is open
        if reading == GPIO.LOW:
            self.currentState = 'closed'
        elif reading == GPIO.HIGH:
            self.currentState = 'open'
        else:
            self.currentState = None

    def activate(self):
        # Activate relay (simulate garage door button press)
        GPIO.output(17, GPIO.LOW)
        time.sleep(0.4)
        GPIO.output(17, GPIO.HIGH)