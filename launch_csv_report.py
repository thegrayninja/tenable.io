#github.com/thegrayninja

import json
import requests
import time
import csv

from auth_file import tenable_header

#presents user the list of all scans plus the scan ID
url_main = 'https://cloud.tenable.com/scans'

temp_scan_list_data = requests.get(url_main, headers=tenable_header)

temp_scan_list = open("temp_scan_list.json", "w")
temp_scan_list.write(temp_scan_list_data.content)
temp_scan_list.close()


scan_list_data = "temp_scan_list.json"
with open (scan_list_data, "r") as scan_list:
	counter = 0
	results = ""
	#agent_scanned = ""
	data = json.load(scan_list)
	for i in (data["scans"]):
		scans_name = (data["scans"][counter]["name"])
		scans_id = (data["scans"][counter]["id"])
		results = results + "\n%s,%s" % (scans_name, scans_id)				
		counter += 1

print (results)
scan_id = raw_input("Please enter the Scan ID: ")
##user now has selected the scan ID to use, proceeding to start the scan in csv format

params = {'format':'csv'}			
#filters = {'filters':[{'filter': 'plugin.attributes.cve.raw','quality': 'eq','value': 'CVE-2013-1609'}], 'filter.search_type':'and'}

create_report_url = 'https://cloud.tenable.com/scans/%s/export' % (scan_id)

create_report = requests.post(create_report_url, data=(params), headers=(tenable_header))

#this method is required to create a dictionary of the provided report id
temp_reportFile = open("temp_id.py", "w")
temp_reportFile.write("report_id = %s" % (create_report.content))
temp_reportFile.close()

from temp_id import report_id

store_id_in_File = open("scan_and_report_id.txt", "a")
store_id_in_File.write("\nscan id:%s;report id:%s" % (scan_id,report_id["file"]))
store_id_in_File.close()


print("report id: %s" %(report_id["file"]))
#now checks the status of the report via the report id
status_url = 'https://cloud.tenable.com/scans/%s/export/%s/status' % (scan_id,report_id["file"])
export_scan = requests.get(status_url, headers=(tenable_header))
print("The report is running. Please check back later to download the report using \'save_csv_report.py\'")
