#github.com/thegrayninja
#for use with: curl -H "X-ApiKeys: accessKey=; secretKey=" https://cloud.tenable.com/scanners/1/agents >> all_agents.json 
#simply returns all agent IP, Hostname and OS

import json

with open ('all_agents.json') as data_file:
	counter = 0
	results = ""
	data = json.load(data_file)
	for i in (data["agents"]):
		agent_ip = (data["agents"][x]["ip"])
		agent_os = (data["agents"][x]["platform"])
		agent_name = (data["agents"][x]["name"])
		x += 1
		msg = msg + "\n%s,%s,%s" % (agent_ip, agent_name, agent_os)
print (msg)
