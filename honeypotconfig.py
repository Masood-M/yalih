#!/usr/bin/python2.7
import sys
import os
import string
from os.path import basename


wdir="/opt/yalih/" #set your working directory - should start and end with "/" without quotations
useragent="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)" #Internet explorer identifies itself as Mozilla/4.0 - MSIE 7.0 is Internet Explorer Version and Windows NT 5.1 is Windows XP
acceptlang="en-us,en;q=0.5"
referrer="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source="
# Referrer Google Search "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source="


#    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6",
#    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 Firefox/3.0.6",
#    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)",
#    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6",
#    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6",
#    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)",
#    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19",
#    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)",
#    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6",
#    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121621 Ubuntu/8.04 (hardy) Firefox/3.0.5",
#    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1",
#    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
#    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
#    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"



#====Bing Search
starturl=20


username="email username"
password="email password"
server="mail server"
#server="imap.gmail.com"


mode=""

#====Temporary folder name (inside honeypot folder)
tmpfolder="tmp/" #followed by / sign

#====Number of Threads
#====Worker threads = threadnum - 2
threadnum=10

#====JSBeautifier
jsbeautifier = False

#====Add proxies in this format
#===={"protocol" : "address:port"} {"http" : "60.220.212.12:80"}
proxy={}

#====The maximum size for executables that would be downloaded, in kb
exe_max_size = 1800

#====HoneypotMonitor, in sec
checkfrequency = 100
staticScanMaxTime = 100

