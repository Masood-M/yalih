import psutil,sys,honeypotconfig,threading,smtplib,subprocess,shlex,time
import signal,os

def sendEmail(SUBJECT,MESSAGE):
	FROMADDR = "yalihstatus@outlook.com"
	LOGIN    = FROMADDR
	PASSWORD = "!QWER4321"
	TOADDRS  = ["yalihstatus@outlook.com"]
	msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
	       % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
	msg += MESSAGE + "\r\n"
	print "Preparing to send status email"
	server = smtplib.SMTP('smtp-mail.outlook.com', 587)
	#server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.login(LOGIN, PASSWORD)
	server.sendmail(FROMADDR, TOADDRS, msg)
	server.quit()
	print "Finished sending"

#Function that repeats to monitor honeypot.py
def checkMonitor():
	#Crash log file
	myfile = open(honeypotconfig.wdir+"crash.txt","a")
	#Process ID of honeypot.py
	global processID
	global process
	global noOfScanTimes
	#Check status of honeypot.py (Status: "Done","Starting",URL)
	doneFile = open(honeypotconfig.wdir+'done.txt','r')
	status = doneFile.readline()
	doneFile.close()
	print "Check monitor status: "+str(status)
	#Starting -> Waiting for the first url in queue to be completed
	if str(status) == "Starting":
		threading.Timer(honeypotconfig.checkfrequency,checkMonitor).start()
		myfile.write("Waiting for first url to be done\n")
		print "Waiting for first url to be done"
	#Scan -> Finished downloading all files, performing static analysis now
	elif str(status) == "Scan":
		noOfScanTimes = noOfScanTimes + 1
		if noOfScanTimes*honeypotconfig.checkfrequency > honeypotconfig.staticScanMaxTime:
			#Psutil used to check for network connections and if the process is still running or not
			p = psutil.Process(processID)
			if p.is_running():
				print "Restarting honeypot.py, Yalih honeypot static scan max time reached"
				myfile.write("Restarting honeypot.py, Yalih honeypot static scan max time reached\n")
				process.kill()
				process = subprocess.Popen(['python',honeypotconfig.wdir+'honeypot.py','--local',honeypotconfig.wdir+honeypotconfig.tmpfolder])
				processID = int(process.pid)
				sendEmail("Yalih Status Update","Yalih honeypot static scan max time reached. Restarted Yalih honeypot.")
				checkMonitor()
		else:
			threading.Timer(honeypotconfig.checkfrequency,checkMonitor).start()

	#Done -> All url's in queue has been compeleted
	elif str(status) == "Done":
		print "Completed scanning, terminating honeypotMonitor"
		myfile.write("Completed scanning, terminating honeypotMonitor\n")
		sendEmail("Yalih Status Update","Yalih honeypot has completed scanning.")
	#URL -> The last url that has been scanned, queue not finished yet
	else:
		#Repeat checkMonitor func since job has not been completed
		threading.Timer(honeypotconfig.checkfrequency,checkMonitor).start()
		#Psutil used to check for network connections and if the process is still running or not
		p = psutil.Process(processID)
		#Honeypot.py process is still running
		if p.is_running():
			print p.connections()
			#No network connections being made, restart honeypot.py
			if str(p.connections()) == "[]":
				print "Restarting honeypot.py, Yalih honeypot has stop making network connections"
				myfile.write("Restarting honeypot.py, Yalih honeypot has stop making network connections\n")
				process.kill()
				process = subprocess.Popen(['python',honeypotconfig.wdir+'honeypot.py']+sys.argv[1:])
				processID = int(process.pid)
				sendEmail("Yalih Status Update","Yalih honeypot has stop making network connections. Restarted Yalih honeypot.")
				checkMonitor()
			else:
				print str("Last scanned file: "+status)
				myfile.write("Last scanned file: "+status+"\n")
		#Honeypot.py process not running, restart
		else:
			process = subprocess.Popen(['python',honeypotconfig.wdir+'honeypot.py']+sys.argv[1:])
			processID = int(process.pid)
			print "Restarted Yalih Honeypot.py (PID:"+str(processID)+"), Yalih honeypot has crashed"
			myfile.write("Restarted Yalih Honeypot.py (PID:"+str(processID)+"), Yalih honeypot has crashed"+"\n")
			sendEmail("Yalih Status Update","Yalih honeypot has crashed, restarted Yalih honeypot (PID:"+str(processID)+").")
		myfile.close()

global noOfScanTimes
noOfScanTimes = 0
global process
process = subprocess.Popen(['python',honeypotconfig.wdir+'honeypot.py']+sys.argv[1:])
#stdout,stderr = process.communicate()
#print stderr
#print stdout
global processID
processID = int(process.pid)
p = psutil.Process(processID)
time.sleep(10)
print "Starting up HoneypotMonitor on Honeypot.py (PID:"+str(process.pid)+")"
checkMonitor()
