#! /usr/bin/env python

import argparse
import datetime
import os, sys, errno
import honeypotconfig
import shutil
import subprocess
from maltype import Maltype
from YaraGenerator import yaraGenerator
 
 
min_file_req = 2      # Minimum number of files that match with each other in order to be considered as a rule
min_string_req = 3    # Minimum number of Strings in a rule for the rule to be considered


def create_directory(directory_name):
	try:
		os.makedirs(directory_name)
	except OSError as exc:
		if exc.errno == errno.EEXIST:
			pass
		else:	
			raise


def classify():
	
	with open(honeypotconfig.wdir + "scanlogs/RulesGenerator_Yara.log", "a") as f:
		print "Clam Antivirus Engine is running! Please Wait." 
		f.write("=======================ClamAV Antivirus====================\n")
		f.write(datetime.datetime.now().strftime("%A, %d %B %Y %I:%M:%S%p") + "\n\n")
		f.write("--------------------------------------------------------------------------------------------------------------------\n\n")
		process = subprocess.Popen("clamscan -r --stdout --infected --scan-html=yes --scan-pdf=yes --scan-archive=yes --algorithmic-detection=yes", shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline, ''):
			sys.stdout.write(line)
			f.write(line)
		f.write("\nclamscan -r --stdout --infected --scan-html=yes --scan-pdf=yes --scan-archive=yes --algorithmic-detection=yes" + " " + os.getcwd() + "\n\n")
	
	with open(honeypotconfig.wdir + "scanlogs/RulesGenerator_Yara.log" , 'r') as f:
		create_directory(honeypotconfig.wdir + "ClamAV")
		
		for line in f.readlines():
			if "FOUND" in line:
				splitter = line.split(":")
				filename = splitter[0]
				virus = splitter[1].split(" ")[1]		
				create_directory(honeypotconfig.wdir + "ClamAV/" + virus)
				shutil.copy2(filename, honeypotconfig.wdir + "ClamAV/" + virus)
				

	
def iter_islast(iterable):
	it = iter(iterable)
	prev = it.next()
	for item in it:
		yield prev, False
		prev = item
	yield prev, True

 
def write_rules(maltype_list, rule_path):
	rulefile = open(rule_path, "a")
	print("")
	for maltype in maltype_list:
		if len(maltype.get_files()) >= min_file_req:
			print("\tWriting: "+maltype.get_rule().split('\n', 1)[0])
			rulefile.write(maltype.get_rule())
			rulefile.write("\n")

 
def generate_rules(file_path, rule_path):

	# Enter folder only if there is more than 1 file
	if len(os.walk(os.path.join(os.getcwd(), file_path)).next()[2]) > 1: 
		maltype_list = [] # Array of maltypes
		maltypenum = 0
 
		print("\n\nEntering: " + file_path)
 
		for f in os.listdir(file_path):
			
			f = os.path.join(os.getcwd(), file_path, f)
			
			print("\tParsing: " + f);
	
			# For first file to create a maltype
			if not maltype_list:
				tmpmaltype = Maltype(f, maltypenum)
				maltype_list.append(tmpmaltype)
				maltypenum += 1
				continue
			
			# File goes through all maltypes in the maltype_list
			# Breaks out of loop when it matches a maltype
			# File and new rule gets inserted into the maltype
			for maltype, islast in iter_islast(maltype_list):
				
				# Generate yara rule name
				# Remove illegal characters
				# Add maltype number behide
				rulename = os.path.basename(os.path.normpath(file_path)).replace(".","_").replace("-","_") + "_Maltype_" +str(maltype.get_maltype_num())
				
				# Adds current file to the maltype
				# Generate rule from all files in the maltype with yaragenerator
				maltype.add_file(f)
				rule = yaraGenerator.main(rulename, maltype.get_files())

				# Set rule in maltype to new rule if there are enough Strings in it
				# Else remove the current file from the maltype
				if maltype.count_rule_string(rule) >= min_string_req:
					maltype.set_rule(rule)
					break
				elif islast:
				# If the file doesn't match any of the other maltype
				# Create a maltype and add the file in
					maltype.remove_file(f);
					tmpmaltype = Maltype(f, maltypenum)
					maltype_list.append(tmpmaltype)
					maltypenum += 1
				else:
					maltype.remove_file(f);
	 
		write_rules(maltype_list, rule_path)
 

def main():
	parser = argparse.ArgumentParser(description="Examples:\n./rulesgenerator.py --generaterules /opt/yalih-honeypot/ClamAV\n./rulesgenerator.py --classify /home/infected/", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("--generaterules", nargs=1, help="Path To Files To Create Yara Rule From")
	parser.add_argument("--classify", nargs=1, help="Use ClamAV to sort the malicious files into their malware type, results found in honeypotconfig.wdir/ClamAV")
	args = parser.parse_args()
	
	
	os.chdir(os.path.join(honeypotconfig.wdir, sys.argv[2]))


	if args.classify:
		classify()

	if args.generaterules:
		#get directory_list from parserions.InputDirectory. Subdirectories
		directory_list = [name for name in os.listdir(".") if os.path.isdir(name)]
		
		if not directory_list:
			open("../rules.yar", "w").close()
			generate_rules(sys.argv[2], "../rules.yar")
		else:
			open("rules.yar", "w").close()
			for directory in directory_list:
				generate_rules(directory, "rules.yar");
 
 
if __name__ == "__main__":  
	main()
