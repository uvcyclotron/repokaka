import ast
import json
import os
import collections
from post_comment import post_comment
from post_commit_comment import post_commit_comment
from sloc_count import sloc_count
from flask import Flask, render_template, request, url_for,jsonify
from flask_json_multidict import get_json_multidict
from github import Github
from github import IssueComment, CommitComment

app = Flask(__name__)
#from post_comment import post_comment

COMMENT_ON_PR="pull"
COMMENT_ON_ISSUE="issues"
CODE_KAKA="codekaka"
PR="pull_request"

#comment_type because, GitHub doesn't differentiate the comments between issues comments and PR comments.
PR_COMMENT="issue_comment"
COMMIT_COMMENT="commit_comment"

PR_SIZE_SMALL=5
PR_SIZE_MEDIUM=10
#PR_SIZE_LARGE=2

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
    def process_tagged_comment(self,comment):
            reply="You have selected option"
            if comment.find(1):
                reply+="1,"
            elif comment.find(2):
                reply+="2,"
            return "You just tagged me! I am always at your service"

    def get_reply_to_PR(self,dict_payload):
            return "Here are the results of your PR"

    def get_reply_to_CC(self):
        return "Responding to commit comment"

    def respond_to_PR_comment(self,dict_payload,rest_git):
            comment,issue_num,commenting_user,comment_type=self.get_comment_details(dict_payload)
            if(not (commenting_user == 'codekaka')  and comment_type is COMMENT_ON_PR and self.is_codekaka_tagged(comment)):
                    reply=self.process_tagged_comment(comment)
                    print "before post comment"
                    post_comment_status=post_comment(reply, rest_git, self.user,self.repo,issue_num)
                    print "SUCCESS" if isinstance(post_comment_status, IssueComment.IssueComment) else "FAILURE"

    def repsond_to_PR(self,rest_git,dict_payload):
            reply=self.get_reply_to_PR()
            issue_num=dict_payload['pull_request']['number']
            pr_diff_url=dict_payload['pull_request']['diff_url']
            pr_size=sloc_count(pr_diff_url)
            if(pr_size<=PR_SIZE_SMALL):
                return
            elif(pr_size<=PR_SIZE_MEDIUM):
                reply=get_reply_to_PR(dict_payload)
                post_comment_status=post_comment(reply, rest_git,self.user,self.repo,issue_num)
                print "SUCCESS" if isinstance(post_comment_status, IssueComment.IssueComment) else "FAILURE"
            elif(pr_size>PR_SIZE_MEDIUM):
                reply="Pull request was made succesfully, do you want me to run the below analysis? 1. Code coverage, 2. New dependencies added, 3. Documentation"
                post_comment_status=post_comment(reply, rest_git,self.user,self.repo,issue_num)
                print "SUCCESS" if isinstance(post_comment_status, IssueComment.IssueComment) else "FAILURE"



    def respond_to_commit_comment(self,rest_git,dict_payload):
        reply=self.get_reply_to_CC()
        sha_num=dict_payload['comment']['commit_id']
        comment=dict_payload['comment']['body']
        if(self.is_codekaka_tagged(comment)):
            post_comment_status=post_commit_comment(reply, rest_git,self.user,self.repo,sha_num)
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


        if(self.method==PR_COMMENT):
                print "inside PR_COMMENT"
                self.respond_to_PR_comment(dict_payload,rest_git)
        elif(self.method==PR):
                print "inside PR"
                self.repsond_to_PR(rest_git,dict_payload)
        elif(self.method==COMMIT_COMMENT):
            print "inside commit comment"

            self.respond_to_commit_comment(rest_git,dict_payload)


#Main function that handles the post request
@app.route('/<user>/<repo>/<method>',methods=['POST'])
def func_main(user,repo,method):
        crabot_obj=crabot(user,repo,method,request)
        crabot_obj.process_request()
        return "Obtained data"


if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
