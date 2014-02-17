#! /usr/bin/env python


import subprocess
import sys, threading, Queue
import os
import string
from time import gmtime, strftime
import urllib2
import urllib
import re, time
import urlparse
import os.path
#import extract
import logging
#from google import search
import honeypotconfig
import copyinfected
import scan
import executemechanize
import extractlink
import mechanize
from BeautifulSoup import BeautifulSoup


def domaindownload():# this function downloads domain and website links from multible blacklisted website databases.
	if os.path.isfile(honeypotconfig.wdir+"list/list1.txt")==True:
		print "Malicious website database from https://spyeyetracker.abuse.ch exists!\n"
		print "Continuing with the next list."
	else:
		print "Fetching list from: https://spyeyetracker.abuse.ch"
		command1="wget https://spyeyetracker.abuse.ch/blocklist.php?download=domainblocklist -O "+honeypotconfig.wdir+"list/list1.txt"
		os.system(command1)
#--proxy-user=username --proxy-password=password

	if os.path.isfile(honeypotconfig.wdir+"list/list2.txt")==True:
		print "Malicious website database from https://zeustracker.abuse.ch/ exists!\n"
		print "Continuing with the next list."
	else:
		print "Fetching list from: https://zeustracker.abuse.ch/"
		command2="wget https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist -O "+honeypotconfig.wdir+"list/list2.txt"
		os.system(command2)

	if os.path.isfile(honeypotconfig.wdir+"list/list3.txt")==True:
		print "Malicious website database 3 exists!\n"
	else:
		print "Fetching list 3"
#		command3="wget http://www.montanamenagerie.org/hostsfile/hosts.txt -O "+honeypotconfig.wdir+"list/list3.txt"
		command3="wget http://hosts-file.net/hphosts-partial.asp -O "+honeypotconfig.wdir+"list/list3.txt"
		os.system(command3)



	mainfile=open(honeypotconfig.wdir+"list/malwebsites.txt", 'w')
	file1=open(honeypotconfig.wdir+"list/list1.txt", 'r')
	mainfile.write(file1.read())
	file2=open(honeypotconfig.wdir+"list/list2.txt", 'r')
	mainfile.write(file2.read())
	file3=open(honeypotconfig.wdir+"list/list3.txt", 'r')
	mainfile.write(file3.read())
	mainfile.close()
	file1.close()
	file2.close()
	file3.close()

#def normalizeurl(url): ## this function normalizes the urls obtained from emails.txt files and writes them to crawler.txt.
#	url = url.strip()
#	if (url.endswith("/")):
#		url=url[:-1]
#		pass
#	elif (url.endswith(".")):
#		url=url[:-1]
#		pass
#	elif url.find('javascript:void(0)')!= -1:
#		url="invalid"
#	elif url.find('#')!= -1:
#		url="invalid"
#	elif url.startswith("/"):
#		url="invalid"
#	elif url.startswith("//"):
#		url="invalid"
#	elif url.startswith("./"):
#		url="invalid"
#	elif url.startswith("..//"):
#		url="invalid"
#	if url.startswith("127.0.0.1"):
#		url=url[10:]
#		pass
#	return url

def duplicateremover():
	mylist=list()
	fopen2=open(honeypotconfig.wdir+"list/malwebsites.txt","r")
	for line in fopen2:
		line=line.strip()
		if line.startswith("127.0.0.1"):
			line=line[10:]
			pass
		if line.startswith("#"):
			continue
		if line.find('#') == 1:
			continue
#		if line=="invalid":
#			continue
		if not line:
			continue
		if line in mylist:
			continue
		if not (line.startswith("http://")) and not (line.startswith("https://")):
			line="http://"+line
			pass
#		print line
		mylist.append(line)
	fopen2.close()
	fopen3=open(honeypotconfig.wdir+"list/malwebsites.txt","w")
	for line in mylist:
		fopen3.write(line+"\n")
	fopen3.close()
	print "List of Malicious websites were downloaded from three databases."
