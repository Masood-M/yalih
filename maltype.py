import string
import re

class Maltype:
 
    files = []  # Store all the file names that are of the same maltype
    rule = ""   # Store the rule
    maltype_num = 0
 
    def __init__(self, f, num):
        self.files = []
        self.files.append(f);
        self.maltype_num = num;
 
    def remove_file(self, f):
        self.files.remove(f);

    def add_file(self, f):
        self.files.append(f);
 
    def get_maltype_num(self):
        return self.maltype_num
 
    def get_files(self):
        return self.files
 
    def set_rule(self, rule):
        self.rule = rule
 
    def get_rule(self):
        return self.rule
 
    def count_rule_string(self, rule):
        return len(re.findall("\$string", str(rule)))
