#! /usr/bin/env python


import subprocess
import sys, threading, Queue
import os

def updateantivirus():
	command="echo ======================= Updating Antivirus Signatures ========================"
	os.system(command)

	command3="freshclam"
	os.system(command3)

