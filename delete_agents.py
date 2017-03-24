#github.com/thegrayninja
#deletes non-scanned agents based on an IP filter

import json
import requests
import time


tenable_header = {'X-ApiKeys':'accessKey=; secretKey='}



def is_in(ipfilter, agentip, lastscanned, agentid):
	currenttime = time.time()
	if ipfilter in agentip:
		if lastscanned == None:
			url = 'https://cloud.tenable.com/scanners/1/agents/%s' % (agentid)
			stale_agents = requests.delete(url, headers=tenable_header)
			print ("%s was deleted" %(agentip))

			
tempFile_data = requests.get('https://cloud.tenable.com/scanners/1/agents', headers=tenable_header)

tempFile = open("temp.json", "w")
tempFile.write(tempFile_data.content)
tempFile.close()
#currenttime = time.time()

originalFile = "temp.json"
with open (originalFile, "r") as data_file:
	counter = 0
	results = ""
	agent_scanned = ""
	data = json.load(data_file)
	for i in (data["agents"]):
		agent_ip = (data["agents"][counter]["ip"])
		agent_age = (data["agents"][counter]["last_scanned"])
		agent_name = (data["agents"][counter]["name"])
		agent_id = (data["agents"][counter]["id"])
		is_in("192.168.1.", agent_ip, agent_age, agent_id)
		counter += 1
