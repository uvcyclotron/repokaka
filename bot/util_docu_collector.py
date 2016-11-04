# util_docu_collector
# utility for collecting code documentation
# using PyGithub
# for CRA-BOT

import json
from pprint import pprint
from subprocess import Popen
from subprocess import call
from github import Github
import subprocess

'''
method parameters:
	x		is

returns ..

description..

'''
def util_docu_collector():
	return """

DOCUMENTATION
------------------
@Class_M :
/** ....
*	....
*	....
*/

@method_A :
// ....
// ....
// ....

@method_B :
// ....
// ....
// ....
"""

def generate_documentation():


	# Doxygen script
	subprocess.call(["doxygen", "-g", "config-file"])
	subprocess.call("perl -pi -w -e 's/EXTRACT_ALL            = NO/EXTRACT_ALL            = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/GENERATE_MAN           = NO/GENERATE_MAN           = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/EXTRACT_PRIVATE        = NO/EXTRACT_PRIVATE        = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/EXTRACT_STATIC         = NO/EXTRACT_STATIC         = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/GENERATE_HTML          = YES/GENERATE_HTML          = NO/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/GENERATE_LATEX         = YES/GENERATE_LATEX         = NO/g;' config-file", shell=True)
	subprocess.call(["doxygen", "config-file"])

	# Concatenate all the man pages of the patches
	#subprocess.call("cd man/man3", shell=True)
	subprocess.call("cat *.3 >> document.3", shell=True, cwd = "./man/man3")

	# Convert the man pages to txt
	subprocess.call("groff -t -e -mandoc -Tascii document.3 | col -bx > manpage.txt", shell=True, cwd = "./man/man3")

	# Strip off unneccesary details

	# Read the txt file and post it as a comment. 

	#print ls_output

def get_patches():

    # get PR json
    #pr_json = open(r"sample", "r")
    # parsejs = pickle.load(pr_json)
    # print parsejs

    # list of dictionaries
    with open('sample.json') as pr_json:
        data = json.load(pr_json)

    #print(data)
    # iterate through the list and for each element save the patch value with name as the filename
    for a in data:
    	s = str(a['filename'])
    	index = s.rfind('/')
    	index = index + 1
    	file = open(s[index:], "w")
    	file.write(str(a['patch']))
    	file.close()
    	#print(str(a['filename']) +"\n"+ str(a['patch']))
    
    #repouri = data['head']['repo']['clone_url']
    #reponame = data['head']['repo']['name']

def main():
	# Get the patches
	get_patches()

	# Generate documentation
	generate_documentation()


if __name__=="__main__":
	main()
