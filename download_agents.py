#github.com/thegrayninja
#download the latest nessus agents without going through the GUI


#full url string:
#http://downloads.nessus.org/nessus3dl.php?file=NessusAgent-6.11.1-Win32.msi&licence_accept=yes&t=1ea0fe39437453a7e12a12115194e8e5

#simply updated the version# in the "NessusAgent-6.11.1" string in the url. 

import os


agent_list = ["-amzn.x86_64.rpm", "-debian6_amd64.deb", "es5.x86_64.rpm",
				"-es6.x86_64.rpm", "-es7.x86_64.rpm", "-fc20.x86_64.rpm", 
				"-suse11.x86_64.rpm", "-suse12.x86_64.rpm", "-ubuntu910_amd64.deb",
				"-ubuntu1110_amd64.deb", ".dmg", "-x64.msi"]

agent_prefix = "NessusAgent-6.11.1"

for i in agent_list:
	file_name = agent_prefix + i.strip()
	wget_format = 'wget -O %s "http://downloads.nessus.org/nessus3dl.php?file=NessusAgent-6.11.1%s&licence_accept=yes&t=1ea0fe39437453a7e12a12115194e8e5"' % (file_name, i.strip())
	os.system(wget_format)
agent_list.close()

print("Your files have been saved to your current directory!")
