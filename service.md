# CRABOT - Code Review Assist Bot

## Services
Bot listens to web-hooks as decribed, and calls the scripts for each requested service. Service implementations run as independent modules, and return analysis result as text to the parent calling method of bot.


### Documentation Collector

### Code Coverage

We are using *Cobertura* for calculating code coverage. It can work on maven-based projects, and provide results in well-formated HTML file.

In this service implementation, the bot first clones the git repository. It then builds the repository using maven, and then runs Cobertura tool on it, which genreates the report file.
Finally, the bot parses the report html, and gets the the coverage report results. The results are reported back to the calling method.


### Duplicate Checker

### Dependency Tracker


### 

##Use Case #1 

####Get Code-review-stats for new pull-requests (large-sized)

##Use Case #2: 

####Get Code-review-stats automatically for new pull-requests (medium-sized) 

##Use Case #3: 

####Get Code-review-stats for new pull-requests (small-sized) 

##Use Case #4: 

####Get Code-review-stats manually for specific commit(s)

## Task Tracking

Task Tracking Worksheet: [WORKSHEET](WORKSHEET.md)

## Screencast

+ [Use Cases] 