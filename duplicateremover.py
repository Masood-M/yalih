#! /usr/bin/env python


import subprocess
import sys, threading, Queue
import os
import string
from time import gmtime, strftime


def normalizeurl(url): ## this function normalizes the urls obtained from emails.txt files and writes them to crawler.txt.
	url = url.strip()
	if (url.endswith("/")):
		url=url[:-1]
		pass
	elif (url.endswith(".")):
		url=url[:-1]
		pass
	elif url.find('javascript:void(0)')!= -1:
		url="invalid"
	elif url.find('#')!= -1:
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
	return url



mylist=list()
file1=raw_input("File name containing URLs to read: ")
file2=raw_input("File name to write to: ")
fopen2=open(file1,"r")
for line in fopen2:
	line=line.strip()
	line=normalizeurl(line)
	if line=="invalid":
		continue
	elif not line:
		continue
	elif line in mylist:
		continue
	elif line =="-":
		continue
	elif not (line.startswith("http://")) and not (line.startswith("https://")):
		line="http://"+line
		pass
#		print line
	mylist.append(line)
fopen2.close()
fopen3=open(file2,"w")
for line in mylist:
	fopen3.write(line+"\n")
fopen3.close()


