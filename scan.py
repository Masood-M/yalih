#! /usr/bin/env python

import subprocess
import sys, threading, Queue
import os
import string
import urlparse
import os.path
import honeypotconfig
import re, time, datetime



def scanning(path):
	os.chdir(path)
		
	start_time = time.time()
	with open(honeypotconfig.wdir + "scanlogs/Clam-report.log", "w") as f:
		print "\n================ ClamAV Antivirus Engine is running! Please Wait ===============" 
		f.write("======================================ClamAV======================================\n\n")
		f.write(datetime.datetime.now().strftime("%A, %d %B %Y %I:%M:%S%p") + "\n\n")
		f.write("--------------------------------------------------------------------------------------------------------------------\n\n")
		process = subprocess.Popen("clamscan -r --stdout --infected --scan-html=yes --scan-pdf=yes --scan-archive=yes --algorithmic-detection=yes" , shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline, ''):
			sys.stdout.write(line)
			f.write(line)
		f.write("\nclamscan -r --stdout --infected --scan-html=yes --scan-pdf=yes --scan-archive=yes -i --algorithmic-detection=yes " + os.getcwd() + "\n\n")
		finish_time = time.time() - start_time, "seconds"
		f.write("Scanning time with ClamAV engine was: " + str(finish_time) + "\n\n")
		print "================================================================================"	
	

		
#codes for comodo

	os.chdir(path)		
	start_time = time.time()
	with open(honeypotconfig.wdir + "scanlogs/Comodo-report.log", "w") as f:
		print "\n================ COMODO Antivirus Engine is running! Please Wait ===============" 
		f.write("======================================Comodo======================================\n\n")
		f.write(datetime.datetime.now().strftime("%A, %d %B %Y %I:%M:%S%p") + "\n\n")
		f.write("--------------------------------------------------------------------------------------------------------------------\n\n")
		COMODOcommand="sudo /opt/COMODO/cmdscan ARCHIVE LOGLEVEL=2 -v -s "+path#+" > "+honeypotconfig.wdir + "scanlogs/tmpCOMODO.log "
		process = subprocess.Popen(COMODOcommand , shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline, ''):
			if line.find('Found Virus, ') != -1:
				sys.stdout.write(line)
				f.write(line)
			else:
				continue;
#		infected=""grep "Found Virus, "+honeypotconfig.wdir + "scanlogs/tmpCOMODO.log"+" > "+honeypotconfig.wdir + "scanlogs/COMODO.log""
		f.write("\nsudo /opt/COMODO/cmdscan ARCHIVE LOGLEVEL=2 -v -s "+path+" > "+honeypotconfig.wdir + "scanlogs/Comodo-report.log "+"\n\n")
		finish_time = time.time() - start_time, "seconds"
		f.write("Scanning time with COMODO engine was: " + str(finish_time) + "\n\n")
		print "================================================================================"	




#Codes for avgscan
'''	start_time = time.time()
	with open(honeypotconfig.wdir + "scanlogs/AVG-report.log", "w") as f:
		print "\n================ AVG Antivirus Engine is running! Please Wait ================" 
		f.write("======================================AVG Antivirus======================================\n\n")
		f.write(datetime.datetime.now().strftime("%A, %d %B %Y %I:%M:%S%p") + "\n\n")
		f.write("--------------------------------------------------------------------------------------------------------------------\n\n")
		path=os.path.abspath(path)
		path=path.replace(" ","\ ")
		process = subprocess.Popen("avgscan --ignerrors -r " + honeypotconfig.wdir + "scanlogs/tmpavg.log " + path , shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline, ''):
			sys.stdout.write(line)
		with open(honeypotconfig.wdir + "scanlogs/tmpavg.log") as a:
			f.write(a.read())
			os.remove(honeypotconfig.wdir + "scanlogs/tmpavg.log")
		f.write("\navgscan --ignerrors " + path + "\n\n")
		finish_time = time.time() - start_time, "seconds"
		f.write("Scanning time with AVG engine was: " + str(finish_time) + "\n\n")
		print "==============================================================================="
