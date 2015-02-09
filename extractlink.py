#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
import unicodedata
import subprocess
import sys, threading, Queue
import os
import string
from time import gmtime, strftime
import urllib2
import urllib
import re, time
import honeypotconfig 
from HTMLParser import HTMLParseError
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import optparse
from itertools import groupby
from operator import itemgetter
import honeypotconfig
import urlparse
import os.path
import honeypot
#import extract
import sys, logging
#from google import search
import mechanize
import executemechanize
from BeautifulSoup import BeautifulSoup
import normalize


def extracturl():
	emailurlextract=open('crawler.txt', 'w')
	emailfile=open('emails.txt','r')
	soup = BeautifulSoup(emailfile.read())
	for tag in soup.findAll('a', href=True):
		link=tag['href']
		emailurlextract.write(normalizeurl(link)+'\n')

	sp1=re.findall(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', str(soup))

	for i in sp1:
		emailurlextract.write(normalizeurl(i)+"\n")

	emailfile.close()
	emailurlextract.close()


def duplicateremover():
	mylist=list()
	fopen=open("crawler.txt","r")
	for line in fopen:
		line=line.strip()
		line=normalize.normalizeurl(line)
		if line in mylist:
			continue
		if line=="invalid":
			continue
		if not line:
	        	continue
		mylist.append(line)
	mylist.sort()
	fopen.close()
	fopen=open("crawler.txt","w")
	for line in mylist:
		fopen.write(line+"\n")	


#def main():
#
#	extracturl()#extracts urls from emails.txt file 
##	visiturl()
#if __name__ == "__main__":
#    main()
