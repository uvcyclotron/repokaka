# coverage_helper
# for CRA-BOT 

from github import Github
import json
from pprint import pprint
from subprocess import call

'''
method parameters:
	x		is 
returns ..
description..	
'''
def coverage_helper():

	# get PR json
	pr_json = open(r"pull_txt", "r")
	# parsejs = pickle.load(pr_json)
	# print parsejs

	with open('pull_txt') as pr_json:
		data = json.load(pr_json)

	# pprint(data['head']['repo']['git_url'])
	repouri = data['head']['repo']['clone_url']
	reponame = data['head']['repo']['name']
	print repouri


	cmdlist = list()
	cmdlist.append("mkdir temp")
	cmdlist.append("cd temp")
	# cmdlist.append("git clone " + repouri)
	# cmdlist.append("cd " + reponame)

	print cmdlist

	# for cmd in cmdlist:
		# call(cmd.split())
