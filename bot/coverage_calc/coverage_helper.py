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
method parameters: tmp dir name variable, repository name
	
description 
	Builds the source code using maven
	Runs Cobertura code analysis
	Parses report from Cobertura
	Returns text with overall coverage result
'''
def coverage_helper(TMP_DIR_NAME, reponame):

	try:
		cmdlist = list()
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
			return "\nUnable to generate Coverage report!\n Possibly a build error!\n"

	except (RuntimeError, TypeError, NameError) as ex:
		print '\nException occurred\n'
		print ex
		return '\nError generating coverage report!\n'


def parse_coverage_results(cobertura_report_path):

	with open(cobertura_report_path) as coverage:
		# print coverage.read()
		tree = html.fromstring(coverage.read())

		classes = tree.xpath("//tbody//tr//td//table//td[@class='percentgraph']/text()")
		if(classes):
			retstr = "\nLine Coverage: "+ classes[0] + "\nBranch Coverage: " + classes[1] + "\n\n"
			return retstr 
		else:
			return "\nNull classes\n"

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
