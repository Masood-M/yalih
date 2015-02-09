import os
import re
import sys

# Extracts and appends forbidden links to forbidden.txt
# Input Example: python extractforbidden.py /home/user/Desktop/france-1.log
folderPath = str(sys.argv[1])
output = ""
with open(folderPath) as f:
	lines = f.readlines()
	for eachline in lines:
		pattern = re.compile(r'.+,\sERROR,\s403,\s\d{5},\s(.+),\sHTTP Error 403: Forbidden\n')
		match = pattern.findall(eachline)
		if match:
			for eachmatch in match:
				output= output+eachmatch+"\n"
		else:
			pattern2 = re.compile(r'ERROR,\s403,\s*\d\d\d\d\d,\s(.+),\s.+,\s(.+)')
			match2 = pattern2.findall(eachline)
			if match2:
				for eachmatch2 in match2:
					string = '\t\tComponent: '.join(eachmatch2)
					output= output+string+"\n"
with open("/home/user/yalih/forbidden.txt", "a") as appendforbidden:
	appendforbidden.write(output)
print output
