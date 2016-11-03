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

def rit_check():
	# Get the patches

	# Doxygen script
	subprocess.call(["doxygen", "-g", "config-file"])
	subprocess.call("perl -pi -w -e 's/EXTRACT_ALL            = NO/EXTRACT_ALL            = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/GENERATE_MAN           = NO/GENERATE_MAN           = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/EXTRACT_PRIVATE        = NO/EXTRACT_PRIVATE        = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/EXTRACT_STATIC         = NO/EXTRACT_STATIC         = YES/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/GENERATE_HTML          = YES/GENERATE_HTML          = NO/g;' config-file", shell=True)
	subprocess.call("perl -pi -w -e 's/GENERATE_LATEX         = YES/GENERATE_LATEX         = NO/g;' config-file", shell=True)
	subprocess.call(["doxygen", "config-file"])

	# Cat all the man pages of the patches
	subprocess.call("cat *.3 >> document.3", shell=True)

	# Convert the man pages to txt
	subprocess.call("groff -t -e -mandoc -Tascii document.3 | col -bx > manpage.txt", shell=True)

	# Strip off unneccesary details

	# Read the txt file and post it as a comment. 

	#print ls_output

def main():
	rit_check()


if __name__=="__main__":
	main()
