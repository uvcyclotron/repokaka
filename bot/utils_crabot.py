import urllib2
import json

def get_list_changed_files(dict_payload,request_type):
	PR_COMMENT="issue_comment"
	COMMIT_COMMENT="commit_comment"
	COMMENT_ON_PR="pull"
	PR="pull_request"
	#if the comment is made on a PR
	if(request_type==COMMENT_ON_PR):
		url=str(dict_payload['issue']['pull_request']['url'])+"/files"
		response=urllib2.urlopen(url)
		print "INSIDE COMMENT_ON_PR"
		data = json.load(response)

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

	#Triggered when a PR is made.
	elif(request_type==PR):
		print "INSIDE PR"
		url=str(dict_payload['pull_request']['url'])+"/files"
		response=urllib2.urlopen(url)
		data = json.load(response)

	return data
