# CRABOT - Code Review Assist Bot

## 1. Services
Bot listens to web-hooks as described in [bot.md](https://github.ncsu.edu/uverma/crabot/blob/master/bot.md#bot-platform), and calls the scripts for each requested service. Service implementations run as independent modules, and return analysis result as text to the parent calling method of bot.

The services which need to get all the code first by cloning the git repository, are passed through a clone wrapper script, which handles git cloning, and then invokes the required service modules. This helps the bot avoid cloning multiple times in a single run. 


#### a. Documentation Collector

We are using [*Doxygen*](http://www.stack.nl/~dimitri/doxygen/) for generating documentation, where it goes through each source file, retrieves all in-code documentation for classes and methods and creates a man file. 

In this service the bot first generates Java files from the patched files (the files which have been modified in the PR) and later runs Doxygen on it. The documentation is generated as a Man Page which bot then converts to a Text file. The results from the Text file are returned to the calling method.

#### b. Code Coverage Reporter

We are using [*Cobertura*](http://cobertura.github.io/cobertura/) for calculating code coverage. It can work on maven-based projects, and provide results in well-formated HTML file.

In this service implementation, the bot first clones the git repository. It then builds the repository using maven, and then runs Cobertura tool on it, which genreates the report file.
Finally, the bot parses the report html, and gets the the coverage report results. The results are reported back to the calling method.

#### c. Duplicate Code Checker

We are using [*PMD*](https://pmd.github.io/) for duplicate code checking in the repository. 

In this serivce implementation, the bot first clones the git repository. It then runs PMD on the repository and returns the information on duplicate code that it finds.

#### d. Dependency Tracker

When developer adds some new method which asks for a new dependency, maven's `pom.xml` file is updated with the new dependency.
And code reviewer might be interested in the added or removed dependencies. This service analyses the diff of the `pom.xml` file and returns added new dependencies or removed dependencies. The logic of the service is completely developed by us without using any third party tools.


## 2. Use Cases

For each use-case, the requested services are invoked, and they run as explained in the previous section.

#### Use Case #1 Get Code-review-stats for new pull-requests (large-sized)

	Happy Case: Bot is invoked automatically and then asks the user for any specific service to run.
	Alternate Case: Bot is invoked automatically and then runs all the services. 


#### Use Case #2 Get Code-review-stats automatically for new pull-requests (medium-sized) 

	Happy Case: Bot is invoked automatically and then runs all the services. 
	Alternate Case: Bot is invoked by the user and the user asks for the specific services to run. 


#### Use Case #3 Get Code-review-stats for new pull-requests (small-sized) 

	Happy Case: Bot is invoked automatically and then asks the user whether to run all the services. 
	Alternate Case: Bot is invoked automatically and then asks the user for any specific service to run.


#### Use Case #4 Get Code-review-stats manually for specific commit(s)

	Happy Case: Bot is invoked by the user for the specific commit and the user asks the bot for the specific services to run. 
	Alternate Case: N/A


## Task Tracking

Task Tracking Worksheet: [WORKSHEET](WORKSHEET.md)

## Screencast

+ [Use Cases] 
