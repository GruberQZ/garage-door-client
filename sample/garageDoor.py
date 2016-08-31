import json
import sys
import requests
from requests.auth import HTTPBasicAuth


class garageDoorAPI:
	base_url = 'https://devops-tutorial-1-jploewen-1945.mybluemix.net/'
	
	#Ignore the sapce id for now
	space_id = None

	def __init__(self, space_id=None):
		self.space_id = space_id
		#self.userid = "extuser"
    	#self.passwd = "DRiving4AWorking/sYstem2016"
    		
		
		self.headers = {
			'Content-type': 'application/json',
			#'X-TenantID': self.space_id,
		}

	def print_key(self):
		print self.space_id
		print self.base_url
	
	
	def getGarages(self):
		#curl -k http://devops-tutorial-1-jploewen-1945.mybluemix.net/garages
		#URL to send request to
		url = self.base_url + 'garages'
		
			
		#send GET request
		r = requests.get(url, headers=self.headers, verify=False)
		#Not using basic auth yet
		#r = requests.get(url, headers=self.headers, auth=HTTPBasicAuth(self.userid,self.passwd), verify=False)
		
		#Let the user know how it went
		print "Get garages"
		print r
		
		#Return the JSON data
		return r.json()

	def getGarage(self, garageId):
		#curl -k http://devops-tutorial-1-jploewen-1945.mybluemix.net/garages/6212
		#URL to send request to
		url = self.base_url + 'garages/' + str(garageId)
		
			
		#send GET request
		r = requests.get(url, headers=self.headers, verify=False)
		#Not using basic auth yet
		#r = requests.get(url, headers=self.headers, auth=HTTPBasicAuth(self.userid,self.passwd), verify=False)
		
		#Let the user know how it went		
		print r
		
		#Return the JSON data
		return r.json()