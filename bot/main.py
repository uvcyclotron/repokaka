import ast
import json
import os
from flask import Flask, render_template, request, url_for,jsonify
from flask_json_multidict import get_json_multidict
from github import Github


app = Flask(__name__)
#from post_comment import post_comment


#Get payload from the request object
def get_payload(request_dict):
	#Extracting payload and converting it from unicode to str
        str_req_dict=str(request_dict['payload'])
        temp_dict=str_req_dict.replace("'", "\"")

        #loading a json object from the string
        dict_payload=json.loads(temp_dict)
	return dict_payload


#Get comment text from the payload dict
def get_comment(dict_payload):
	comment=dict_payload['comment']['body']
	return comment

#Process the comment and reply
def get_reply(comment):
	return "Howdy, from Crabot"

#Get issue_id
def get_issue_num(dict_payload):
	return dict_payload['issue']['number']




#Main function that handles the post request
@app.route('/<user>/<repo>/<method>',methods=['POST'])
def func_main(user,repo,method):
	#Extracting the information from the request object
	request.body = request.form
    	if request.headers['content-type'] == 'application/json':
        	request.body = get_json_multidict(request)
	body = request.body
	
	# Formatting it as a dictionary
    	request_dict={key: body[key] for key in body}
	
	dict_payload=get_payload(request_dict)
	
	comment=get_comment(dict_payload)
	
	reply=get_reply(comment)
	
	issue_num=get_issue_num(dict_payload)
	
	rest_git=Github(os.environ['oauth_token'])	
	print rest_git
	post_comment_status=post_comment(reply, rest_git,user, repo, issue_id)
	print post_comment_status
	return "Obtained data"

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
