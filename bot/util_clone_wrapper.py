# git clone wrapper
# utility for getting src code from git, and calling utils
# using PyGithub
# for CRA-BOT

from github import Github
import json
from pprint import pprint
from subprocess import call
from lxml import html
import requests
import os.path 

from coverage_calc.coverage_helper import coverage_helper
from util_duplicates_checker import util_duplicates_checker

PR_COMMENT="issue_comment"
COMMIT_COMMENT="commit_comment"
COMMENT_ON_PR="pull"
PR="pull_request"
TMP_DIR_NAME = 'tmp_clone'



def util_clone_wrapper(dict_payload, request_type, coverageFlag, duplicateFlag):
	if(request_type == COMMENT_ON_PR or request_type==COMMIT_COMMENT or request_type==PR):
		pr_url = str(dict_payload['issue']['pull_request']['url'])

		pull_json_text =  requests.get(pr_url)
		data = json.loads(pull_json_text.content)

		repouri = data['head']['repo']['clone_url']
		reponame = data['head']['repo']['name']

		try:
			call('mkdir '+TMP_DIR_NAME, shell=True)							# make temp dir
			call("git clone " + repouri, shell=True, cwd='./'+TMP_DIR_NAME) 	# clone repo in temp

			cmdlist = list()
			cmdlist.append("git checkout mvn")				#TODO remove later
			for cmd in cmdlist:
				call(cmd, shell=True, cwd='./' + TMP_DIR_NAME + '/'+reponame) 		# run util on 

			############################
			# NOW WE HAVE CODE CLONED INTO TMP_DIR_NAME FOLDER
			# WE CAN RUN REQUESTED ANALYSIS NOW
			# CALL MODULES, and GET RESULTS
			############################
			results = ""
			if (coverageFlag):
				results += coverage_helper(TMP_DIR_NAME, reponame)

			if (duplicateFlag):
				results += util_duplicates_checker('./' + TMP_DIR_NAME + '/'+reponame)

			return results



		except (RuntimeError, TypeError, NameError) as ex:
			print 'exception occurred'
			print ex

		finally:
			print 'deleting temp dir'
			call('rm -rf ' + TMP_DIR_NAME, shell=True)							# remove temp	

