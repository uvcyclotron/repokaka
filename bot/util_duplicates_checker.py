# util_duplicates_checker
# utility for checking code duplicates
# using PyGithub
# for CRA-BOT

from github import Github
import subprocess


'''
method parameters: currentFile is the file to be scanned for duplicates.

returns duplicate code if any. 

description: pmd is ran over the currentFile to scan for duplicates.

'''
def util_duplicates_checker(currentFile):
    # Calling pmd with customized configuration on the currentFile.
	p=subprocess.Popen("/home/ubuntu/pmd/pmd-bin-5.4.1/bin/run.sh cpd --minimum-tokens 10 --files " + currentFile , shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output=p.communicate()[0]
	temp = output.strip()
	# Returing the duplicates found if any. 
	if not temp:
		return "\nNo duplicates found for file: " + currentFile + "\n" 
	else:
		return "\nFound these duplicates for file: " + currentFile + "\n" + str(output)+"\n"

