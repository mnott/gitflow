# gf

# Gitflow: A Git Wrapper for Release and Branch Management

This script is a simple Git wrapper for managing local feature, hotfix, and release branches.
It provides a set of commands to start, finish, and update branches, as well as to list
branches, checkout a branch, add files to Git, commit changes, push changes, and
cherry-pick a file from the current branch into a target branch.

It is based on the GitFlow branching model, which is a branching strategy for Git that
defines a strict branching model designed around the project release. This model helps
to manage large projects with multiple developers and teams working on different features
and bug fixes.

You can read about the GitFlow branching model here:

- [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)

Here is an overview:

![](git-branching-model.svg)

The script uses the GitPython library to interact with the Git repository, and the
InquirerPy library to provide an interactive command-line interface for selecting
branches and options.

# Installation

To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```

# Configuration

Before using the script, you need to configure your Git and GitHub settings. You can do
this by running the following command:

```bash
./gitflow.py config
```

If you want to also configure your OpenAI API key for generating commit messages and
explaining files and commits, you can run the following command:

```bash
./gitflow.py config-ai
```


# Usage

To get help about the script, call it with the `--help` option:

```bash
./gitflow.py --help
```

## Starting and Finishing Branches

### Starting a Branch

To start a new local, feature, hotfix, or release branch, run:

```bash
./gitflow.py start ...
```

The options are explained further below.

### Finishing a Branch

Any branch type can be finished by

- Making sure you are on the branch you want to finish (use `checkout`)
- Running:

```bash
./gitflow.py finish
```


## Hotfix Branches

Hotfix branches are used to fix critical bugs in the production code. According to the
GitFlow branching model, hotfix branches are created from the main branch and merged
back into both the main and develop branches. If you have a release branch, you can
(and should) specify the target release branch to merge the hotfix into.

The script provides commands for hotfix branches in general, and for weekly updates
in particular.

### Weekly Update Hotfix Branches

Weekly Update Hotfix Branches are used for minor weekly updates.

To start a new weekly update hotfix branch, run:

```bash
./gitflow.py start -t hotfix
```

Because you are not giving an explicit name, it is going to use the current week
as a branch name.

### Start a Hotfix Branch

To start a new hotfix branch, run:

```bash
./gitflow.py start -t hotfix critical-bugfix
```

This will start a branch `hotfix/critical-bugfix` and switch to it.


## Feature Branches

Feature branches are used to develop new features. According to the GitFlow branching
model, feature branches are created from the develop branch and merged back into the
develop branch.

To start a new feature branch, run:

```bash
./gitflow.py start -t feature new-feature
```

## Release Branches

Release branches are used to prepare a new release. According to the GitFlow branching
model, release branches are created from the develop branch and merged back into both
the main and develop branches.

To start a new release branch, run:

```bash
./gitflow.py start -t release -i "patch"
```

Should you have made last minute updates to the release branch, you can update the
release branch by merging it back into the develop branch:

```bash
./gitflow.py update
```


## Other Commands

### List All Branches

To list all branches, run:

```bash
./gitflow.py ls
```

### Checkout a Branch

To switch to a different branch using an interactive menu, run:

```bash
./gitflow.py checkout <branch_name>
```

If you do not give a branch name, you will be presented with an interactive menu.

### Add Files to Git

To add file changes to the staging area, run:

```bash
./gitflow.py add gitflow.py README.md
```

### Stash and Pop Changes

To stash changes, run:

```bash
./gitflow.py stash
```

To pop stashed changes, run:

```bash
./gitflow.py unstash
```


### Stage and Unstage Changes

```bash
./gitflow.py stage gitflow.py README.md
```

likewise,

```bash
./gitflow.py unstage gitflow.py README.md
```

### Commit Staged Changes

To commit the current changes with a specified message, run:

```bash
./gitflow.py commit -m "Updated gitflow script"
```

If you do not specify a commit message, you will be prompted to enter one,
and you'll also be able to use the AI to generate one.


### Push Changes

To push the committed changes to the remote repository, run:

```bash
./gitflow.py push feature/new-feature
```

This will optionally allow you to stage and commit all current changes.


### Fetch Changes

To fetch changes from the remote repository, run:

```bash
./gitflow.py fetch
```

### Pull Changes

To pull changes for the current branch, run:

```bash
./gitflow.py pull
```

To pull changes for all remote branches that you have locally, run:

```bash
./gitflow.py pull -a
```

### Copy a File

To copy the latest commit of a specific file from the current branch into a target branch, run:

```bash
./gitflow.py cp gitflow.py feature/new-feature
```

### Rename a Branch

To rename a branch run (if you do not specify branch names, you will get an interactive menu):

```bash
./gitflow.py mv <old_branch_name> <new_branch_name>
```

### Delete a Branch

To delete a branch using an interactive menu, run:

```bash
./gitflow.py rm <branch_name>
```

Use the `-a` option to delete the branch both from local and remote. If the branch was
not fully merged, you are going to receive an error. You can force the deletion using
the `-f` option.


## Merge Operations

### Merge a Branch

To merge a branch into the current branch, run:

```bash
./gitflow.py merge <branch_name>
```

### Merge a Branch into Another Branch

To merge a branch into another branch, run:

```bash
./gitflow.py merge <source_branch> <target_branch>
```

## AI Options

The script also provides options to configure the OpenAI API key and use it to generate
documentation for the script.

### Use AI to generate commit messages

Whenever you would use the -m option to pass in a message, you can alternatively
also not do that and then be asked whether you want to use the AI to generate a
commit message for you.

### Explain Commits or Files

To explain a commit or a file, run:

```bash
./gitflow.py explain --commit <commit_hash>
```

To explain changes between two commits, run

```bash
./gitflow.py explain --start <commit_hash1> --end <commit_hash2>
```

Any explanations of commits can be further refined by adding

- `-d` To get the number of days in the past to parse
- `--daily` to get a daily summary of the commits of those days

To explain a file or a set of files, you can run:

```bash
./gitflow.py explain <file_names relative to the git root>
```

When explaining a file, you can also specify the `--improve` option to receive
feedback about what you could improve in the file; adding `--examples` will
provide examples of how to improve the file.

All explanations can be further improved by adding the `--prompt` option, which,
followed by a prompt that you specify, will refine the explanations further.

Alternatively, you can also just get a summary of what the file does by adding
the `--summary` option.


## Document the script

To re-create the documentation and write it to the output file, run:

```bash
./gitflow.py doc
```

## Issue Operations

Github lacks the ability to clone issues. Hence here two commands that can come
in handy:

### Clone an Issue

```bash
./gitflow.py clone-issue 245 -A --title "New Issue Title"
```


### List Issues

```bash
./gitflow.py list-issues
```

# License

This script is released under the [WTFPL License](https://en.wikipedia.org/wiki/WTFPL).

## get_current_week_tag

Generate a tag for the current week.

## get_next_semver

Generate the next Semantic Versioning (SemVer) tag.

## config_ai

Configure, update, create, delete, clone an AI provider interactively, or set the default provider.

For reference, here is a typical configuration for GPT and Claude:

```ini

