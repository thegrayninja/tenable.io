#github.com/thegrayninja

import json
import requests
import time

from auth_file import tenable_header
print("calculating...")


tempFile_data = requests.get('https://cloud.tenable.com/scanners/1/agents', headers=tenable_header)
if tempFile_data.content == "Please retry request.":
	print("tenable.io appears to be offline")
	break
tempFile = open("temp_agent_count.json", "w")
tempFile.write(tempFile_data.content)
tempFile.close()


originalFile = "temp_agent_count.json"
with open (originalFile, "r") as data_file:
	counter = 0
	try:
		data = json.load(data_file)
		for i in (data["agents"]):
			counter += 1
		print ("%d agents" % (counter+1))
	except: 
		print("There was an error saving the agent information")
