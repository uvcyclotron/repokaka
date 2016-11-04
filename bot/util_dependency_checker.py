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


def parse_patch(patch):
	patch_list=[]
	patch_list=patch.split('@@')
	patch_data=patch_list[2]
	return str(patch_data)

def format_result(result):
	added_code=""
	removed_code=""
	result_list=result.split('\n')
	for item in result_list:
		if str(item).startswith('+'):
			added_code+=str(item)[1:]+"\n"
		elif str(item).startswith('-'):
			removed_code+=str(item)[1:]+"\n"

	return added_code,removed_code

def extract_result(data):
	result=""
	for item in data:
		filename=item['filename']
		if('xml' in filename):
			patch_data = parse_patch(item['patch'])
			result+=filename+'\n'+patch_data
	return result

def util_dependency_checker(dict_payload,request_type):
	url=''
	result=''
	final_result=""
	print '---------------------------------------------------Request type is ---------------------------------------------------'
	print request_type
	#if the comment is made on a PR
	if(request_type==COMMENT_ON_PR):
		url=str(dict_payload['issue']['pull_request']['url'])+"/files"
		response=urllib2.urlopen(url)
		print "INSIDE COMMENT_ON_PR"
		data = json.load(response)
		result=extract_result(data)

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
		result=extract_result(data)


	#Triggered when a PR is made.
	elif(request_type==PR):
		print "INSIDE PR"
		url=str(dict_payload['pull_request']['url'])+"/files"
		response=urllib2.urlopen(url)
		data = json.load(response)
		result=extract_result(data)

	added_code,removed_code=format_result(result)

	if(bool(added_code) or bool(removed_code)):
		final_result="\nDEPENDENCY CHANGE ANALYSIS:\n"

	if(bool(added_code)):
		final_result+="Added Dependencies are: \n"+added_code+"\n"
	if(bool(removed_code.replace("\n",""))):
		final_result+="Removed Dependencies are: \n"+ removed_code+"\n"

	final_result=final_result.replace("<","&lt;")
	final_result=final_result.replace("<","&&gt;")
	print final_result
	return final_result
