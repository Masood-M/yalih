import honeypotconfig

infected_files = dict()


def unquoteDirectory(path):

	# Open the AVG log
	with open(honeypotconfig.wdir + "scanlogs/AVG-report.log") as f:
		for line in f:
			# Store the directory path as the key for infected_files
			if line.startswith(honeypotconfig.wdir):
				infected_files[line.split(" ")[0]] = " AVG"

	# Open the Clam-AV log
	with open(honeypotconfig.wdir + "scanlogs/Clam-report.log") as f:
		for line in f:
			if line.strip().endswith("FOUND"):
				line = line.split(":")[0]

				# Check if the the directory path(key) exists
				# If key exists, append value "Clam-AV" 
				# If it doesn't, create the key
				if line in infected_files:
					# If Clam-AV already exists for that key, go to the next iteration of loop
					if infected_files[line].endswith("Clam-AV"):
						continue
					infected_files[line] = infected_files[line] + ", Clam-AV"
				else:
					infected_files[line] = " Clam-AV"


	# Open the YARA log
	with open(honeypotconfig.wdir + "scanlogs/Yara-report.log") as f:
		start = False
		for line in f:
			# The start of yara rule
			if "------------" in line:
				start = True
				continue
			# The end of yara rule
			elif line.startswith("yara -r"):
				start = False
			if start:
				if line.strip():
					line = line.split(" ")[1].strip()
					# Check if the the directory path(key) exists
					# If key exists, append value "YARA" 
					# If it doesn't, create the key					
					if line in infected_files:
						# If YARA already exists for that key, go to the next iteration of loop
						if infected_files[line].endswith("YARA"):
							continue
						infected_files[line] = infected_files[line] + ", YARA"
					else:
						infected_files[line] = " YARA"

	infected_urls = dict()

	for k, v in infected_files.iteritems():

		# Check if "http" string not in folder name
		# If "http" not in folder name, use parent directory as "website"
		# Else use folder with first occurrence of "http"
		if k.rfind("/") < k.find("http") or k.find("http") == -1:
					website = k[:k.rfind("/")]
		else:
			website = k[k.find("http"):].split("/")[0]

		# Place files(Value) under respective folder(Key)
		# If folder(Key) exist, append
		# Else create
		if website in infected_urls:
			infected_urls[website] = infected_urls[website] + "\n\t" + k + v
		else:
			infected_urls[website] = "\n\t" + k + v


	# Write to file, replacing %3A%2F%2F with ://
	with open(honeypotconfig.wdir + "scanlogs/Malicious-Websites.log", "w") as f:
		f.write("Infected directories: " + str(len(infected_urls)) + "\n")
		for k, v in infected_urls.iteritems():
			f.write("\n\n" + k.replace("%3A%2F%2F" , "://"))
			f.write(v)

