#github.com/thegrayninja


import json
import requests
#import time

from auth_file import tenable_header


search_list_prompt = raw_input("Need to input search ranges. Column formatted, no wildcards.\nPlease Enter File Name: ")
#search_list_prompt = "new_agent_list.txt"
with open(search_list_prompt, "r") as SearchList:
	import_search_strings=SearchList.readlines()
SearchList.close()



tempFile_data = requests.get('https://cloud.tenable.com/scanners/1/agents', headers=tenable_header)

if tempFile_data.content == "Please retry request.":
	print("tenable.io appears to be offline")
else:
	tempFile = open("temp_agent_count.json", "w")
	tempFile.write(tempFile_data.content)
	tempFile.close()


originalFile = "temp_agent_count.json"
with open (originalFile, "r") as asset_file:
	counter = 0
	results = ""
	agent_scanned = ""
	tenable_list = ""
	data = json.load(asset_file)
	for i in (data["agents"]):
		agent_name = (data["agents"][counter]["name"])
		tenable_list += "%s\n" % (agent_name)
		counter +=1

added_count = 0
new_agents=[]
for ss in import_search_strings:
	search_string = ss.strip()
	if search_string in tenable_list:
		continue
	else:
		if search_string in new_agents:
			continue
		else:
			new_agents.append(search_string)
		added_count += 1 

with open ("agent_diff.txt", "w") as diff_file:
	for asset in new_agents:
		diff_file.write("%s\n" % (asset))
		print(asset)
diff_file.close()

print (added_count)
