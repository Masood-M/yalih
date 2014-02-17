#! /usr/bin/env python


# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import honeypotconfig
from BeautifulSoup import BeautifulSoup

def searchBing(keyword):
	queryBingFor = "'%s'" %keyword #"'google fibre'" # the apostrophe's required as that is the format the API Url expects. 
	quoted_query = urllib.quote(queryBingFor)
	account_key = "Unolx7kLAlLp1NSwmPyis9df+ecjQeN9pqGe57sW/D8="
	rootURL = "https://api.datamarket.azure.com/Bing/Search/"
	searchURL = rootURL + "Web?$format=json&Query=" +quoted_query+ "&$top=50&$skip="+str(honeypotconfig.starturl)
	username="masood.mansoori@live.com"
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, searchURL,username,account_key)

	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

#	authhandler = urllib2.HTTPDigestAuthHandler(password_mgr)
#	opener = urllib2.build_opener(authhandler)

	urllib2.install_opener(opener)
	readURL = urllib2.urlopen(searchURL).read()
	response_data = readURL
	json_result = json.loads(response_data)
	result_list = json_result['d']['results']
	searchresult=open("list/searchresult.txt", "w")
	for i in result_list:
		print i['Url']
		searchresult.write(i['Url']+"\n")
	searchresult.close()


	nextsearch=honeypotconfig.starturl+50

	queryBingFor = "'%s'" %keyword #"'google fibre'" # the apostrophe's required as that is the format the API Url expects. 
	quoted_query = urllib.quote(queryBingFor)
	account_key = "Unolx7kLAlLp1NSwmPyis9df+ecjQeN9pqGe57sW/D8="
	rootURL = "https://api.datamarket.azure.com/Bing/Search/"
	searchURL = rootURL + "Web?$format=json&Query=" +quoted_query+ "&$top=50&$skip="+str(nextsearch)
	username="masood.mansoori@live.com"
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, searchURL,username,account_key)

	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

#	authhandler = urllib2.HTTPDigestAuthHandler(password_mgr)
#	opener = urllib2.build_opener(authhandler)

	urllib2.install_opener(opener)
	readURL = urllib2.urlopen(searchURL).read()
	response_data = readURL
	json_result = json.loads(response_data)
	result_list = json_result['d']['results']
	searchresult=open("list/searchresult.txt", "a")
	for i in result_list:
		print i['Url']
		searchresult.write(i['Url']+"\n")
	searchresult.close()

	nextsearch=honeypotconfig.starturl+100

	queryBingFor = "'%s'" %keyword #"'google fibre'" # the apostrophe's required as that is the format the API Url expects. 
	quoted_query = urllib.quote(queryBingFor)
	account_key = "Unolx7kLAlLp1NSwmPyis9df+ecjQeN9pqGe57sW/D8="
	rootURL = "https://api.datamarket.azure.com/Bing/Search/"
	searchURL = rootURL + "Web?$format=json&Query=" +quoted_query+ "&$top=50&$skip="+str(nextsearch)
	username="masood.mansoori@live.com"
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, searchURL,username,account_key)

	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

#	authhandler = urllib2.HTTPDigestAuthHandler(password_mgr)
#	opener = urllib2.build_opener(authhandler)

	urllib2.install_opener(opener)
	readURL = urllib2.urlopen(searchURL).read()
	response_data = readURL
	json_result = json.loads(response_data)
	result_list = json_result['d']['results']
	searchresult=open("list/searchresult.txt", "a")
	for i in result_list:
		print i['Url']
		searchresult.write(i['Url']+"\n")
	searchresult.close()
		


	nextsearch=honeypotconfig.starturl+150

	queryBingFor = "'%s'" %keyword #"'google fibre'" # the apostrophe's required as that is the format the API Url expects. 
	quoted_query = urllib.quote(queryBingFor)
	account_key = "Unolx7kLAlLp1NSwmPyis9df+ecjQeN9pqGe57sW/D8="
	rootURL = "https://api.datamarket.azure.com/Bing/Search/"
	searchURL = rootURL + "Web?$format=json&Query=" +quoted_query+ "&$top=50&$skip="+str(nextsearch)
	username="masood.mansoori@live.com"
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, searchURL,username,account_key)

	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

#	authhandler = urllib2.HTTPDigestAuthHandler(password_mgr)
#	opener = urllib2.build_opener(authhandler)

	urllib2.install_opener(opener)
	readURL = urllib2.urlopen(searchURL).read()
	response_data = readURL
	json_result = json.loads(response_data)
	result_list = json_result['d']['results']
	searchresult=open("list/searchresult.txt", "a")
	for i in result_list:
		print i['Url']
		searchresult.write(i['Url']+"\n")
	searchresult.close()
