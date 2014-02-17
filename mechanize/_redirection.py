import os,sys
parentdir = os.path.dirname(__file__)
sys.path.insert(0,parentdir)
import executemechanize

class redirection:

	def createarray(self):
		setattr(self, "redirection_list", [])

	def appendurl(self, url):
		url = str(url)
		if not url.endswith(".js") or url.endswith(".json"):
			self.redirection_list.append(url);
			self.passarray()

	def passarray(self):
		executemechanize.set_redirection_list(self.redirection_list)
