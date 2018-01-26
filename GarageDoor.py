
import json
from pprint import pprint
import requests
import random
import time
import sys

class GarageDoor:
    base_url = 'https://garage-door.mybluemix.net/'

    def __init__(self, door_id=None):
        self.door_id = door_id
        # self.userid = "extuser"
        # self.passwd = "DRiving4AWorking/sYstem2016"
        self.headers = {
            'Content-type': 'application/json'
        }

    def print_key(self):
        print(self.space_id)
        print(self.base_url)

    def getDoorConfig(self):
        url = self.base_url + "garages/" + self.door_id 
        #print ("Get Door Config")
        #print ("url=%s" % (url))

        r = requests.get(url, headers=self.headers, verify=True)
    
        print ("<%d>" % (r.status_code))
        
        if (r.status_code>=200 and r.status_code<300):
            return r.json()
            #Sample:
            #{"id":6212,"name":"Main door home","lastUpdated":"2017-11-30T14:48:00","desiredState":"open","status":"open"}
        return None

    def doorStateChange(self, newState):
        url = self.base_url + "garages/" + self.door_id 
        data = {"id": self.door_id, "state": newState }

        start_time = time.time()
        r = requests.post(url, headers=self.headers, data=data, verify=True)
    
        print ("<%d>" % (r.status_code))
        
        if (r.status_code>=200 and r.status_code<300):
            return r.json()
        return None

gd = GarageDoor("6212")
config = gd.getDoorConfig()
if config!=None:
    print ("%s" % (config))
    