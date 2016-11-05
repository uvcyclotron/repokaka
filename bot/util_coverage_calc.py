# util_coverage_calc
# utility for calculating code coverage
# using PyGithub
# for CRA-BOT

from github import Github
from coverage_calc.coverage_helper import coverage_helper


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

def util_coverage_calc(dict_payload, request_type):
	if(request_type==COMMENT_ON_PR or request_type==COMMIT_COMMENT or request_type==PR):
		pr_url = str(dict_payload['issue']['pull_request']['url'])
		result = coverage_helper(pr_url)
	if(result):
		return result
	else:
		return "Could not find coverage information from Cobertura!"
