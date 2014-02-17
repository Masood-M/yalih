#! /usr/bin/env python


import subprocess
import sys, threading, Queue
import os

def updateantivirus():
	command="echo ======================= Updating Antivirus Signatures ========================"
	os.system(command)

	command1="service avgd start" 
	os.system(command1)
	command2="avgupdate"
	os.system(command2)

	command3="freshclam"
	os.system(command3)
'''
	command4="avast-update"
	os.system(command4)

'''
