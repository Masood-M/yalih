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
from HTMLParser import HTMLParseError
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import optparse
from itertools import groupby
from operator import itemgetter
import os.path
import sys, logging
import mechanize
import executemechanize
from BeautifulSoup import BeautifulSoup
import normalize
import lxml.html

def exe_extraction(url_list):
	exe_list = []
	exe_regex = re.compile("\.(exe|msi|scr|zip)$")
	for link in url_list:
		if exe_regex.search(link.strip()):
			exe_list.append(link)
	return exe_list


def js_extraction(response, scheme, host):

# JS extraction approach 1
	jsurl_list_old = []	# Array of link to js as is in html file
	jsurl_list = list()	# Array of link to js after getting fully qualified domain name

	url_list = re.findall(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', response)
	js_regex = re.compile("\.js(\?)?.*$")

	for link in url_list:
		link = link.strip()
		if js_regex.search(link) and link not in jsurl_list:
			jsurl_list_old.append(link)
			link = link.replace("amp;", "") # remove amp; from urls
			link = re.split("['\"]", link)[0] # remove unnecessary quotes from url
			jsurl_list.append(link)


# JS extraction approach 2
	doc = lxml.html.document_fromstring(response)
	script_list = doc.xpath('//script/@src')

	for link in script_list:
		if not js_regex.search(link):
			continue

		elif link.startswith("//"):
			jsurl_list_old.append(link)
			link = scheme + ":" + link
			jsurl_list.append(link)

		elif link.startswith("/"):
			jsurl_list_old.append(link)
			link = scheme + "://" + host + link
			jsurl_list.append(link)

		elif link.startswith("www."):
			jsurl_list_old.append(link)
			link = "http://" + link
			jsurl_list.append(link)

		elif link.lower().startswith(("js/", "catalog/", "script/", "scripts/", "katalog/","template/","templates/","includes/","static/","mod/","files/","data/","css/","components/","component/","sites/","default/")):
			jsurl_list_old.append(link)
			link = scheme + "://" + host + "/" + link
			jsurl_list.append(link)

		elif link.startswith("./") or link.startswith("../"):
			jsurl_list_old.append(link)
			link = re.sub(r"^[\./|\.\./]", "", link)
			link = scheme + "://" + host + link
			jsurl_list.append(link)

			jsurl_list.append(link)

#		elif not link.lower().startswith(("//","/","www.","http://","https://","./","../")):
#			jsurl_list_old.append(link)
#			link = scheme + "://" + host + "/" + link
#			jsurl_list.append(link)

		else:
			jsurl_list_old.append(link)
			jsurl_list.append(link)
			
	del doc
	del script_list 
	return jsurl_list_old, jsurl_list, url_list




def extracturl():
	emailurlextract=open('crawler.txt', 'w')
	emailfile=open('emails.txt','r')
	soup = BeautifulSoup(emailfile.read())
	for tag in soup.findAll('a', href=True):
		link=tag['href']
		emailurlextract.write(normalize.normalizeurl(link.strip())+'\n')

	sp1=re.findall(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', str(soup))

	for i in sp1:
		emailurlextract.write(normalize.normalizeurl(i)+"\n")

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
