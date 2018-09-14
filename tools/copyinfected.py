#! /usr/bin/env python

import subprocess
import sys, threading, Queue
import os
import string
import urlparse
import os.path
import honeypotconfig
import re, time

def copyinfected():
	logfile=open(honeypotconfig.wdir+"scanlogs/"+"report.log","r")
	foundfileslog=open(honeypotconfig.wdir+"found/"+"FoundExploits.log","w")
#	foundfileslog.write("The following files were detected to be malicious:\n\n")
	for line in logfile:
		if line.startswith("/"):
			results=line.strip()
			if "\t" in results:
				results=results.replace("\t"," ")

			if "  " in results:
				results=results.replace("  "," ")

			p1=results.find(".html") #find the lowest index of ".html", finds the index of (.)
#			print p
			if (p1 != -1):
				filename1=results[0:p1+5]# to cover .html
				foundfileslog.write(filename1+"\n")
				copycommand1='cp -R --backup "'+ filename1+ '" ' +honeypotconfig.wdir+'found/'
#				print copycommand1
				os.system(copycommand1)

			p2=results.find(".js")
			if (p2 != -1):
				filename2=results[0:p2+3]# to cover .js
				foundfileslog.write(filename2+"\n")
				copycommand2='cp -R --backup "'+ filename2+ '" ' +honeypotconfig.wdir+'found/'
#				print copycommand2
				os.system(copycommand2)
	mylist=list()
	foundfileslog.close()
	fopen=open(honeypotconfig.wdir+"found/"+"FoundExploits.log","r")
	for line in fopen:
		line=line.strip()
		if line in mylist:
			continue
		else:
			mylist.append(line)
	mylist.sort()
	fopen.close()
	fopen=open(honeypotconfig.wdir+"found/"+"FoundExploits.log","w")
	fopen.write("The following files were detected to be malicious:\n\n")
	for line in mylist:
		fopen.write(line+"\n")

#	fopen.close()
#	fopen=open(honeypotconfig.wdir+"found/"+"FoundExploits.log","w")
#	for line in mylist:
#		fopen.write(line+"\n")
#	fopen.close()



#			filename2=line[0:p2+5]			
#			j=results.index(".html")
#			results2=results[:j]
#
#			if results2.endswith(":"):
#				results2=results2[:-1]
#			print "Copying the infected file to: "+filename1
#			foundfileslog.write(filename1+"\n")
#			copycommand1="cp -R --remove-destination "+filename1+" "+honeypotconfig.wdir+"found/"
#			os.system(copycommand1)
#			print "Copying the infected file to: "+filename2
#			foundfileslog.write(filename2+"\n")
#			copycommand2="cp --remove-destination "+filename2+" "+honeypotconfig.wdir+"found/"
#			os.system(copycommand2)


