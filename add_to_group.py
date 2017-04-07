#github.com/thegrayninja

import json
import requests
import time

from auth_file import tenable_header

search_list_prompt = raw_input("Need to input search ranges. Column formatted, no wildcards.\nPlease Enter File Name: ")
with open(search_list_prompt, "r") as SearchList:
	import_search_strings=SearchList.readlines()
SearchList.close()

added_count = 0



######################
######################
######################
#Getting Group Info, for Group ID Request
#
#
tempFile_get_group_data = requests.get('https://cloud.tenable.com/scanners/1/agent-groups', headers=tenable_header)

tempFile_get_group = open("temp_get_group.json", "w")
tempFile_get_group.write(tempFile_get_group_data.content)
tempFile_get_group.close()

get_group_File = "temp_get_group.json"
with open (get_group_File, "r") as group_data_file:
	temp_counter = 0
	results = ""
	agent_scanned = ""
	data = json.load(group_data_file)
	for i in (data["groups"]):
		temp_group_name = (data["groups"][temp_counter]["name"])
		temp_group_id = (data["groups"][temp_counter]["id"])
		print ("name:%s,id:%s" % (temp_group_name, temp_group_id))
		temp_counter += 1


######################
######################
######################
#Asking user to input group ID from above list
#
search_group_id = raw_input("Please Enter Group ID: ")



def is_in(agentip, agentid, agentname):
	global import_search_strings	
	global search_group_id
	for ss in import_search_strings:
		search_string = ss.strip()
		if search_string in agentip:
			url = 'https://cloud.tenable.com/scanners/1/agent-groups/%s/agents/%s' % (search_group_id, agentid)
			temp_container = requests.put(url, headers=tenable_header)
			newentry = ("%s - %s was added to the group %s" % (agentip, agentname, search_group_id))		
			newFile = open("tenable_added_to_group.log", "a")
			newFile.write("%s\n" % (newentry))
			newFile.close()		
			print (newentry)
			time.sleep(.3)		
			global added_count
			added_count += 1
							
			
tempFile_data = requests.get('https://cloud.tenable.com/scanners/1/agents', headers=tenable_header)

tempFile = open("temp_add_group.json", "w")
tempFile.write(tempFile_data.content)
tempFile.close()


originalFile = "temp_add_group.json"
with open (originalFile, "r") as data_file:
	counter = 0
	results = ""
	agent_scanned = ""
	data = json.load(data_file)
	for i in (data["agents"]):
		agent_ip = (data["agents"][counter]["ip"])
		agent_name = (data["agents"][counter]["name"])
		agent_id = (data["agents"][counter]["id"])
		is_in(agent_ip, agent_id, agent_name)
		counter += 1

print("%d agents were added." %(added_count))
print("tenable_added_to_group.log has been saved to your current directory")
