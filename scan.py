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
	
#Codes for avgscan
	os.chdir(path)
		
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



	os.chdir(path)
	print "Avast is running!"
	command14="echo ============================================================ > "+honeypotconfig.wdir+"scanlogs/"+"Avast-report.log"
	command15="echo ========================AVAST Antivirus===================== >> "+honeypotconfig.wdir+"scanlogs/"+"Avast-report.log"
	os.system(command14)
	os.system(command15)
	start_timeavast = time.time()
	command13="avast -a -r "+honeypotconfig.wdir+"scanlogs/"+"Avast-report.log"
	os.system(command13)
	finish_time=time.time()-start_timeavast, "seconds"
	fileopen=open(honeypotconfig.wdir+"scanlogs/Avast-report.log", "a")
	fileopen.write("\nScanning time with Avast Antivirus engines was: "+str(finish_time))
	fileopen.close

'''
