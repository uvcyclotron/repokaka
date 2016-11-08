# coverage_helper
# for CRA-BOT 

from github import Github
import json
from pprint import pprint
from subprocess import call
from lxml import html
import requests
import os.path 

'''
method parameters: url for pulls json data
	
returns ..
description 
	Parses the json to get repo clone url, and repo name
	Downlaods the code from clone url, builds it using maven, then runs coverage tool
	Returns text with overall coverage result
'''
TMP_DIR_NAME = 'tmp_coverage'
def coverage_helper(pull_url):

	# get PR json
	# with open('mvn_sample_txt') as pr_json:
		# data = json.load(pr_json)
	# print pull_url

	pull_json_text =  requests.get(pull_url)
	data = json.loads(pull_json_text.content)

	repouri = data['head']['repo']['clone_url']
	reponame = data['head']['repo']['name']

	# temp testing
	# repouri = 'https://github.com/checkstyle/checkstyle.git'
	# reponame = 'checkstyle'
	# print repouri, reponame

	# get code from github
	#
	try:

		call('mkdir '+TMP_DIR_NAME, shell=True)							# make temp dir
		call("git clone " + repouri, shell=True, cwd='./temp') 	# clone repo in temp


		# do maven build, and then run cobertura
		#
		cmdlist = list()
		cmdlist.append("git checkout mvn")				#TODO remove later
		cmdlist.append("mvn install") 						# build project
		cmdlist.append("mvn cobertura:cobertura")			# run cobertura
		print cmdlist

		for cmd in cmdlist:
			call(cmd, shell=True, cwd='./' + TMP_DIR_NAME + '/'+reponame) 		# run util on cloned code

		# cobertura report parsing
		cob_path = './' + TMP_DIR_NAME + '/' + reponame + '/target/site/cobertura/frame-summary.html'
		if os.path.isfile(cob_path):
			# print 'yes'
			return parse_coverage_results(cob_path)
		else:
			return "Unable to generate Coverage report! Possibly a build error!"

	except (RuntimeError, TypeError, NameError) as ex:
		print 'exception occurred'
		print ex

	finally:
		print 'deleting temp dir'
		call('rm -rf ' + TMP_DIR_NAME, shell=True)							# remove temp


def parse_coverage_results(cobertura_report_path):

	with open(cobertura_report_path) as coverage:
		# print coverage.read()
		tree = html.fromstring(coverage.read())

		classes = tree.xpath("//tbody//tr//td//table//td[@class='percentgraph']/text()")
		if(classes):
			retstr = "\nLine Coverage: "+ classes[0] + "\nBranch Coverage: " + classes[1]
			return retstr 
		else:
			return "Null classes"

		# linecoverage = [int(x[:-1]) for x in classes[2::2]]
		# branchcoverage = [int(x[:-1]) for x in classes[3::2]]
		# ml = median(linecoverage)
		# mb = median(branchcoverage)
		# package_names = tree.xpath("//tbody//tr//td//a/text()")


		# print "Package Name\tLine Coverage\tBranch Coverage"
		# for i in range(len(package_names)):
			# print "{}\t{}\t{}".format(package_names[i], linecoverage[i], branchcoverage[i])

		# print 'Br Cov: ', branchcoverage, 'median: ', mb
		# print 'Line Cov: ', linecoverage, 'median: ', ml
		return ml, mb


def median(s):
	s = sorted(s)
	i = len(s)
	if not i % 2:
		return (s[(i/2)-1]+s[i/2])/2.0
	return s[i/2]		
