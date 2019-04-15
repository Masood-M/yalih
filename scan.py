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
		print "\n=============== ClamAV Antivirus Engine is running! Please Wait ===============" 
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