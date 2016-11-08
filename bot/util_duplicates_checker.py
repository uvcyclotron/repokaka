# util_duplicates_checker
# utility for checking code duplicates
# using PyGithub
# for CRA-BOT

from github import Github
import subprocess


'''
method parameters:
	x		is

returns ..

description..

'''
def util_duplicates_checker(currentDirectory):
	p=subprocess.Popen("/home/ubuntu/pmd/pmd-bin-5.4.1/bin/run.sh cpd --minimum-tokens 10 --files " + currentDirectory , shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output=p.communicate()[0]
	temp = output.strip()
	if not temp:
		return "No Duplicates Found" 
	else:
		return "Found these duplicates:\n-----------------------\n" + str(output)

