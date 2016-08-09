# Testing the API and testing Git
import json
from pprint import pprint
import urllib.request

# Need to test API in range 6212-6215
for i in range(6212,6216,1):
    # Retrieve the JSON file
    response = urllib.request.urlopen("http://devops-tutorial-1-jploewen-1945.mybluemix.net/garages/" + str(i))
    output = response.read().decode('utf-8')
    data = json.loads(output)
    pprint(data)