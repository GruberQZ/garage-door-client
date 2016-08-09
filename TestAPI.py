# Testing the API and testing Git
import json
from pprint import pprint
import urllib.request

# Need to test APIs at /6212, /6213, /6214, and /6215
for i in range(6212,6216,1):
    # Retrieve the JSON file
    response = urllib.request.urlopen("http://devops-tutorial-1-jploewen-1945.mybluemix.net/garages/" + str(i))
    # Decode response with proper charset
    output = response.read().decode('utf-8')
    # Load output string into JSON
    data = json.loads(output)
    # Pretty print data to ensure it came in correctly
    pprint(data)