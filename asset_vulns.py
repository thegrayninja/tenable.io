#github.com/thegrayninja
#2.1.2

#v2.1.2 - cleaning up code, removing temporary files. Also updated link so it returns correct data!!
#changes were made on tenable's back end, having to revamp the old version..and this is the result
#v2.0 involves single lookup. v2.1 will deal with importing a file

import json
import requests

from auth_file import tenable_header

#ORDER OF OPERATIONS
#
#main()
#GetFileName()
#DownloadAssetVulns()
#VulnsToCSV()
#



def GetFileName():
	
	filename = raw_input("Please enter filename: ")
	myfile = open(filename, "r")
	myfile_contents = myfile.readlines()
	myfile.close()
	
	return myfile_contents



def VulnsToCSV(AllAssetHostnames, AssetResultsInJson):
	results = ""
	counter = 0

	data = AssetResultsInJson

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


		results = results + "%s,%s,%s\n" % (AllAssetHostnames,vuln_severity,vuln_name)

		counter += 1
	return results





def DownloadAssetVulns(AllAssetHostnames):

	#downloads as json, must save to file before parsing the contents
	NewResults = "Hostname,Severity,Vuln_Name\n"
	for i in AllAssetHostnames:
		hostname = i.lower()
		hostname = hostname.replace("\n","")
		agent_url = 'https://cloud.tenable.com/workbenches/vulnerabilities?filter.0.quality=match&filter.0.filter=host.hostname&filter.0.value=%s*' % (hostname)
		agent_url_request = requests.get(agent_url, headers=tenable_header)


		ResultsInJson = agent_url_request.json()

		NewResults += VulnsToCSV(hostname, ResultsInJson)
		print("....")
		

	#this is the csv containing all asset vulns
	temp_final_csv = open("my_new_awesome_file.csv", "w")
	temp_final_csv.write(NewResults)
	temp_final_csv.close()
	print("....\n....\ndone\n....\n....")

	return 0





def main():
	#get file name	
	AssetHostname = GetFileName()

	#filter vulns per host. using VulnsToCSV(), save to file
	DownloadAssetVulns(AssetHostname)



	



if __name__ == main():
	main()	

