#! /usr/bin/env python


import subprocess
import sys, threading, Queue
import os
import string
from time import gmtime, strftime
import urllib2
import urllib
import re, time
import optparse
from itertools import groupby
from operator import itemgetter
import urlparse
import os.path
#import extract
import imapfile
import sys, logging




def normalizeurl(url): ## this function normalizes the urls obtained from emails.txt files and writes them to crawler.txt.
	url = url.strip()
	if (url.endswith("/")):
		url=url[:-1]
		pass
	elif (url.endswith(".")):
		url=url[:-1]
		pass
	elif url.find('mailto')!= -1:
		url="invalid"
	elif url.find('javascript:void(0)')!= -1:
		url="invalid"
	elif url.find('#')!= -1:
		url="invalid"
	if url.find('.')== -1:
		url="invalid"
	elif url.startswith("/"):
		url="invalid"
	elif url.startswith("//"):
		url="invalid"
	elif url.startswith("./"):
		url="invalid"
	elif url.startswith("..//"):
		url="invalid"
	elif url.startswith("127.0.0.1"):
		url=url[10:]
		pass
	elif not (url.startswith("http://")) and not (url.startswith("https://")): #if url does not start with http:// it adds it
		url="http://"+url
		pass
	return url


def normalizeurl2(url): ## this function normalizes the passed urls.
	url = url.strip()
	if not (url.startswith("http://")) and not (url.startswith("https://")): #if url does not start with http:// it adds it
		url="http://"+url
		pass
	elif url.find('\\')!= -1:
		url=url.replace('\\','')
	return url

