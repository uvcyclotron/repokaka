# sha validator function
# using PyGithub
# for CRA-BOT 

from github import Github
from github import GithubException

'''
method parameters :
	github_object 	is pygithub library object created by caller
	user 			is username for the repo
	reponame 		is repository name where issue exists
	sha			 	is the SHA hash which needs validation

method returns -1 for invalid sha, and returns object of type Commit on valid sha
'''
def validate_sha(github_object, user, reponame, sha):
	try:
		user_var = github_object.get_user(user)

		repo_var = user_var.get_repo(reponame)

		commit_var = repo_var.get_commit(sha)

		return commit_var

	except GithubException as ex:
		return -1