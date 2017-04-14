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
filters = {'filters':'["filter": "plugin.attributes.cve.raw","quality": "eq","value": "CVE-2013-1609"]'}

create_report_url = 'https://cloud.tenable.com/scans/%s/export' % (scan_id)

create_report = requests.post(create_report_url, params, filters, headers=(tenable_header))

#this method is required to create a dictionary of the provided report id
temp_reportFile = open("temp_id.py", "w")
temp_reportFile.write("report_id = %s" % (create_report.content))
temp_reportFile.close()

from temp_id import report_id
print("report id: %s" %(report_id["file"]))
#now checks the status of the report via the report id
status_url = 'https://cloud.tenable.com/scans/%s/export/%s/status' % (scan_id,report_id["file"])

#when ready, download the file and and save it to the input provided by the user +.tmp
report_name_user = raw_input("Please enter name for report: ")
report_name_user_temp = "%s.tmp" % (report_name_user)

def download_report():
	timer = 0
	while 1 == 1:
		export_scan = requests.get(status_url, headers=(tenable_header))
		if export_scan.content == '{"status":"ready"}':
			url = 'https://cloud.tenable.com/scans/%s/export/%s/download' % (scan_id,report_id["file"])
			download_report = requests.get(url, headers=tenable_header)
			newFile = open(report_name_user_temp, "w")
			newFile.write(download_report.content)
			newFile.close()			
			print ("Downloaded!")
			break
		else:
			print ("%s (%d seconds)" % (export_scan.content, timer))
			timer += 10
			time.sleep(10)
		
download_report()


#since the csv is huge, parse the data and save a new file, -.tmp	
def delete_rows(old_report, new_report):
	updatedlines = ""
	with open(old_report, 'rb') as csvfile:
		delimfile = csv.DictReader(csvfile)
		for row in delimfile:
			if 'None' not in row['Risk']:
				updatedlines = updatedlines + '%s,%s,%s,%s,%s,%s,%s\n' %(row['Host'], row['Risk'], row['CVSS'], row['CVE'], row['Port'], row['Protocol'], row['Name'])
	csvfile.close()

	#to save the good stuff to a new file
	with open(new_report, 'w') as csvnew:
		csvnew.write('Host, Risk, CVSS, CVE, Port, Protocol, Name\n')
		csvnew.write(updatedlines)

	csvnew.close()


delete_rows(report_name_user_temp,report_name_user)

#show proof to the user that the report has been saved
print ("%s has been saved to your local directory!" %(report_name_user))


