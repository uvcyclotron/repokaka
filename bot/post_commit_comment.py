# comment helper function for commits
# using PyGithub
# for CRA-BOT 

from github import Github
from github import GithubException

'''
method parameters :
	text 			is the comment to be posted
	github_object 	is pygithub library object created by caller
	user 			is username for the repo
	reponame 		is repository name where issue exists
	sha			 	is the SHA hash of the commit on which comment will be posted

method returns -1 for errors and exceptions, and returns object of type IssueComment on success
'''
def post_commit_comment(text, github_object, user, reponame, sha):

	# verify sane input types 
	# if(not(type(text) == str and
	# 	isinstance(github_object, Github) and
	# 	type(user) == str and
	# 	type(reponame) == str and
	# 	type(sha) == str )):
	# 	return -1

	# handle exceptions from bad inputs
	try:
		user_var = github_object.get_user(user)

		repo_var = user_var.get_repo(reponame)

		commit_var = repo_var.get_commit(sha)

		return commit_var.create_comment(text)

	except GithubException as ex:
		print "Exception occured !"
		print type(ex) 
		return -1
