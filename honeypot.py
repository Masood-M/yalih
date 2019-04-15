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
import extraction

try:
	import signal
	from signal import SIGPIPE, SIG_IGN
	signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
	pass


queue=Queue.Queue()
logger = logging.getLogger()

def worker():

	urldict = queue.get()	
#this is for the normal visitor output (no error)
	logger.info(str(urldict["counter"]) + ",\t" + urldict["url"]+",\t"+ "Visiting")
	executemechanize.executemechanize(urldict)
	queue.task_done()
	

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
	path = honeypotconfig.tmpfolder


#create the tmp folder
	if not os.path.isdir(os.path.join(honeypotconfig.tmpfolder)):
		os.makedirs("tmp")           

		
#Crawler
	if args.crawler:
		executemechanize.crawler = True
		
#Logging
	"""Initialize logger."""
	command = "mkdir -p debug/" #create a temporary folder in your working space folder
	os.system(command)
	sys.stdin=open(debug/" +  time.asctime(time.localtime(time.time())) +".log", "a")
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
			if not os.path.exists("list"):
				os.mkdir("list")
		except OSError as e:	
			logger.error(e)	
		malwebsites.domaindownload()
		malwebsites.duplicateremover()
		urls = open("list/malwebsites.txt", "r")
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


#Email
	if args.email:
		imapfile.imap()
		extraction.extracturl()#extracts urls from emails.txt file 
		extraction.duplicateremover() #removes the duplicate urls from crawler.txt files (which now contain extracted urls from emails.txt)
		os.remove("emails.txt")		
		urls = open('crawler.txt', "r")
		counter = 0
		for line in urls:
			dict={}
			counter += 1
			dict["url"] = line.rstrip()
			dict["counter"] = counter
			queue.put(dict)
		queue.join()
		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)

#File

	if args.file:
		mylist = list()
		mylist2 = list()
		counter =0
		fopen3 = open(sys.argv[2],"r")	
		for line in fopen3:
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
		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)



#URL
	if args.url:
		url = readurl()
		url = normalize.normalizeurl(url)
		dict={}
		counter = 1
		if not (url.startswith("http://")) and not (url.startswith("https://")):
			url = "http://"+url
		dict["url"] = url
		dict["counter"] = counter
		queue.put(dict)
		queue.join()
#		executemechanize.executemechanize(url)
		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)


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
		counter = 0
		for line in mylist:
			dict={}
			counter += 1
			dict["url"] = line
			dict["counter"] = counter
			queue.put(dict)
		queue.join()

		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)



#Local Scan
	if args.local:
		path = sys.argv[2]
		scan.scanning(path)
		yaradetection.listandscan(path)
		unquote.unquoteDirectory(path)



class SpecialFormatter(logging.Formatter):
	FORMATS = {logging.INFO : "%(name)s,\t%(levelname)s,\t%(message)s", 'DEFAULT' :  "%(name)s,\t%(levelname)s,\t%(message)s"}	   
	def formatTime(self, record, datefmt=None):
		self._datefmt = time.strftime("%Y-%m-%d %H:%M:%S")
		return logging.Formatter.formatTime(self, record, self._datefmt)

	def format(self, record):
		self._fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
		return logging.Formatter.format(self, record)



if __name__ == "__main__":
	main()
