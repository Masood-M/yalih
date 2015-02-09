import smtplib,sys

def sendEmail(SUBJECT,MESSAGE):
	FROMADDR = "yalihstatus@outlook.com"
	LOGIN    = FROMADDR
	PASSWORD = "!QWER4321"
	TOADDRS  = ["yalihstatus@outlook.com"]
	SUBJECT  = "Server Crash Report"

	msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
	       % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
	msg += MESSAGE + "\r\n"

	server = smtplib.SMTP('smtp-mail.outlook.com', 587)
	server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.login(LOGIN, PASSWORD)
	server.sendmail(FROMADDR, TOADDRS, msg)
	server.quit()

sendEmail("Testing Subject","Hi, this is message")