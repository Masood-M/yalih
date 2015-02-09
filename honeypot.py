#! /usr/bin/env python

import time
import threading
import os, sys, Queue
from time import gmtime, strftime
from itertools import groupby
from operator import itemgetter
import os.path
import imapfile
import logging
import honeypotconfig
import scan
import bing
import executemechanize
import malwebsites
import normalize
import updateantivirus
import yaradetection
import unquote
import argparse

try:
	import signal
	from signal import SIGPIPE, SIG_IGN
	signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
	pass

#global lastWebsite
#lastWebsite = ""
queue=Queue.Queue()
logger = logging.getLogger()
doneFileLock = threading.Lock()

def worker():
	global lastWebsite
	print "Last Website is: "+lastWebsite
	urldict = queue.get()	
	logger.info(str(urldict["counter"]) + ",\t" + urldict["url"] + ",\t" + "Visiting")
	executemechanize.executemechanize(urldict)
	queue.task_done()
	doneFileLock.acquire()
	myfile = open(honeypotconfig.wdir+"done.txt","w")
	print "Last website:"+str(lastWebsite)+" Last website scanned:"+str(urldict["url"])
	if str(lastWebsite) == str(urldict["url"]):
		myfile.write("Scan")
	else:
		myfile.write(urldict["url"])
	myfile.close()
	doneFileLock.release()

def threadmaker():	
	while True:		
		threadstomake = honeypotconfig.threadnum - threading.active_count()
		
		for i in range(threadstomake):
			thread = threading.Thread(target=worker)
			thread.setDaemon(True)
		 	thread.start()

		time.sleep(5)


def readurl():
	url = sys.argv[2]
	return url


def main():
	#Variable to store the last website in the job list
	global lastWebsite
	lastWebsite = ""
#Create the threads
	thread = threading.Thread(target=threadmaker)
	thread.setDaemon(True)
	thread.start()

	parser = argparse.ArgumentParser(description="Examples:\n/honeypot.py --url www.yahoo.com\nhoneypot.py --file <file path>\n./honeypot.py --blacklist\n./honeypot.py --email\n./honeypot.py --update\n./honeypot.py --search <warez>\n./honeypot.py --local <file/directory path>", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("--email", help="Retrieves your Spam emails from your mail server and crawls the extracted URLS. Enter your email credentials in honeypotconfig.py file!", action="store_true")
	parser.add_argument("--update", help="Updates the anti-virus signatures", action="store_true")
	parser.add_argument("--blacklist", help="Downloads list of suspicious malicious websites from three databases and retrieves/scans them accordingly", action="store_true")
	parser.add_argument("--file", nargs=1, help="Provide an input file", action="store")
	parser.add_argument("--url", nargs=1, help="Provide a url", action="store")
	parser.add_argument("--search", nargs=1, help="searches Bing search engine for a keyword (1 single keyword at the moment) and returns 100 results starting from the 20th result.", action="store")
	parser.add_argument("--local", nargs=1, help="scans a local file or directory for malicious signatures.", action="store")
	parser.add_argument("--debug", help="Include http header", action="store_true")
	parser.add_argument("--crawler", help="Crawl the sites and save any executables found", action="store_true")

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)
	args = parser.parse_args()
	path = honeypotconfig.wdir + honeypotconfig.tmpfolder

	#Check if 'done.txt' exists, create file if it doesn't
	if not os.path.exists(honeypotconfig.wdir+'done.txt'):
		open(honeypotconfig.wdir+'done.txt','w').close()
	#try:
	#	open(honeypotconfig.wdir+'done.txt')
	#except:
	#	open(honeypotconfig.wdir+'done.txt','w').close()
	
	#Check what URL Yalih crashed at
	f = open(honeypotconfig.wdir+'done.txt')
	lastDone = f.readline()
	#If 'done.txt' says 'Done' or 'Starting' or 'Blank', reset the last URL scanned
	if(str(lastDone)=="Done" or str(lastDone)=="Starting" or str(lastDone)==""):
		open(honeypotconfig.wdir+'done.txt','w').write("Starting")
		lastDone = ""
		print str(lastDone)

#create the tmp folder
	if not os.path.isdir(os.path.join(honeypotconfig.wdir, honeypotconfig.tmpfolder)):
		os.makedirs(os.path.join(honeypotconfig.wdir, honeypotconfig.tmpfolder))           
		
