#github.com/thegrayninja


import requests

from auth_file import tenable_header

print("calculating...")

for i in "a":
	TempData = requests.get('https://cloud.tenable.com/scanners/1/agents', headers=tenable_header)
	if TempData.content == "Please retry request.":
		print("tenable.io appears to be offline")
	AssetData = TempData.json()

	counter = 0
	try:
		AssetData
		for i in (AssetData["agents"]):
			counter += 1
		print ("%d agents" % (counter+1))
	except: 
		print("There was an error saving the agent information")
