# Fix Design

## Actions

### 1. Consider Pull Request triggered interaction. Otherwise does not fit in bot paradigm
We have modifed our design, and now it runs on cloud server instead of running locally. It is also triggered automatically on submission of Pull Request. 

### 2. Redesign workflow to have bot populate data automatically for code reviews, not by dev !
Resdesign done to run it automaticlly, and then post results as comment on the pull request itself. Reviewer can see this comment from bot, and it will help him/her evaluate the code faster. We are much happier with it now. 

### 3. Additional Patterns?
Added event systems as an additional pattern for crabot.