#Crawler
	if args.crawler:
		executemechanize.exe_crawler = True
		
#Logging
	"""Initialize logger."""
	command = "mkdir -p "+honeypotconfig.wdir+"debug/" #create a temporary folder in your working space folder
	os.system(command)
	sys.stdin=open(honeypotconfig.wdir+"debug/" +  time.asctime(time.localtime(time.time())) +".log", "a")
	logger = logging.getLogger()
	
	sh = logging.StreamHandler()
	sh.setFormatter(SpecialFormatter())

	sh2 = logging.StreamHandler(sys.stdin)
	sh2.setFormatter(SpecialFormatter())
	
	logger.addHandler(sh)
	logger.addHandler(sh2)
	logger.setLevel(logging.INFO)
	
	if args.debug:
		logger.setLevel(logging.DEBUG)
		executemechanize.set_logging_level(logging.DEBUG)

#Update antivirus signatures
	if args.update:
		updateantivirus.updateantivirus()

#Blacklist Databases
	if args.blacklist:
		try:
			if not os.path.exists(os.path.join(honeypotconfig.wdir, "list")):
				os.mkdir(os.path.join(honeypotconfig.wdir, "list"))
		except OSError as e:	
			logger.error(e)	
		malwebsites.domaindownload()
		malwebsites.duplicateremover()
		urls = open(honeypotconfig.wdir+"list/malwebsites.txt", "r")
		#Convert URLs to standard format, store as a new list.
		urlsList = []
		for line in urls:
			if not (line.startswith("http://")) and not (line.startswith("https://")):
				line = "http://"+line
			if line.endswith("\r\n"):
				line = line[:-2]
			urlsList.append(line)
		#Stores the last website from the user input file
		#global lastWebsite
		lastWebsite = urlsList[-1]
		#Check if the last scanned website is in the user input file, starts from the next URL after the last scanned.
		if lastDone in urlsList:
			index = urlsList.index(lastDone) + 1
			counter = 0
			for line in urlsList[index:]:
				dict={}
				counter += 1
				dict["url"] = line.strip()
				dict["counter"] = counter
				queue.put(dict)
			queue.join()
		#Last scanned website is not in the current user input file, start from the first url.
		else:
			counter = 0
			for line in urls:
				dict={}
				counter += 1
				dict["url"] = line.strip()
				dict["counter"] = counter
				queue.put(dict)
			queue.join()
		
		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)

		myfile = open(honeypotconfig.wdir+"done.txt","w")
		myfile.write("Done")
		myfile.close()

#Email
	if args.email:
		imapfile.imap()
		extractlink.extracturl()#extracts urls from emails.txt file 
		extractlink.duplicateremover() #removes the duplicate urls from crawler.txt files (which now contain extracted urls from emails.txt)
		urlsListOld = open('crawler.txt', "r")
		#Convert URLs to standard format, store as a new list.
		urlsList = []
		for line in urlsListOld:
			if not (line.startswith("http://")) and not (line.startswith("https://")):
				line = "http://"+line
			if line.endswith("\r\n"):
				line = line[:-2]
			urlsList.append(line)
		#Stores the last website from the user input file
		#global lastWebsite
		lastWebsite = urlsList[-1]
		#Check if the last scanned website is in the user input file, starts from the next URL after the last scanned.
		if lastDone in urlsList:
			index = urlsList.index(lastDone) + 1
			counter = 0
			for line in urlsList[index:]:
				dict={}
				counter += 1
				dict["url"] = line
				dict["counter"] = counter
				queue.put(dict)
			queue.join()
		#Last scanned website is not in the current user input file, start from the first url.
		else:
			counter = 0
			for line in urlsList:
				dict={}
				counter += 1
				dict["url"] = line
				dict["counter"] = counter
				queue.put(dict)
			queue.join()
		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)
		myfile = open(honeypotconfig.wdir+"done.txt","w")
		myfile.write("Done")
		myfile.close()

