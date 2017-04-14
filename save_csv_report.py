#github.com/thegrayninja
import json
import requests
import time
import csv

from auth_file import tenable_header

scan_id = raw_input("The following requests can be located within scan_and_report_id.txt.\n\nEnter Scan ID: ")
report_id = raw_input("Enter Report ID: ")


#status_url = 'https://cloud.tenable.com/scans/%s/export/%s/status' % (scan_id,report_id["file"])
status_url = 'https://cloud.tenable.com/scans/%s/export/%s/status' % (scan_id,report_id)

#when ready, download the file and and save it to the input provided by the user +.tmp
report_name_user = raw_input("Please enter name for report: ")
report_name_user_temp = "%s.tmp" % (report_name_user)

def download_report():
	timer = 0
	while 1 == 1:
		export_scan = requests.get(status_url, headers=(tenable_header))
		if export_scan.content == '{"status":"ready"}':
			url = 'https://cloud.tenable.com/scans/%s/export/%s/download' % (scan_id,report_id)
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
