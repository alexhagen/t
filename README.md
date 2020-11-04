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