#File
	if args.file:
		mylist = list()
		mylist2 = list()
		counter =0
		fopen3 = open(sys.argv[2],"r")	
		#List containing URLs from the user input file
		inputListOld = fopen3.readlines()
		#Convert URLs to standard format, store as a new list.
		inputList = []
		for line in inputListOld:
			if not (line.startswith("http://")) and not (line.startswith("https://")):
				line = "http://"+line
			if line.endswith("\r\n"):
				line = line[:-2]
			inputList.append(line)
		#Stores the last website from the user input file
		#global lastWebsite
		lastWebsite = inputList[-1]				
		#Check if the last scanned website is in the user input file, starts from the next URL after the last scanned.
		if lastDone in inputList:
			index = inputList.index(lastDone) + 1
			for line in inputList[index:]:
				dict={}
				line = line.strip()
				counter += 1
				if not (line.startswith("http://")) and not (line.startswith("https://")):
					line = "http://"+line
				dict["url"] = line
				dict["counter"] = counter
				queue.put(dict)
				queue.join()
		#Last scanned website is not in the current user input file, start from the first url.
		else:
			for line in inputList:
				dict={}
				line = line.strip()
				counter += 1
				if not (line.startswith("http://")) and not (line.startswith("https://")):
					line = "http://"+line
				dict["url"] = line
				dict["counter"] = counter
				queue.put(dict)
				queue.join()		
		fopen3.close()
		#scan.scanning(path)
		#yaradetection.listandscan(path)
		#unquote.unquoteDirectory(path)
		myfile = open(honeypotconfig.wdir+"done.txt","w")
		myfile.write("Done")
		myfile.close()

#URL
	if args.url:
		url = readurl()
		url = normalize.normalizeurl(url)
		dict={}
		counter = 1
		if not (url.startswith("http://")) and not (url.startswith("https://")):
			url = "http://"+url
		#global lastWebsite
		lastWebsite = url
		dict["url"] = url
		dict["counter"] = counter
		queue.put(dict)
		queue.join()		
#		executemechanize.executemechanize(url)
		#scan.scanning(path)
		#yaradetection.listandscan(path)
		#unquote.unquoteDirectory(path)
		myfile = open(honeypotconfig.wdir+"done.txt","w")
		myfile.write("Done")
		myfile.close()


#Search
	if args.search:
		keyword = sys.argv[2]
		bing.searchBing(keyword)
		mylist = list()
		fopen = open("list/searchresult.txt","r")
		for line in fopen:
			line = line.strip()
			if not line:
				continue
			mylist.append(line)
		fopen.close()

		#Convert URLs to standard format, store as a new list.
		inputList = []
		for line in mylist:
			if not (line.startswith("http://")) and not (line.startswith("https://")):
				line = "http://"+line
			if line.endswith("\r\n"):
				line = line[:-2]
			inputList.append(line)

		inputList = inputList[:5]
		#Stores the last website from the user input file
		#global lastWebsite
		lastWebsite = inputList[-1]

		myfile = open(honeypotconfig.wdir+"crash.txt","a")
		myfile.write(str(inputList)+"\n\n")
		myfile.close()

		#Check if the last scanned website is in the user input file, starts from the next URL after the last scanned.
		if lastDone in inputList:
			index = inputList.index(lastDone) + 1
			counter = 0
			for line in inputList[index:]:
				dict={}
				counter += 1
				dict["url"] = line
				dict["counter"] = counter
				queue.put(dict)
			queue.join()
		#Last scanned website is not in the current user input file, start from the first url.
		else:
			counter = 0
			for line in inputList:
				dict={}
				counter += 1
				dict["url"] = line
				dict["counter"] = counter
				queue.put(dict)
			queue.join()
		#scan.scanning(path)
		#yaradetection.listandscan(path)
		#unquote.unquoteDirectory(path)
		myfile = open(honeypotconfig.wdir+"done.txt","w")
		myfile.write("Done")
		myfile.close()

#Local Scan
	if args.local:
		myfile = open(honeypotconfig.wdir+"done.txt","w")
		myfile.write("Scan")
		myfile.close()
		path = sys.argv[2]
		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)
		myfile = open(honeypotconfig.wdir+"done.txt","w")
		myfile.write("Done")
		myfile.close()

class SpecialFormatter(logging.Formatter):

	FORMATS = {logging.ERROR : "%(asctime)s,\t%(name)s,\t%(levelname)s,\t%(error_code)s,\t%(message)s",
			   'DEFAULT' :  "%(asctime)s,\t%(name)s,\t%(levelname)s,\t,\t%(message)s"}
			   
	def formatTime(self, record, datefmt=None):
		self._datefmt = time.strftime("%Y-%m-%d %H:%M:%S")
		return logging.Formatter.formatTime(self, record, self._datefmt)

	def format(self, record):
		self._fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
		return logging.Formatter.format(self, record)



if __name__ == "__main__":
	main()