# CRABOT - Code Review Assist Bot

## Use Cases

####Use Case: Get Code-review-stats for new pull-requests (large-sized)

1 Preconditions
   Repo owner must have added bot as a collaborator.

2 Main Flow
   User will submit a PR to repo [S1]
   Bot provides list of differnt analysis it can do [S2]
   Reviewer provides go-ahead for the analysis he/she wants [S3]
   Bot runs analysis, and posts stats as a comment [S4]

3 Subflows
  [S1] User submits PR to repo.
  [S2] Bot will get auto-invoked from web hook, and will return a list of analysis it can run on the code. 
  [S3] User will confirm which analysis to run.
  [S4] Bot will run requested analysis, and post stats on the GitHub comment thread.

4 Alternative Flows
  [E1] User can choose all or some of the offered services for the bot to run.
  [E2] User can choose not to run any analysis.

--------------------------------------------------

#####Use Case: Get Code-review-stats automatically for new pull-requests (medium-sized) 

1 Preconditions
   Repo owner must have added bot as a collaborator.
   We will define medium-size code by an arbitrary SLOC range.

2 Main Flow
   User will submit a PR to repo [S1]
   Bot detects size of PR to be medium, runs analysis automatically and posts stats as a comment [S2]

3 Subflows
  [S1] User submits PR to repo.
  [S2] Bot will get auto-invoked from web hook, will run analysis, and post stats on the GitHub comment thread.

4 Alternative Flows
  N/A

--------------------------------------------------  

####Use Case: Get Code-review-stats for new pull-requests (small-sized) 

1 Preconditions
   Repo owner must have added bot as a collaborator.
   We will define small-size code by an arbitrary SLOC range.

2 Main Flow
   User will submit a PR to repo [S1]
   Bot detects size of PR to be small, and so ignores it [S2]
   User can manually invoke the bot to run specific analysis [S3]
   Bot runs analysis, and posts stats as a comment [S4]

3 Subflows
  [S1] User submits PR to repo.
  [S2] Bot will get auto-invoked from web hook, detects small code size, and so ignores it.
  [S3] User will request different analysis to run.
  [S4] Bot will run requested analysis, and post stats on the GitHub comment thread.

4 Alternative Flows
  N/A

--------------------------------------------------  

####Use Case: Get Code-review-stats manually for specific commit(s)

1 Preconditions
   Repo owner must have added bot as a collaborator. 

2 Main Flow
   User will choose a commit, and invoke bot [S1]
   Bot provides list of differnt analysis it can do on that commit [S2]
   Reviewer provides go-ahead for the analysis he/she wants [S3]
   Bot runs analysis, and posts stats as a comment [S4]

3 Subflows
  [S1] User calls bot on a specific commit, by invoking it via comments.
  [S2] Bot will return a list of analysis it can run on the code. 
  [S3] User will confirm which analysis to run.
  [S4] Bot will run requested analysis, and post stats on the GitHub comment thread.

4 Alternative Flows
  [E1] User can choose all or some of the offered services for the bot to run.



## Mocking

## Bot Implementation

## Selenium Testing of each use case

## Task Tracking

The task tracking can be seen in the [WORKSHEET] (WORKSHEET.md)

## Screencast



