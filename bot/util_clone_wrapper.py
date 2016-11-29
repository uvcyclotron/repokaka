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
from utils_crabot import get_list_changed_files
from utils_crabot import get_PR_repo_details

PR_COMMENT="issue_comment"
COMMIT_COMMENT="commit_comment"
COMMENT_ON_PR="pull"
PR="pull_request"
TMP_DIR_NAME = 'tmp_clone'
relative_filenames_list = []


'''
method parameters: dictionary payload from github comment, type of request, flags indicating whether to run coverage util, and duplicate util
	
returns results as text
description 
	Parses the json to get repo clone url, and repo name
	Downlaods the code from clone url
	Calls utils which have call flag passed as true
	Returns text with overall results
'''
def util_clone_wrapper(dict_payload, request_type, coverageFlag, duplicateFlag):
	list_files=get_list_changed_files(dict_payload,request_type)
	result=extract_result(list_files)

	if result:
		repouri, reponame = get_PR_repo_details(dict_payload, request_type)
		return(call_coverage_duplicate_utils(repouri, reponame, result, coverageFlag, duplicateFlag))		
	else:
		return "\nNo java file found in Pull Request!\n"		


def extract_result(data):
	result = {}
	for item in data:
		relative_filename = item['filename']
		if('.java' in relative_filename):
			if relative_filename not in relative_filenames_list:
				relative_filenames_list.append(relative_filename) 
			#strip relative path of filename
			relative_path = relative_filename.rsplit('/', 1)[0]
			raw_url = item['raw_url']
			result[relative_path] = raw_url
	print "RELATIVE FILE NAME STRING: " + str(relative_filenames_list)
	return result

'''
This method acts as a wrapper for calling the utils which need to operate on the cloned code
Currently, only 2 such modules:
	-- coverage_helper : analyses code to calculate code coverage
	-- util_duplicates_checker : analyses code to find duplcates
Results are returned as a single text
'''
def call_coverage_duplicate_utils(repouri, reponame, result, coverageFlag, duplicateFlag):
	try:
		# we clone code into a tmp directory
		# clean out this directory if it already exists (from previous runs)
		if os.path.exists(TMP_DIR_NAME):
			call('rm -rf ' + TMP_DIR_NAME, shell=True)	

		# create the tmp dir, and clone repo into that
		call('mkdir '+TMP_DIR_NAME, shell=True)							# make temp dir
		call("git clone " + repouri, shell=True, cwd='./'+TMP_DIR_NAME) 	# clone repo in temp

		REPO_PATH = './' + TMP_DIR_NAME + '/'+reponame

		# cmdlist = list()
		# for cmd in cmdlist:
		# 	call(cmd, shell=True, cwd=REPO_PATH) 		# run util on 

		#replace files from result dictionary
		print "===================CHANGED FILES============================="
		print result
		for relative_path, raw_url in result.iteritems():
			#downlaod & replace files
			print "-------------------------------"
			print raw_url
			print "-------------------------------"
			if not os.path.exists(REPO_PATH + '/' + relative_path):
				call('mkdir -p '+REPO_PATH + '/' + relative_path, shell=True)     # make directories if reqd
			call("curl -H 'Accept: application/vnd.github.v3.raw' -O -L " + raw_url, shell = True, cwd = REPO_PATH + '/' + relative_path)

		############################
		# NOW WE HAVE CODE CLONED INTO TMP_DIR_NAME FOLDER
		# WE CAN RUN REQUESTED ANALYSIS NOW
		# CALL MODULES, and GET RESULTS
		############################
		results = {}
		if (coverageFlag):
			results['coverage'] = str(coverage_helper(TMP_DIR_NAME, reponame))

		if (duplicateFlag):
			for filename in relative_filenames_list:
				results['duplicates'] = str(util_duplicates_checker(REPO_PATH + "/" + filename))	
			#results += str(util_duplicates_checker(REPO_PATH))

		if results:			
			return results
		else:
			return None

	except (RuntimeError, TypeError, NameError) as ex:
		print 'exception occurred'
		print ex

	finally:
		print 'deleting temp dir'
		# call('rm -rf ' + TMP_DIR_NAME, shell=True)			# remove temp	
