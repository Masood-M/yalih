import os
import re
import sys

# Extracts and appends connection refused links to connectionrefused.txt
# Input Example: python extractconnectionrefuse.py /home/user/Desktop/france-1.log
folderPath = str(sys.argv[1])
output = ""
with open(folderPath) as f:
	lines = f.readlines()
	for eachline in lines:
		pattern = re.compile(r'.*\s(.+),\s<urlopen error \[Errno 111\] Connection refused>')
		match = pattern.findall(eachline)
		if match:
			for eachmatch in match:
				output= output+eachmatch+"\n"
				
with open("/home/user/yalih/connectionrefused.txt", "a") as appendforbidden:
	appendforbidden.write(output)
print output
