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
def util_coverage_calc():
	if(request_type==COMMENT_ON_PR or request_type==COMMIT_COMMENT or request_type==PR):
		pr_url = str(dict_payload['issue']['pull_request']['url'])
		result = coverage_helper(pr_url)
	if(result)
		return result
	else
		return "Could not find coverage information from Cobertura!"
