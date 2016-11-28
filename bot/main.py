import ast
import json
import os
import collections
from post_comment import post_comment
from post_commit_comment import post_commit_comment
from sloc_count import sloc_count
from util_dependency_checker import util_dependency_checker
from util_docu_collector import util_docu_collector
from util_duplicates_checker import util_duplicates_checker
from util_clone_wrapper import util_clone_wrapper
from utils_crabot import get_list_changed_files
from flask import Flask, render_template, request, url_for,jsonify
from flask_json_multidict import get_json_multidict
from github import Github
from github import IssueComment, CommitComment
#import logging
#logging.basicConfig(filename='/home/ubuntu/example.log',level=logging.INFO)
#from validate_sha import validate_sha

app = Flask(__name__)
#from post_comment import post_comment

#If a comment is made on Pull Request
COMMENT_ON_PR="pull"
#If a comment is made on issues
COMMENT_ON_ISSUE="issues"
CODE_KAKA="codekaka"
#If a Pull Request is used
PR="pull_request"

DESCRIPTION_TEXT="""Do you want me to run any or all of the following analysis?
                    \ns1: Code coverage
                    s2: Code Duplication
                    s3: Dependency Analysis
                    s4: Documentation
                    run all: To run all the above analysis
                    \nPlease reply with s1, s2, s3, s4 or 'run all' for the respective analysis
                    Example 1: To run Code coverage, Code Duplication, reply with "run s1,s2"
                    Example 2: To run all the analysis, reply with "run all".
                    Note: Reply commands are not case sensitive."""

#comment_type because, GitHub doesn't differentiate the comments between issues comments and PR comments. Issue comments are ignored
PR_COMMENT="issue_comment"
COMMIT_COMMENT="commit_comment"

PR_SIZE_SMALL=10
PR_SIZE_MEDIUM=20
#PR_SIZE_LARGE=2

