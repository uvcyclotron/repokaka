
#### Idea:
TestRepo is an open source project. A new user wants to add some cool features into the existing repo. To do this, he forks from the existing repo and adds his changes. He will then create a pull request and request the owner (`@chethan1801`) of TestRepo to review his code changes. chethan1801 knows that his project is popular and he gets several requests from software engineers around the world to review the features they want to add. chethan1801 devises a clever bot, codekaka. codekaka performs the code reviews on the new pull requests and old commits as well.


#### Please follow the steps:

1. Fork from the existing repo https://github.com/chethan1801/TestRepo

2. git clone into your local machine and make changes.

	* 2a. Use Case 1: The number of lines of change is less than 5.

	* 2b. Use Case 2: The number of lines of change is greater than 5 and less than 10.

	* 2c. Use case 3: The number of lines of change is greater than 10.

3. git add

4. git commit

5. git push origin master

6. Click on New pull request. Ensure that base fork is `chethan1801/TestRepo` and head fork is your own `username/TestRepo`. If there are no other open pull requests on https://github.com/chethan1801/TestRepo continue with step 7. Else, navigate to https://github.com/chethan1801/TestRepo and click on pull request associated with your user id. Skip to step 9.

7. Click on Create new pull request.

8. Enter a suitable title and click Create pull request.

9. For different Use Cases.

	* 9a. Use case 1: For a small change, codekaka initiates a dialog
	```
	Pull request was made succesfully and this is a small sized Pull Request. Do you still want me to run analysis?

	s1: Code coverage
	s2: Code Duplication
	s3: Dependency Analysis
	s4: Documentation
	run all: To run all the above analysis

	Please reply with s1, s2, s3, s4 or 'run all' for the respective analysis
	Example 1: To run Code coverage, Code Duplication, reply with "run s1,s2"
	Example 2: To run all the analysis, reply with "run all".
	Note: Reply commands are not case sensitive.
	```

	* 9b. Use case 2: For medium size change, codekaka does not wait for the user's prompt, and instead runs directly to provides all the analysis

	* 9c. Use case 3: For large size change, codekaka initiates dialog

	```
	Pull request was made succesfully and this is a large sized Pull Request.Do you want me to run any or all of the following analysis?

	s1: Code coverage
	s2: Code Duplication
	s3: Dependency Analysis
	s4: Documentation
	run all: To run all the above analysis

	Please reply with s1, s2, s3, s4 or 'run all' for the respective analysis
	Example 1: To run Code coverage, Code Duplication, reply with "run s1,s2"
	Example 2: To run all the analysis, reply with "run all".
	Note: Reply commands are not case sensitive.
	```

10. Execute any of the following commands to run analysis:
	```
	@codekaka run all
	```
	```
	@codekaka run s1
	```
	```
	@codekaka run s2
	```
	```
	@codekaka run s3
	```
	```
	@codekaka run s4
	```

11. Use case 4:
	* 11a. On an existing commit, make a comment as any of the following:
	```
	@codekaka run all
	```
	```
	@codekaka run s1
	```
	```
	@codekaka run s2
	```
	```
	@codekaka run s3
	```
	```
	@codekaka run s4
	```
