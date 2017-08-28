#github.com/thegrayninja
#this is v2.1
#changes were made on tenable's back end, having to revamp the old version..and this is the result
#v2.0 involves single lookup. v2.1 deals with importing a file

import json
import requests
import time
import csv

from auth_file import tenable_header


filename = raw_input("Please enter filename: ")
myfile = open(filename, "r")
myfile_contents = myfile.readlines()
myfile.close()

results = "Hostname,Severity,Vuln_Name\n"
for i in myfile_contents:
	hostname = i.lower()
	hostname = hostname.replace("\n","")
	agent_url = 'https://cloud.tenable.com/workbenches/vulnerabilities?authenticated=false&exploitable=false&filter.0.quality=like&filter.0.filter=host.hostname&filter.0.value=%s&resolvable=false' % (hostname)
	agent_url_request = requests.get(agent_url, headers=tenable_header)




	temp_agent_list = open("temp_agent_list.json", "w")
	temp_agent_list.write(agent_url_request.content)
	temp_agent_list.close()


	agent_list_File = "temp_agent_list.json"
	with open (agent_list_File, "r") as data_file:
		counter = 0

		data = json.load(data_file)
	
		for i in (data["vulnerabilities"]):
			vuln_severity = (data["vulnerabilities"][counter]["severity"])
			vuln_name = (data["vulnerabilities"][counter]["plugin_name"])
			if (vuln_severity == 1):
				vuln_severity = "low"
			elif (vuln_severity == 2):
				vuln_severity = "medium"
			elif (vuln_severity == 3):
				vuln_severity = "high"
			else:
				vuln_severity = "critical"


			results = results + "%s,%s,%s\n" % (hostname,vuln_severity,vuln_name)

			counter += 1


temp_final_csv = open("my_new_awesome_file.csv", "w")
temp_final_csv.write(results)
temp_final_csv.close()
print("....\n....\ndone\n....\n....")
	

