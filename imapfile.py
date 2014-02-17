#! /usr/bin/env python

import imaplib
import os, re, email
from pprint import pprint
import base64
import honeypotconfig


def open_connection():
    connection = imaplib.IMAP4_SSL(honeypotconfig.server)
    connection.login(honeypotconfig.username, honeypotconfig.password)
    return connection

def imap():
	c = open_connection()

	list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

	def parse_list_response(line):
	    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
	    mailbox_name = mailbox_name.strip('"')
	    return (mailbox_name)
	email_file = open("emails.txt", "w")
	folderlist=list()
	try:
		typ, data = c.list()
		print "available folders are:\n"
		for line in data:
			mailbox_name = parse_list_response(line)
			print mailbox_name
			folderlist.append(str(mailbox_name))

		typ, data = c.select('INBOX', readonly=True)
		num_msgs = int(data[0])+1
		print 'There are %d messages in INBOX' % num_msgs

		for i in range(1,num_msgs):
			print "Retrieving Email "+ str(i)
			typ, msg_data = c.fetch(i, '(RFC822)')
			msg_data=msg_data[0][1]
			msgbody = email.message_from_string(msg_data)
			for part in msgbody.walk():
				if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
					email_file.write(part.get_payload(decode=True)+"\n")
				elif part.get_content_maintype() == 'text/plain' or part.get_content_maintype() == 'text/html':
					email_file.write(part.get_payload(decode=True)+"\n")
				elif part.get_content_subtype() == 'text/plain' or part.get_content_subtype() == 'text/html':
					email_file.write(part.get_payload(decode=True)+"\n")
				elif part.__getitem__('Content-Transfer-Encoding') == "quoted-printable":
					email_file.write(part.get_payload(decode=True)+"\n")
				elif part.__getitem__('charset')== 'utf-8' and part.__getitem__('Content-Transfer-Encoding') == 'base64':
					email_file.write(part.get_payload(decode=True)+"\n")
				else:
					pass
			email_file.write("==================================================\n")
			email_file.write("==================================================\n")
			i=i+1

		typ, data2 = c.list()
		i=1
		for name in folderlist:
			if ('spam' in name.lower()):
				typ, data2 = c.select(name, readonly=True)
				num_msgs = int(data2[0])+1
				print 'Spam folder exists and there are %d messages in it.' % num_msgs
				for i in range(1,num_msgs):
					print "Retrieving Spam Email "+ str(i)
					typ, msg_data = c.fetch(i, '(RFC822)')
					msg_data=msg_data[0][1]
					msgbody = email.message_from_string(msg_data)
					for part in msgbody.walk():
						if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
							email_file.write(part.get_payload(decode=True)+"\n")
						elif part.get_content_maintype() == 'text/plain' or part.get_content_maintype() == 'text/html':
							email_file.write(part.get_payload(decode=True)+"\n")
						elif part.get_content_subtype() == 'text/plain' or part.get_content_subtype() == 'text/html':
							email_file.write(part.get_payload(decode=True)+"\n")
						elif part.__getitem__('Content-Transfer-Encoding') == "quoted-printable":
							email_file.write(part.get_payload(decode=True)+"\n")
						elif part.__getitem__('charset')== 'utf-8' and part.__getitem__('Content-Transfer-Encoding') == 'base64':
							email_file.write(part.get_payload(decode=True)+"\n")
						else:
							pass
					email_file.write("==================================================\n")
					email_file.write("==================================================\n")
					i=i+1
			else:
				pass

	finally:
		email_file.close()
		c.logout()
