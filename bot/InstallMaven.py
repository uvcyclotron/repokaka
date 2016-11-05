from subprocess import Popen
from subprocess import call
from github import Github
import subprocess
import os

# need to change this path. Assign the actual path
path = "/Users/Anindita/SE/SEproject/checkstyle-master"


os.chdir(path)
pmvn = subprocess.Popen("mvn install", stdout=subprocess.PIPE, shell = True)
pcob=subprocess.Popen("mvn cobertura:cobertura", stdout=subprocess.PIPE, shell = True)

output, err = pcob.communicate()

pcob_status = pcob.wait()
print "output status", err
print "Return code", pcob_status	