name = openai
aiprovider = true
apikey = sk-proj-...
model = gpt-4o
url = https://api.openai.com/v1/chat/completions
header = {Authorization: Bearer {api_key}}
response = response.json()['choices'][0]['message']['content']


name = Claude
aiprovider = true
apikey = sk-ant-...
model = claude-3-5-sonnet-20240620
url = https://api.anthropic.com/v1/messages
header = {x-api-key: {api_key}, anthropic-version: 2023-06-01}
response = response.json()['content'][0]['text']
```

## config

Configure Git and GitHub settings.

Prompts for username, token, email, name, and host if not provided via CLI options.

## start

Start a new feature, hotfix, or release branch.

If a name is provided, create a feature, hotfix, or release branch.
Otherwise, create a weekly update hotfix branch.

Parameters:
- name       : The name of the feature, hotfix, or release branch. Optional for hotfix branches.
- branch_type: The type of branch to create ('local', 'hotfix', 'feature', or 'release').
- week       : The calendar week for a weekly hotfix branch.
- increment  : The version increment type for release branches ('major', 'minor', or 'patch').
- message    : An optional commit message.
- skip_switch: Whether to skip switching to the main or develop branch before creating the new branch. True is assumed for -t backup.

## finish

Finish the current feature, hotfix, or release branch by creating pull requests for main and/or develop.
Must be run from the branch that is being finished.

## weekly_update

Pull changes from the weekly-updates branch, commit any new changes, push them, and then merge them into develop and main branches.

Parameters:
- message: An optional commit message for the merge commits.
- body   : An optional commit message body for the merge commits.

Examples:
- Pull changes, commit, push, and merge them:
    ./gitflow.py weekly_update -m "Merging weekly updates"
- Pull changes, commit with a message body, push, and merge them:
    ./gitflow.py weekly_update -m "Merging weekly updates" -b "This includes documentation updates from the team."

## cds_update

Sync changes from the remote tenantcleanup-cds repository to a specified local path, then create pull requests for main and develop branches.

This command will:
1. Clone or update the remote tenantcleanup-cds repository
2. Switch to a branch named after the local path in the current repository
3. Copy contents from the remote repository to the specified local directory
4. Commit and push the changes
5. Create pull requests to merge changes into main and develop branches

Parameters:
- remote : The URL of the remote tenantcleanup-cds repository (default: https://github.wdf.sap.corp/I052341/tenantcleanup-cds)
- local  : The local path where cds-views content will be synced (default: cds-views)
- message: An optional commit message for the sync commit
- body   : An optional commit message body for the sync commit

Example:
./gitflow.py cds_update --remote https://github.wdf.sap.corp/I052341/tenantcleanup-cds --local cds-views -m "Sync CDS views" -b "Update views from tenantcleanup-cds"

## update

Update the current release branch and merge it back into the develop branch.
Must be run from the release branch that is being updated.

## ls

List all branches, including both local and remote.

Examples:
- List all branches:
    ./gitflow.py ls

## checkout

Switch to a different branch or revert changes in files/directories.

Examples:
- Switch to a different branch interactively:
    ./gitflow.py checkout
- Switch to a specific branch:
    ./gitflow.py checkout develop
- Revert changes in a file:
    ./gitflow.py checkout -- filename.txt
- Revert all changes in the current directory:
    ./gitflow.py checkout .
- Force checkout to a branch, discarding local changes:
    ./gitflow.py checkout develop -f

## rm

Delete one or more branches using an interactive menu or by specifying the branch names.

## mv

Rename a branch locally and/or remotely.

Parameters:
- old_name: The current name of the branch to rename.
- new_name: The new name for the branch.
- all     : Rename both local and remote branches.

Examples:
- Rename a branch interactively:
    ./gitflow.py mv
- Rename a specific branch:
    ./gitflow.py mv old-feature-name new-feature-name
- Rename both local and remote branches:
    ./gitflow.py mv old-feature-name new-feature-name -a

## add

Add file changes to the staging area.

Parameters:
- file_paths: The path(s) to the file(s) to add. If not specified, you can use the --all option to add all changes.
- all       : Add changes from all tracked and untracked files.
- force     : Allow adding otherwise ignored files.

Examples:
- Add a single file:
    ./gitflow.py add gitflow.py
- Add multiple files:
    ./gitflow.py add gitflow.py README.md
- Add all changes:
    ./gitflow.py add --all
- Add a file that is ignored:
    ./gitflow.py add --force ignored_file.txt

## stage

Stage changes for the next commit.

Examples:
- Stage all changes          : ./gitflow.py stage --all
- Stage specific files       : ./gitflow.py stage file1.py file2.py
- Use interactive staging    : ./gitflow.py stage --interactive

## unstage

Unstage changes from the staging area.

Examples:
- Unstage all changes        : ./gitflow.py unstage --all
- Unstage specific files     : ./gitflow.py unstage file1.py file2.py
- Use interactive unstaging  : ./gitflow.py unstage --interactive

## stash

Stash changes in the working directory.

Examples:
- Stash changes                   : ./gitflow.py stash
- Stash changes with a message    : ./gitflow.py stash -m "Work in progress"
- Stash including untracked files : ./gitflow.py stash --untracked
- List all stashes                : ./gitflow.py stash --list
- Show changes in a stash         : ./gitflow.py stash --show stash@{0}
- Drop a stash                    : ./gitflow.py stash --drop stash@{0}
- Clear all stashes               : ./gitflow.py stash --clear

## unstash

Apply and remove a stash (pop), or just apply it.

Examples:
- Pop the latest stash                      : ./gitflow.py unstash
- Apply the latest stash without removing it: ./gitflow.py unstash --apply
- Pop a specific stash                      : ./gitflow.py unstash stash@{0}
- Apply a specific stash without removing it: ./gitflow.py unstash --apply stash@{0}
- Interactively select a stash to pop       : ./gitflow.py unstash --interactive
- Interactively select a stash to apply     : ./gitflow.py unstash --interactive --apply

## commit

Commit the current changes with a specified message and optional body.

Parameters:
- message    : The commit message.
- body       : The commit message body.
- add_all    : Add all changes before committing.
- interactive: Use interactive mode for commit message.
- files      : Files or directories to commit.

Examples:
- Commit the current changes:
    ./gitflow.py commit -m "Updated gitflow script"
- Commit with a message and body:
    ./gitflow.py commit -m "Updated gitflow script" -b "This includes changes to improve performance and readability."
- Add all changes and commit:
    ./gitflow.py commit -m "Updated gitflow script" --all
- Commit specific files:
    ./gitflow.py commit -m "Updated gitflow script" README.md script.py
- Use interactive mode:
    ./gitflow.py commit -i

## split_message_body

Splits the commit message body at the 72nd character, avoiding word splits.

## explain

Generate an explanation using AI based on changes between two commits, the current state, or file history.

This command will:
1. Get the diff between two specified commits, the current state, or file history
2. Send to an AI model for analysis
3. Generate an explanation or commit message body

Examples:
- Generate an explanation for current changes:
    ./gitflow.py explain
- Generate an explanation for a given commit
    ./gitflow.py explain --commit def456
- Generate an explanation for changes between two commits:
    ./gitflow.py explain --start abc123 --end def456
- Explain the history of specific files:
    ./gitflow.py explain path/to/file1.py path/to/file2.py
- Explain the relevance of specific files:
    ./gitflow.py explain path/to/file1.py path/to/file2.py --summary
- Explain the history of specific files for the last 30 days:
    ./gitflow.py explain path/to/file1.py path/to/file2.py -d 30
- Explain the daily summary of files for the last 30 days:
    ./gitflow.py explain path/to/file1.py path/to/file2.py -d 30 --daily
- Provide improvement suggestions for files:
    ./gitflow.py explain path/to/file1.py path/to/file2.py --improve
- Provide improvement suggestions with code examples:
    ./gitflow.py explain path/to/file1.py path/to/file2.py --improve --examples
- Use a custom prompt addition:
    ./gitflow.py explain path/to/file1.py --prompt "Focus on performance improvements"

## fetch

Fetch changes from the remote repository.

Parameters:
- remote     : The name of the remote to fetch from (default is 'origin').
- branch     : Specific branch to fetch.
- prune      : Prune deleted branches from the remote repository.
- all_remotes: Fetch changes from all remotes.

Examples:
- Fetch changes from the default remote:
    ./gitflow.py fetch
- Fetch changes from a specific remote:
    ./gitflow.py fetch origin
- Fetch a specific branch:
    ./gitflow.py fetch --branch main
- Prune deleted branches:
    ./gitflow.py fetch -p
- Fetch changes from all remotes:
    ./gitflow.py fetch -a

## merge

Merge one local branch into another.

Parameters:
- source: The source branch to merge from. If not specified, the current branch will be used.
- target: The target branch to merge into. If not specified, will be prompted.
- squash: Squash commits when merging.
- no_ff : Create a merge commit even when fast-forward is possible (default: True).

Examples:
- Merge current branch into main:
    ./gitflow.py merge main
- Merge feature branch into develop with squash:
    ./gitflow.py merge feature/new-feature develop --squash
- Merge release branch into main with fast-forward:
    ./gitflow.py merge release/v1.0 main --no-ff=false

## push

Push the committed changes to the remote repository. If the branch is protected, create a pull request.

Parameters:
- branch   : The branch to push changes to. If not specified, the current branch will be used.
- force    : Force push the changes.
- create_pr: Create a pull request instead of pushing directly.

Examples:
- Push changes to the current branch:
    ./gitflow.py push
- Force push changes to a specific branch:
    ./gitflow.py push feature/new-feature -f
- Create a pull request instead of pushing:
    ./gitflow.py push -p

## pull

Pull changes from a remote repository.

Examples:
- Pull from origin:
    ./gitflow.py pull
- Pull from a specific remote:
    ./gitflow.py pull --remote upstream
- Pull a specific branch:
    ./gitflow.py pull --branch feature/new-feature
- Pull with rebase:
    ./gitflow.py pull --rebase
- Pull all branches:
    ./gitflow.py pull --all
- Pull and prune:
    ./gitflow.py pull --prune

## status

Display a concise status of the current Git repository in a single, comprehensive table.

## compare

Compare the same file in two different branches.

Parameters:
- file_path: The path to the file to compare.
- branch1  : The first branch to compare.
- branch2  : The second branch to compare.

Examples:
- Compare a file interactively:
    ./gitflow.py compare gitflow.py
- Compare a file directly:
    ./gitflow.py compare gitflow.py develop feature/new-feature

## cp

Copy the latest commit of a specific file from the current branch into one or more target branches.

Parameters:
- file_path     : The path to the file to copy the latest commit for.
- target_branches: The target branch(es) to copy into. If not provided, you'll be prompted to select.
- push          : Push the changes to the remote repository after copying if the remote branch exists.
- create_pr     : Create a pull request instead of pushing directly.

Examples:
- Copy the latest commit of gitflow.py into a feature branch:
    ./gitflow.py cp gitflow.py feature/new-feature --push
- Copy into multiple branches:
    ./gitflow.py cp gitflow.py feature/branch1 feature/branch2 main
- Copy and create pull requests:
    ./gitflow.py cp gitflow.py main develop --pr

## list_issues

List GitHub issues with optional filtering, sorting, and configurable columns.

Available columns: number, title, state, labels, createdAt, updatedAt, author, assignees, comments, body, closed, closedAt, url

Default columns: number, state, labels, updatedAt, author, title, url

Examples:
- List issues with default columns:
    gf list-issues
- List all issues with custom columns:
    gf list-issues -c number -c title -c state -c labels -c author
- List all issues (open and closed) sorted by creation date:
    gf list-issues --state all --order-by created
- Use login instead of name for author and assignees:
    gf list-issues --use-login
- Search issues with a regex for not containing a colon:
    gf list-issues --search '!:' -R
- List open issues related to "bug" with involved filter:
    gf list-issues --search "bug" --involved --state open
- Search issues with plain text:
    gf list-issues --search "Tenants with Issues"

## clone_issue

Clone an existing issue, creating a new issue with the same metadata and comments.

Parameters:
- issue_number    : The number of the issue to clone.
- empty_checkboxes: Whether to empty checkboxes in the description (default: True).
- replace         : String or regex pattern to replace in the title.
- with_str        : String to replace with in the title.
- regex           : Use regex for string replacement in title.
- new_title       : Replace the entire title with a new one.
- keep_assignees  : Keep the original assignees (default: False).
- assignees       : List of assignees to add to the new issue.

Examples:
- Clone issue #245 and empty checkboxes:
    ./gitflow.py clone-issue 245
- Clone issue #245, keep checkboxes, and replace 'CW35' with 'CW36' in the title:
    ./gitflow.py clone-issue 245 --keep-checkboxes --search "CW35" --replace "CW36"
- Use regex to replace 'CW' followed by any digits with 'CW36' in the title:
    ./gitflow.py clone-issue 245 --search "CW[0-9]+" --replace "CW36"
- Clone issue #245 with a completely new title:
    ./gitflow.py clone-issue 245 --title "New Issue Title"
- Clone issue #245 and remove the original assignees, assign to self, and give a new title:
    ./gitflow.py clone-issue 245 -A -a @me --title "New Issue Title"
    ./gitflow.py clone-issue 245 -A --title "New Issue Title"
- Clone issue #245 and assign it to specific users:
    ./gitflow.py clone-issue 245 --assignee user1 --assignee user2

## doc

Re-create the documentation and write it to the output file.

This command generates documentation for the script, including an optional
table of contents and custom title.


