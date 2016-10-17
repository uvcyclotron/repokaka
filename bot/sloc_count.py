# sloc_count
# source-lines-of-code count helper function
# using PyGithub
# for CRA-BOT 

import urllib2

'''
method parameters:
	diff_url	is the url for diff file

returns count of line number, returns 0 on error.

For our purpose, an estimate of the line number count is enough. We don't need to
be pedantic about the actual number of lines, so we do not bother with a really precise
count of lines changed. 
'''

def sloc_count(diff_url):
	try:
		response = urllib2.urlopen(diff_url)
		response_data = response.read()
		return response_data.count('\n')
	except urllib2.HTTPError as ex:
		return 0