# Crabot class which takes care of all the crabot functionalities. It handles Pull request, Comment on pull request
# And comment on commit events occuring on a repo where user @codekaka is added as a collaborator.
class crabot:
    def __init__(self, user, repo, method,request):
        self.user=user
        self.repo=repo
        self.method=method
        self.request=request

    def convert_dict_string(self,data):
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(self.convert_dict_string, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.convert_dict_string, data))
        else:
            return data

    #Get payload from the request object
    def get_payload(self,request_dict):
            #Extracting payload and converting it from unicode to str
            str_req_dict=str(request_dict['payload'])
            temp_dict=str_req_dict.replace("'", "\"")
            temp_dict=str(str_req_dict)
            #loading a json object from the string
            dict_payload=json.loads(temp_dict)
            return dict_payload


    #Get comment text from the payload dict
    def get_comment_details(self,dict_payload):
            comment=dict_payload['comment']['body']
            issue_num=dict_payload['issue']['number']
            commenting_user=dict_payload['comment']['user']['login']
            html_url=dict_payload['comment']['html_url']
            list_html_url=html_url.split('/')
            if(COMMENT_ON_PR in list_html_url):
                    comment_type=COMMENT_ON_PR
            # If the comment is made on a issue then ignore.
            elif(COMMENT_ON_ISSUE in list_html_url):
                    comment_type=COMMENT_ON_ISSUE

            return str(comment),issue_num,str(commenting_user),comment_type

    def is_codekaka_tagged(self,comment):
            return comment.find(CODE_KAKA)> -1

    #Process tagged comment
    def process_tagged_comment(self,comment,dict_payload,request_type):
            print "comment is "+ comment
            reply=""
            results=""
            count=0
	    comment=comment.lower()
            if comment.find('run all')>-1:
                reply="Ran all the analysis and here are the results:\n"
                list_files=get_list_changed_files(dict_payload,request_type)
                results += "\nCODE DOCUMENTATION RESULTS:\n-----------------------\n"
                results+=util_docu_collector(list_files)
                # clone wrapper handles coverage util, and duplicates util
                results += "\nCODE COVERAGE AND CODE DUPLICATE CHECK RESULTS:\n-----------------------\n"
                results+=util_clone_wrapper(dict_payload, request_type, True, True)
                results += "\nCODE DEPENDENCY CHECK RESULTS:\n-----------------------\n"
                results+=util_dependency_checker(dict_payload,request_type)
                return reply,results

            coverageUtilRunFlag = False
            duplicateUtilRunFlag = False

            if comment.find('s1')>-1:
                count+=1
                reply+=" s1"
                coverageUtilRunFlag = True
            if comment.find('s3')>-1:
                count+=1
                reply+=", s3"
                results += "\nCODE DEPENDENCY CHECK RESULTS:\n-----------------------\n"
                results+=util_dependency_checker(dict_payload,request_type)
            if comment.find('s2')>-1:
                count+=1
                reply+=", s2"
                duplicateUtilRunFlag = True
                # handle coverage and duplicates

            if coverageUtilRunFlag:
                results += "\nCODE COVERAGE CHECK RESULTS:\n-----------------------\n"
                results += util_clone_wrapper(dict_payload, request_type, coverageUtilRunFlag, duplicateUtilRunFlag)

            if duplicateUtilRunFlag:
                results += "\nCODE DUPLICATE CHECK RESULTS:\n-----------------------\n"
                results += util_clone_wrapper(dict_payload, request_type, coverageUtilRunFlag, duplicateUtilRunFlag)    

            if comment.find('s4')>-1:
                count+=1
                reply+=", s4."
                list_files=get_list_changed_files(dict_payload,request_type)
                results += "\nCODE DOCUMENTATION RESULTS:\n-----------------------\n"
                results+=util_docu_collector(list_files)

            if count>0:
                if(count==1):
                    reply=reply.replace(",","")
                    reply="\nYou have selected option "+reply+"\n"
                else:
                    reply="\nYou have selected options "+reply+"\n"
            else:
                reply=DESCRIPTION_TEXT
            return reply,results

    def respond_to_PR_comment(self,dict_payload,rest_git):
            comment,issue_num,commenting_user,comment_type=self.get_comment_details(dict_payload)
            if(not (commenting_user == 'codekaka')  and comment_type is COMMENT_ON_PR and self.is_codekaka_tagged(comment)):
                    reply,results=self.process_tagged_comment(comment,dict_payload,COMMENT_ON_PR)
                    print "before post comment"
                    post_comment_status=post_comment(reply+results, rest_git, self.user,self.repo,issue_num)
                    print "SUCCESS" if isinstance(post_comment_status, IssueComment.IssueComment) else "FAILURE"

    def respond_to_PR(self,rest_git,dict_payload):
            reply=""
            issue_num=dict_payload['pull_request']['number']
            pr_diff_url=dict_payload['pull_request']['diff_url']
            pr_size=sloc_count(pr_diff_url)
            print "\n\n\n PR_SIZE is: ",pr_size
            if(pr_size<=PR_SIZE_SMALL):
                reply="""Pull request was made succesfully and this is a small sized Pull Request. Do you still want me to run analysis? \n
                        Reply with: \nrun s1: Code coverage,
                        \nrun s2: Code Duplication,
                        \nrun s3: Dependency Analysis,
                        \nrun s4: Documentation
                        \nrun all: To run all the above analysis
                        """

            elif(pr_size<=PR_SIZE_MEDIUM):
                reply=""
		temp=""
                reply+=" This is a medium sized Pull Request."
                temp,result=self.process_tagged_comment('@codekaka run all',dict_payload,PR)
                reply+=temp+result

            elif(pr_size>PR_SIZE_MEDIUM):
                reply="Pull request was made succesfully and this is a large sized Pull Request."+ DESCRIPTION_TEXT
            post_comment_status=post_comment(reply, rest_git,self.user,self.repo,issue_num)
            print "SUCCESS" if isinstance(post_comment_status, IssueComment.IssueComment) else "FAILURE"

    def respond_to_commit_comment(self,rest_git,dict_payload):
        sha_num=dict_payload['comment']['commit_id']
        comment=dict_payload['comment']['body']
        if(self.is_codekaka_tagged(comment)):
            reply,results=self.process_tagged_comment(comment,dict_payload,COMMIT_COMMENT)
            post_comment_status=post_commit_comment(reply+results, rest_git,self.user,self.repo,sha_num)
            print "SUCCESS" if isinstance(post_comment_status, CommitComment.CommitComment) else "FAILURE"

    def process_request(self):
        #Extracting the information from the request object
        self.request.body = self.request.form
        if self.request.headers['content-type'] == 'application/json':
                self.request.body = get_json_multidict(self.request)
        body = self.request.body

        # Formatting it as a dictionary
        request_dict={key: body[key] for key in body}
        dict_payload_uni=self.get_payload(request_dict)
        dict_payload=self.convert_dict_string(dict_payload_uni)
        rest_git=Github(os.environ['oauth_token'])
        print dict_payload
        #logging.info(dict_payload)

        if(self.method==PR_COMMENT):
                print "inside PR_COMMENT"
                self.respond_to_PR_comment(dict_payload,rest_git)
        elif(self.method==PR):
                print "inside PR"
                self.respond_to_PR(rest_git,dict_payload)
        elif(self.method==COMMIT_COMMENT):
                print "inside commit comment"
                self.respond_to_commit_comment(rest_git,dict_payload)


#Main function that handles the post request
@app.route('/<user>/<repo>/<method>',methods=['POST'])
def func_main(user,repo,method):
    print "**************************" , request.form
    #logging.info(request.form)
    crabot_obj=crabot(user,repo,method,request)
    crabot_obj.process_request()
    return "Obtained data"


if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
