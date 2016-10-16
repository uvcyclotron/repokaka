# comment helper

def post_comment(text, github_object, user, reponame, issue_number):
	user_var = github_object.get_user(user)
	repo_var = user_var.get_repo(reponame)
	issue_var = repo_var.get_issue(issue_number)
	issue_var.create_comment(text)