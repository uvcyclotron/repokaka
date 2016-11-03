# util_docu_collector
# utility for collecting code documentation
# using PyGithub
# for CRA-BOT

from github import Github
import subprocess


'''
method parameters:
	x		is

returns ..

description..

'''
def util_docu_collector():
	return """

DOCUMENTATION
------------------
@Class_M :
/** ....
*	....
*	....
*/

@method_A :
// ....
// ....
// ....

@method_B :
// ....
// ....
// ....
"""

def Rit_check
subprocess.call(["doxygen", "-g", "config-file"])
configFile = open('config-file', 'r')
fileContent = configFile.read()
configFile.close()
splitContent = fileContent.split()

cnt = 0
length = len(splitContent)
while(cnt < length)
	if(splitContent[cnt] == "EXTRACT_ALL" )
		splitContent[cnt+2] = "YES"
	if(splitContent[cnt] == "GENERATE_RTF")
		splitContent[cnt+2] = "YES"
fileContentUpdate = .join(splitContent)
configFile = open('config-file', 'w')

subprocess.call(["doxygen", "config-file"])
#print ls_output
