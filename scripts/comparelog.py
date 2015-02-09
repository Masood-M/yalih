import os 
import re
import time
import sys

#save similarities or differences to a file
def saveFile(log):
	file = open("similarLogs.txt","w")
	for line in log:
		file.write(line)
		file.write("\n")
	file.close()
	return
	
#Open files and write them to a list
def openFile(Filename):
	f = open(Filename,"r")
	print "Opening log file...:" + Filename
	log = []
	noOfLines = 0
	for line in f:
		#if noOfLines == 10000:
		#	continue
		#else:
		if "root" and "INFO" and "Visiting" in line:
			continue
		elif "mechanize" and "INFO" and "JS retrieve" in line:
			continue
		else:
			line = re.sub('(^\d*-\d*-\d*\s\d*:\d*:\d*,\s\w*,\s\w*,\s,\s)','',line)
			log.append(line)
		#		noOfLines = noOfLines + 1
	print "Log file opened."
	f.close()
	return log

start = time.time()	
directory = os.path.join("/User/JAmes/Downloads","path")
f1=str(sys.argv[0])
f2=str(sys.argv[1])
log1 = []
log2 = []
log1 = openFile(f1)
log2 = openFile(f2)

logSimilar = []

log1difference = 0 
noOfSimilarities = 0
print "Checking for similarities..."
for line in log1:
	if line in log2:
		logSimilar.append(line)
		noOfSimilarities = noOfSimilarities + 1
		print line
saveFile(logSimilar)
end = time.time()
timeTaken = end - start
print "Time elapsed: ", timeTaken