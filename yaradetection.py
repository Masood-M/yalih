#! /usr/bin/env python


import subprocess
import sys
import os, datetime, time
import string
import honeypotconfig 
import honeypotconfig

#compile the rules



def listandscan(path):
	start_timeYara = time.time()

	with open(honeypotconfig.wdir + "scanlogs/Yara-report.log", "w") as f:
		print "\n===================================== Yara =====================================" 
		f.write("======================================Yara======================================\n\n")
		f.write(datetime.datetime.now().strftime("%A, %d %B %Y %I:%M:%S%p") + "\n\n")
		f.write("--------------------------------------------------------------------------------\n\n")
		os.system("find . -type f -size 0k -exec rm {} \; | awk '{ print $8 }'")
		process = subprocess.Popen("yara -r " + honeypotconfig.wdir + "yrules/rules.yara " + path[:-1], shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline, ''):
			sys.stdout.write(line)
			f.write(line)
		f.write("\nyara -r " + honeypotconfig.wdir + "yrules/rules.yara " + path[:-1] + "\n\n")
		finish_time = time.time() - start_timeYara, "seconds"
		f.write("Scanning time with Yara engine was: " + str(finish_time) + "\n\n")
		print "================================================================================"

'''
def yaradetect(inputfile):
	ruleinput='Value'
	fin = open(honeypotconfig.wdir+"yrules/rules.yara", 'r')
	if fin:
		ruleinput = fin.read()
		fin.close()
	rules = yara.compile(source=ruleinput)
	f = open(inputfile, 'r')
	matches = rules.match(data=f.read())
	for m in matches:
		print "%s" % m+ " found in file: " +inputfile
		yarareport=reportfile.write(inputfile+"\t\t"+"%s" % m+"\n")

'''