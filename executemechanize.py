#! /usr/bin/env python

import honeypotconfig
import re
import os, errno, logging
import threading, normalize
import mechanize
import cookielib
import urlparse, urllib, urllib2
import lxml.html
import magic, mimetypes
import jsbeautifier
import tldextract, httplib
import extraction

try:
    import signal
    from signal import SIGPIPE, SIG_IGN
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
    pass

logger = logging.getLogger("mechanize")
logger.setLevel(logging.INFO)
threadlocal = threading.local()
crawler = False
opts = jsbeautifier.default_options()
opts.eval_code = True


def set_redirection_list(list):
	threadlocal.__setattr__('redirection_list', list)


def set_logging_level(arg):
	logger.setLevel(arg)


def create_directory(directory_name):
 	try:
		os.makedirs(directory_name)
	except OSError as exc:
		if exc.errno == errno.EEXIST:
			pass
		else:	
			raise

script_path = os.path.dirname(os.path.abspath( __file__ ))

def executemechanize(urldict):
	
	url = urldict["url"]
	url_no = urldict["counter"]

	#Array of redirections
	threadlocal.__setattr__('redirection_list', [])	
	
	# Mechanize Settings
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(False)
	br.set_handle_robots(False)
	br.set_debug_responses(False)
	br.set_debug_redirects(True)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=0)		
	br.set_proxies(honeypotconfig.proxy)
	br.encoding = "UTF-8"
	# Add HTTP Basic/Digest auth username and password for HTTP proxy access.
	# (equivalent to using "joe:password@..." form above)
	#	br.add_proxy_password("username", "password")

	# Set header, referrer, accept language from honeypotconfig
	if honeypotconfig.referrer:
		br.addheaders = [('User-Agent', honeypotconfig.useragent),('Accept', 'text/html,application/xhtml+xml,application/xml,text/javascript;q=0.9,*/*;q=0.8'),('Accept-Language', honeypotconfig.acceptlang),('Accept-Encoding', 'gzip,deflate'),('Referer', honeypotconfig.referrer)]
	else:
		br.addheaders = [('User-Agent', honeypotconfig.useragent),('Accept', 'text/html,application/xhtml+xml,application/xml,text/javascript;q=0.9,*/*;q=0.8'),('Accept-Language', honeypotconfig.acceptlang),('Accept-Encoding', 'gzip,deflate'),('Referer', host)] #'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source='+url)]
	
	cj.add_cookie_header(br)

	try:
		r = br.open(url, timeout=12.0)

		# Parse url (url after redirections)
		scheme, host, path, params, query, fragment = urlparse.urlparse(r.geturl())

		# Print redirection route if exist
		threadlocal.__setattr__('redirect', mechanize._redirection.redirection())

		# Extract and format URL
		extracted = tldextract.extract(url)
#		print extracted
		#formatted = "{}.{}".format(extracted.domain, extracted.suffix)
		formatted = "{}.{}.{}".format(extracted.subdomain, extracted.domain, extracted.suffix)
#		print formatted
		
		# Extract each link in the redirection list and match it aginst the formatted URL
		for eachredirect in threadlocal.redirection_list:
			list_extract = tldextract.extract(eachredirect)
			list_format = "{}.{}.{}".format(list_extract.subdomain, list_extract.domain, list_extract.suffix)
#			print list_format
			if list_format == formatted:
				pass
			if not list_format == formatted:
				if threadlocal.redirection_list:
					logger.info(str(url_no) + ",\t" + url + ",\t" + '"'+"Redirection Route" + '"'+ ",\t" +str(threadlocal.redirection_list))
					break
		
		if threadlocal.redirection_list:
			logger.info(str(url_no) + ",\t" + url + ",\t" + "Redirection Route" + ",\t" +str(threadlocal.redirection_list))
		
		# Convert url into valid file name
		fdirname = urllib.quote_plus(url)
		if (len(fdirname) > 250):
			fdirname = fdirname[:247]
			
# Folder Generation

		# Gets first character of website to store alphabetically
		first_char = re.sub(r"(http://|https://)?(www.)?", "", url)[:1]
		second_char = re.sub(r"(http://|https://)?(www.)?", "", url)[1:3]

		directory_name = os.path.join("tmp/", first_char,  second_char, fdirname)

		# If using proxy, names directory in the format ip_address:port
		if honeypotconfig.proxy:
			proxy_name = re.search(r":\s?['\"](.*)\s?['\"]", str(honeypotconfig.proxy)).group(1)
			directory_name = os.path.join(proxy_name, first_char, second_char, fdirname)
 
 		create_directory(directory_name)

		# Fetch array of javascript url
		jsurl_list_old, jsurl_list, url_list = extraction.js_extraction(br.response().read(), scheme, host)

		# Remove duplicates
		jsurl_list_unique = set(jsurl_list)
		del jsurl_list[:]
		
		# Modify javascript paths in html if relative path
		fp = open(os.path.join(directory_name, fdirname), "wb")
		new_js_path = br.response().read()
		for link in jsurl_list_old:
			if not link.lower().startswith(("www.","http://","https://")):
				js_name=link[link.rfind("/") + 1:]
				new_js_path = re.sub(re.escape(link), "./javascripts/" + js_name, new_js_path)
			
		fp.write(new_js_path)
		fp.close()

		del jsurl_list_old[:]

		# Grab the current extension of the file and check the true extension
		# Rename if differ
		current_ext = os.path.splitext(os.path.join(directory_name, fdirname))[1]
		guess_ext = mimetypes.guess_extension(magic.from_file(os.path.join(directory_name, fdirname), mime=True))
		if (guess_ext is not current_ext and guess_ext is not None):
			os.rename((os.path.join(directory_name, fdirname)), (os.path.join(directory_name, fdirname)) + str(guess_ext))
							
