#github.com/thegrayninja
#same as original, but imports the tenable_header info, searches based on hostname
#and added a deletion elif based on age (time.time()). roughly deletes agents that
#haven't been scanned in 60 days

import json
import requests
import time

from auth_file import tenable_header


deleted_count = 0

def is_in(ipfilter, agentname, lastscanned, agentid, agentip):
	timediff = 7872650 #roughly 60 days
	if ipfilter in agentname:
		if lastscanned == None:
			currenttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
			url = 'https://cloud.tenable.com/scanners/1/agents/%s' % (agentid)
			stale_agents = requests.delete(url, headers=tenable_header)
			newentry = ("%s (%s) was deleted at %s" %(agentname, agentip, currenttime))
			newFile = open("tenable_deleted_assets.log", "a")
			newFile.write("%s\n" % (newentry))
			newFile.close()
			print(newentry)		
			time.sleep(.3)
			global deleted_count
			deleted_count += 1
		elif (lastscanned + timediff) < time.time():
			currenttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
			url = 'https://cloud.tenable.com/scanners/1/agents/%s' % (agentid)
			stale_agents = requests.delete(url, headers=tenable_header)
			newentry = ("%s (%s) was deleted at %s" %(agentname, agentip, currenttime))
			newFile = open("tenable_deleted_assets.log", "a")
			newFile.write("%s\n" % (newentry))
			newFile.close()
			print(newentry)		
			time.sleep(.3)
			deleted_count += 1
			
			
tempFile_data = requests.get('https://cloud.tenable.com/scanners/1/agents', headers=tenable_header)

tempFile = open("temp.json", "w")
tempFile.write(tempFile_data.content)
tempFile.close()


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
		is_in("win7", agent_name, agent_age, agent_id, agent_ip)
		counter += 1

print(deleted_count)
print("tenable_deleted_assets.log has been saved to your current directory")
