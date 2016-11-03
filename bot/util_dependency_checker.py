# util_dependency_checker
# utility for checking dependency changes
# using PyGithub
# for CRA-BOT

from github import Github
import urllib2
import json

'''
method parameters:
	x		is

returns ..

description..

'''

PR_COMMENT="issue_comment"
COMMIT_COMMENT="commit_comment"
COMMENT_ON_PR="pull"
PR="pull_request"
def util_dependency_checker(dict_payload,request_type):
	url=''
	print '---------------------------------------------------Request type is ---------------------------------------------------'
	print request_type
	#if the comment is made on a PR
	if(request_type==COMMENT_ON_PR):
		url=str(dict_payload['issue']['pull_request']['url'])+"/files"
		response=urllib2.urlopen(url)
		print "INSIDE COMMENT_ON_PR"
		data = json.load(response)
		#print "data is-----------"
		#print data
		for item in data:
			print item['patch']
			if('xml' in item['filename']):
				print item['patch']



	#if the comment is made on a commit
	elif(request_type==COMMIT_COMMENT):
		print "INSIDE COMMIT_COMMET"
		commit_id= dict_payload['comment']['commit_id']
		path=dict_payload['repository']['commits_url']
		url=str(path.split('{')[0])+"/"+str(commit_id)
		print "url is:",url
		response=urllib2.urlopen(url)
		data = json.load(response)
		data=data['files']
		print "data is ",data
		for item in data:
			print item['patch']
			if('xml' in item['filename']):
				print item['patch']


	#Triggered when a PR is made.
	elif(request_type==PR):
		print "INSIDE PR"
		url=str(dict_payload['pull_request']['url'])+"/files"
		response=urllib2.urlopen(url)
		data = json.load(response)
		for item in data:
			print item['patch']
			if('xml' in item['filename']):
				print item['patch']


	print '-------------------End dependency checker---------------------------------------------------'
	return """
Dependency Changes:
---------------------
+ boto.py
+ pygithub.py
- pyunit
"""
