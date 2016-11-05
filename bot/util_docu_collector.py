# util_docu_collector
# utility for collecting code documentation
# using PyGithub
# for CRA-BOT

import json
import string
from pprint import pprint
from subprocess import Popen
from subprocess import call
from github import Github
import subprocess

patched_files = []

'''
method parameters:
	x		is

returns ..

description..

'''
def util_docu_collector(data):
	subprocess.call("mkdir temp_docu_generator", shell=True)

	# Get the patches
	get_patches(data)

	# Generate documentation
	documentation = generate_documentation()
	return documentation

def generate_documentation():

	# Doxygen script
	subprocess.call("doxygen -g config-file", shell=True, cwd = "./temp_docu_generator")
	subprocess.call("perl -pi -w -e 's/EXTRACT_ALL            = NO/EXTRACT_ALL            = YES/g;' config-file", shell=True, cwd = "./temp_docu_generator")
	subprocess.call("perl -pi -w -e 's/GENERATE_MAN           = NO/GENERATE_MAN           = YES/g;' config-file", shell=True, cwd = "./temp_docu_generator")
	subprocess.call("perl -pi -w -e 's/EXTRACT_PRIVATE        = NO/EXTRACT_PRIVATE        = YES/g;' config-file", shell=True, cwd = "./temp_docu_generator")
	subprocess.call("perl -pi -w -e 's/EXTRACT_STATIC         = NO/EXTRACT_STATIC         = YES/g;' config-file", shell=True, cwd = "./temp_docu_generator")
	subprocess.call("perl -pi -w -e 's/GENERATE_HTML          = YES/GENERATE_HTML          = NO/g;' config-file", shell=True, cwd = "./temp_docu_generator")
	subprocess.call("perl -pi -w -e 's/GENERATE_LATEX         = YES/GENERATE_LATEX         = NO/g;' config-file", shell=True, cwd = "./temp_docu_generator")
	subprocess.call("doxygen config-file", shell=True, cwd = "./temp_docu_generator")

	# Concatenate all the man pages of the patches
	for a in patched_files:
		subprocess.call("cat "+ a +" >> document.3", shell=True, cwd = ".temp_docu_generator/man/man3")
	

	# Convert the man pages to txt
	subprocess.call("groff -t -e -mandoc -Tascii document.3 | col -bx > manpage.txt", shell=True, cwd = ".temp_docu_generator/man/man3")

	subprocess.call("perl -pi -w -e 's/Generated automatically by Doxygen for My Project from the source code./Generated by CRABOT./g;' manpage.txt", shell=True, cwd = ".temp_docu_generator/man/man3")

	# Read the txt file and post it as a comment. 
	with open('temp_docu_generator/man/man3/manpage.txt', 'r') as content_file:
		documentation = content_file.read()

	subprocess.call("rm -rf temp_docu_generator", shell=True)

	return documentation

def format_result(fname, result):
	added_code=""
	removed_code=""

	result_list=result.split('\n')
	for item in result_list:
		if str(item).startswith('+'):
			added_code+=str(item)[1:]+"\n"
		elif str(item).startswith('-'):
			removed_code+=str(item)[1:]+"\n"
	result_list = added_code.split('\n')
	for item in result_list:
		if str(item).startswith('package '):
			temp1 = fname + ".3"
			patched_files.remove(temp1)
			temp = str(item)[8:-1]
			temp = string.replace(temp, '.', '_')
			temp = temp + "_" + str(fname)
			temp = string.replace(temp, ".java", ".3")
			patched_files.append(temp)


	return added_code

def get_patches(data):

    # get PR json
    #pr_json = open(r"sample", "r")
    # parsejs = pickle.load(pr_json)
    # print parsejs



    # list of dictionaries
    #with open('sample.json') as pr_json:
    #    data = json.load(pr_json)

    data = json.loads(data)
    #print(data)
    # iterate through the list and for each element save the patch value with name as the filename
    for a in data:
    	s = str(a['filename'])
    	index = s.rfind('/')
    	index = index + 1
    	file = open("/temp_docu_generator/"+s[index:], "w")
    	temp = s[index:]+".3"
    	patched_files.append(temp)
    	result = format_result(s[index:],str(a['patch']))
    	#file.write(str(a['patch']))
    	file.write(result)
    	file.close()
    	#print(str(a['filename']) +"\n"+ str(a['patch']))
    
'''
def main():
	# Get the patches
	get_patches()

	# Generate documentation
	generate_documentation()


if __name__=="__main__":
	main()
'''
