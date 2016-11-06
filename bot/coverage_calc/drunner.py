from coverage_helper import coverage_helper
from coverage_helper import parse_coverage_results

durl = "https://api.github.com/repos/netty/netty/pulls/5940"
durl2 = "https://api.github.com/repos/codekaka/Repo1/pulls/115"
# parse_coverage_results()

reponame = 'Repo1'
cob_path = './temp/' + reponame + '/target/site/cobertura/frame-summary.html'
#print parse_coverage_results(cob_path)

print coverage_helper(durl2)