#Fetching .js Files
			
		if len(jsurl_list_unique) != 0:
			create_directory(os.path.join(directory_name,  "javascripts"))
		
				
		for link in jsurl_list_unique:
			link=normalize.normalizeurl2(link)
			if len(link)>250:
				continue
			if link.lower().startswith(("js/", "catalog/", "script/", "scripts/", "katalog/","template/","templates/","includes/","static/","mod/","files/","data/","css/","components/","component/","sites/","default/","./javascripts/")):
				link = scheme + "://" + host + "/" + link
			print "****"+link
			try:			
				r = br.open(normalize.normalizeurl2(link.strip()), timeout=12.0)
				logger.info(str(url_no) + ",\t" + url + ",\tJS retrieve,\t" + link)	
				js_name = link[link.rfind("/") + 1:]
				response = br.response().read()
				print "***"+js_name+"***"

				# If it doesn't end with ".js" eg. "abc.js?key=123" truncate after "?"
				if not js_name.endswith(".js"):
					js_name = js_name[0:js_name.rfind("?")]

				# Writes js file
				js_file_path = os.path.join("tmp/", first_char, second_char, fdirname, "javascripts", js_name)
				if honeypotconfig.proxy:
					proxyname = re.search(r":\s?['\"](.*)\s?['\"]", str(honeypotconfig.proxy)).group(1)
					js_file_path = os.path.join(proxyname, first_char, second_char, fdirname, "javascripts", js_name)
				jswrite = open(js_file_path, 'w')
				jswrite.write(response)

				if honeypotconfig.jsbeautifier:
					jswrite.write("\n====================================================\n")
					jswrite.write("====================Beautified Below================\n")
					with open(js_file_path , 'a') as f:
						beautify_script_string = jsbeautifier.beautify(response, opts)
						f.write(str(beautify_script_string))				
				jswrite.close()

			except Exception, e:
				logger.error(str(url_no) + ",\t" + url.strip() + ",\t" + '"'+ str(e) + '"'+",\t" + link)



			r.close()
				


		jsurl_list_unique.clear()

		# Check for executable files and saves them
		exe_list = []

		if crawler:
			exe_list = extraction.exe_extraction(url_list)

		if len(exe_list) != 0:
			create_directory(os.path.join(directory_name,  "exe"))

		for link in exe_list:
			try:
                    # Read header to check for exe size
                # Only downloads if less than a threshold (set in honeypotconfig)
				r = urllib2.urlopen(link, timeout=12)
				size = int(r.headers["Content-Length"]) / 1024
				exename = link[link.rfind("/") + 1:]
				if size < honeypotconfig.exe_max_size:
					logger.info(str(url_no) + ",\t" + url + ",\t" + "EXE retrieve,\t" + link)
					exe_file_path = os.path.join("tmp/".tmpfolder, first_char, second_char, fdirname, "exe", exename)
					if honeypotconfig.proxy:
						proxyname = re.search(r":\s?['\"](.*)\s?['\"]", str(honeypotconfig.proxy)).group(1)
						exe_file_path = os.path.join(proxyname, first_char, second_char, fdirname, "exe", js_name)
					r.close()
					r2=br.open(link, timeout=12)
					exewrite = open(exe_file_path, 'wb')
					exewrite.write(br.response().read())
					exewrite.close()
				else:
					logger.error(str(url_no) + ",\t" + url + ",\t" + "EXE " + str(size) + "KB above exe_max_size" + ",\t" + link)
			except Exception, e:
				try:
					logger.error(str(url_no) + ",\t" + url.strip() + ",\t" + str(e) + ",\t" + link,  extra = {'error_code' : str(e.code)})
				except AttributeError:
					logger.error(str(url_no) + ",\t" + url.strip() + ",\t" + str(e) + ",\t" + link,  extra = {'error_code' : ""})

		del exe_list[:]
		del url_list[:]



	except Exception, e:   #this is for normal errors (No .js)
		logger.error(str(url_no) + ",\t" + url.strip() + ",\t" + '"'+str(e)+'"' + "\t")	
