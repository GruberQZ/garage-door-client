from __future__ import division
import json
import sys
import requests
from garageDoor import garageDoorAPI
import time
import argparse
from pprint import pprint

garage_id = None

#Parser for command line arguments
parser = argparse.ArgumentParser(description="A script that lists synthetic tests for a given spaceid")

#Add an argument for the garage id
parser.add_argument('-g', '--garage_id',
                action="store", dest="garage_id",
                help="Garage id for requested configuration", default=None)


#Parse the arguments
args = parser.parse_args()

#Check if the required arguments are empty
if args.garage_id == None:
    print "ERROR: A garage id is required"
    parser.print_help()
    exit()


def garageDoorConfig(garage_id): 
    
    #Create a request object for our Garage Door server
    garageDoor = garageDoorAPI(space_id=None)

    #Get the config for the given id
    print "Get garage configuration for id = %s" % (garage_id)
    config = garageDoor.getGarage(garage_id)
    
        
    #print time.strftime("%Y-%m-%d %H:%M")
    print config
         
    #{"id":6212,"name":"Main door home","lastUpdated":"2016-07-10T14:48:00","desiredState":"open","status":"open"}
    print 'Garage id = %s for %s' % (config['id'], config['name'])   
    print '  current state = %s, desired state = %s' % (config['status'], config['desiredState'])       
   

garageDoorConfig(args.garage_id)  
