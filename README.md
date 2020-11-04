# T.py

T.py is a fast way to record and list todos from multiple places: git tracked lists, github and gitlab issues, and commented todos within code.

## Use Case 1: Checking Todos from git tracked lists

Go through a file w/ all git repos. Go into that repo and check for a .todo file.
Each line in that .todo file is a todo.  If it has a [] in it, those are options. Number each todo

## Use Case 2: Solving todos from git tracked lists

Track number.  Go into repo, delete line in .todo file.  Commit w/ a message like "Resolving todo: ...".

## Use Case 2: Checking todos from github/gitlab issues

Use ghi or Itxaka/pyapi-gitlab to get issues.  save their number.  When completed, go into that repo and commit w/ message like "Closes issue #...".

## Use Case 3: Check for commented todos

Go into every repo, check every file for ` // TODO[]:...` or `# TODO[]:...` or
`\todo{...}`.  Add into list.

## Use Case 4: Track your todo progress with git?

t.py has a store which is a git repo and it consists of a list of all todos and then removal of them when completed.  This means that we can write up a quick weekly summary or a long list.  We could put this as a private github repo.

## Use Case 5: If a repo isn't available, don't make changes and include in list

## Use Case 6: Jira Issue tracking

https://jira.pnnl.gov/jira/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery=assignee+%3D+currentUser%28%29+AND+resolution+%3D+Unresolved+order+by+updated+DESC&tempMax=2000