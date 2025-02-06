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


## Worktree Operations

Git worktrees allow you to have multiple working directories connected to the same repository.
This is useful for working on multiple branches simultaneously without constantly switching.

Imagine you're working on a big feature in feature/dashboard5 and suddenly your team reports
a critical bug in production that needs immediate attention. Without worktrees, you'd need to:

1. Stash or commit your half-done dashboard work
2. Switch to the hotfix branch
3. Fix the bug
4. Switch back to your feature
5. Remember where you were with your work

With worktrees, instead you can:

1. Keep your dashboard work exactly as is in your worktree
2. In your main repository, create and checkout a hotfix branch
3. Fix the bug
4. Submit the fix
5. Return to your dashboard work in the worktree - everything is exactly as you left it

Another common use case is when you need to run two versions of your code simultaneously -
like comparing how your app behaves before and after your changes, or running tests on
two different branches at once.

But if you're not encountering these scenarios, and branch switching isn't causing you pain,
then worktrees might be adding unnecessary complexity to your workflow. Git worktrees are a
power tool - helpful in specific situations but not something everyone needs for daily work.

Worktrees are best used as a temporary solution for specific situations, not as your
default way of working. Here's a sensible approach:

Do most of your daily work in your main repository directory, using normal branch switching
Create a worktree only when you have a specific need, like:

- When you need to work on an urgent fix while keeping your current work intact
- When you need to run two versions of your code side by side
- When you're reviewing a complex PR and want to run it alongside your current work

Then, once you're done with that specific task, you can remove the worktree and go back
to your normal workflow. Think of worktrees like a spare workbench - you don't need it
for every task, but it's very helpful when you need to work on two things
at once without mixing them up.

### Create a Worktree

To create a new worktree for an existing branch or create a new branch on the fly:

```bash
./gitflow.py worktree add feature/test ../tc-worktrees/dashboard5
```


### Switch Between Worktrees

For this to work, it makes sense to have this in your `~/.bashrc` or `~/.zshrc`:

```bash
# Git worktree navigation
function cdworktree() {
    local branch="$1"
    if [[ -z "$branch" ]]; then
        echo "Usage: cdworktree <branch-name>"
        return 1
    fi

    # Get all output first to avoid multiple calls
    local all_output=$(gf ls --format plain 2>/dev/null)

    # First try to find a worktree for the requested branch
    local line=$(echo "$all_output" | grep -F "$branch" | head -n1)
    local worktree_path=$(echo "$line" | grep -o '<[^>]*>' | sed 's/^<\(.*\)>$/\1/')

    if [[ -n "$worktree_path" && -d "$worktree_path" ]]; then
        cd "$worktree_path"
        return
    fi

    # If no worktree found for the branch, try to find the main repository
    # Look for the current branch's worktree
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    local main_repo=$(echo "$all_output" | grep -F "$current_branch" | grep -o '<[^>]*>' | sed 's/^<\(.*\)>$/\1/')

    # Verify the branch exists
    if git rev-parse --verify "$branch" >/dev/null 2>&1; then
        if [[ -n "$main_repo" && -d "$main_repo" ]]; then
            if [[ "$PWD" != "$main_repo" ]]; then
                cd "$main_repo"
                echo "Note: '$branch' is not in a worktree, changing to main repository at $main_repo"
            fi
        else
            echo "Could not determine main repository location"
            return 1
        fi
    else
        echo "No worktree or branch found for '$branch'"
        return 1
    fi
}
```

To switch to an existing worktree's directory:

```bash
cdworktree feature/test
```

### List Worktrees

To list all worktrees and their locations:

```bash
./gitflow.py worktree ls
```

### Remove a Worktree

To safely remove a worktree and clean up its branch:

```bash
./gitflow.py worktree rm feature/test
```

### Sample Workflow

First, we create a new worktree for the feature branch (if
the branch already exists, it will be added to that worktree):

```bash
./gitflow.py worktree add feature/test ../tc-worktrees/test
```

Then, we cd into the worktree and start working on the feature:

```bash
cdworktree feature/test
```

When we are finished, we can finish the branch right
from here, or we can push the branch to the remote.
We could at some point also just decide to remove the
worktree:

```bash
./gitflow.py worktree rm feature/test
```

Note that if you finish or remove a worktree while you are
in it, you will not be moved back to the main repository, but
you will be shown a message to that effect.


# License

This script is released under the [WTFPL License](https://en.wikipedia.org/wiki/WTFPL).


