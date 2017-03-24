#github.com/thegrayninja
#for use with: curl -H "X-ApiKeys: accessKey=; secretKey=" https://cloud.tenable.com/scanners/1/agents >> all_agents.json 
#currently, simply returns all agent IP, Hostname, OS and ID

import json
originalFile = raw_input("Please Enter JSON file name: ")
with open (originalFile, "r") as data_file:
	counter = 0
	results = ""
	data = json.load(data_file)
	for i in (data["agents"]):
		agent_ip = (data["agents"][counter]["ip"])
		agent_os = (data["agents"][counter]["platform"])
		agent_name = (data["agents"][counter]["name"])
		agent_id = (data["agents"][counter]["id"])
		counter += 1
		results = results + "\n%s,%s,%s,%s" % (agent_ip, agent_name, agent_os, agent_id)


newFile = open(originalFile.replace('.json', '.csv'), "w")
newFile.write(results)
print ("%s has been saved into your current directory!" % (originalFile.replace('.json', '.csv'))) 
newFile.close()
