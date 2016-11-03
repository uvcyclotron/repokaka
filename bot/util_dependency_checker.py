# util_dependency_checker
# utility for checking dependency changes
# using PyGithub
# for CRA-BOT

from github import Github


'''
method parameters:
	x		is

returns ..

description..

'''
def util_dependency_checker(dict_payload):
	print "dict payload is"
	pritn dict_payload
	return """
Dependency Changes:
---------------------
+ boto.py
+ pygithub.py
- pyunit
"""
