import honeypotconfig

infected_files = dict()



with open(honeypotconfig.wdir + "scanlogs/AVG-report.log") as f:
	for line in f:
		if line.startswith(honeypotconfig.wdir):
			infected_files[line.split(" ")[0]] = " AVG"

with open(honeypotconfig.wdir + "scanlogs/Clam-report.log") as f:
	for line in f:
		if line.strip().endswith("FOUND"):
			line = line.split(":")[0]
			if line in infected_files:
				if infected_files[line].endswith("Clam-AV"):
					continue
				infected_files[line] = infected_files[line] + ",Clam-AV"
			else:
				infected_files[line] = " Clam-AV"


with open(honeypotconfig.wdir + "scanlogs/Yara-report.log") as f:
	start = False
	for line in f:
		if "------------" in line:
			start = True
			continue
		elif line.startswith("yara -r"):
			start = False
		if start:
			if line.strip():
				line = line.split(" ")[1].strip()
				if line in infected_files:
					if infected_files[line].endswith("YARA"):
						continue
					infected_files[line] = infected_files[line] + ",YARA"
				else:
					infected_files[line] = " YARA"

infected_urls = dict()

for k, v in infected_files.iteritems():
	website = k[k.find("http"):].split("/")[0]
	if website in infected_urls:
		infected_urls[website] = infected_urls[website] + "\n\t" + k + v
	else:
		infected_urls[website] = "\n\t" + k + v

with open(honeypotconfig.wdir + "scanlogs/Malicious-Websites.log", "w") as f:
	f.write("Infected sites: " + str(len(infected_urls)) + "\n")
	for k, v in infected_urls.iteritems():
		print "\n\n" + k.replace("%3A%2F%2F" , "://")
		print v
		f.write("\n\n" + k.replace("%3A%2F%2F" , "://"))
		f.write(v)
