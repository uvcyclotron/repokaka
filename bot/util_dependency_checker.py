# util_dependency_checker
# utility for checking dependency changes
# using PyGithub
# for CRA-BOT

from github import Github
import urllib2
import json
from utils_crabot import get_list_changed_files

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

	list_files=get_list_changed_files(dict_payload,request_type)
	result=extract_result(list_files)
	added_code,removed_code=format_result(result)

	if(bool(added_code) or bool(removed_code)):
		final_result="\nDEPENDENCY CHANGE ANALYSIS:\n"

	if(bool(added_code)):
		final_result+="Added Dependencies are: \n"+added_code+"\n"
	removed_code.replace("\n","")
	if(bool(removed_code):
		final_result+="Removed Dependencies are: \n"+ removed_code+"\n"

	# final_result=final_result.replace("<","&lt;")
	# final_result=final_result.replace(">","&gt;")
	print final_result
	if not final_result or final_result.isspace():
		return "No new dependency added.\n"
	return final_result
