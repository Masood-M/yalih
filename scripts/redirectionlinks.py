import os
import re
import sys

# Extracts and appends redirection links to links.txt
#"/home/user/yalih/debug"
#+"/home/user/yalih/links.txt"
folderPath = str(sys.argv([1]))
outputFolder = str(sys.argv([2]))
directoryFiles = os.listdir(folderPath)
for filePath in directoryFiles:
    file = open(folderPath+"/"+filePath, 'r')
    #print file.read()
    match = re.search(r'Redirection Route,\t\[(.+)\]', file.read())
    if match:
	print match.group(1)
	with open(outputFolder, "a") as appendlinks:
        	appendlinks.write(match.group(1)+"\n")
