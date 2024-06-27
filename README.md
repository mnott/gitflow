# gf

# Gitflow: A Git Wrapper for Release and Branch Management


This script is a simple Git wrapper for managing feature, hotfix, and release branches.
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

# Usage

To get help about the script, call it with the `--help` option:

```bash
./gitflow.py --help
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

#### Start a Weekly Update Hotfix Branch

To start a new weekly update hotfix branch, run:

```bash
./gitflow.py start
```

#### Finish a Weekly Update Hotfix Branch

To finish a weekly update hotfix branch, run:

```bash
./gitflow.py finish
```


### Hotfix Branches

#### Start a Hotfix Branch

To start a new hotfix branch, run:

```bash
./gitflow.py start -t hotfix -n "critical-bugfix" -m "Starting critical bugfix hotfix"
```

#### Finish a Hotfix Branch

To finish a hotfix branch, run:

```bash
./gitflow.py finish -t hotfix -n "critical-bugfix" -m "Finishing critical bugfix hotfix"
```

In case you have a release branch open, you can specify the target branch to merge the
hotfix into:

```bash
./gitflow.py finish -t hotfix -n "critical-bugfix" -m "Finishing critical bugfix hotfix" -tb "release/v1.4.5"
```


## Feature Branches

Feature branches are used to develop new features. According to the GitFlow branching
model, feature branches are created from the develop branch and merged back into the
develop branch.

### Start a Feature Branch

To start a new feature branch, run:

```bash
./gitflow.py start -t feature -n "new-feature" -m "Starting new feature"
```

### Finish a Feature Branch

To finish a feature branch, run:

```bash
./gitflow.py finish -t feature -n "new-feature" -m "Finishing new feature"
```


## Release Branches

Release branches are used to prepare a new release. According to the GitFlow branching
model, release branches are created from the develop branch and merged back into both
the main and develop branches.

### Start a Release Branch

To start a new release branch, run:

```bash
./gitflow.py start -t release -m "Starting release" -i "patch"
```

### Finish a Release Branch

To finish a release branch, run:

```bash
./gitflow.py finish -t release -n "v1.4.5" -m "Finishing release"
```

Should you have made last minute updates to the release branch, you can update the
release branch by merging it back into the develop branch:

```bash
./gitflow.py update -n "1.2.0" -m "Merging bug fixes from release 1.2.0"
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
./gitflow.py checkout
```

### Add Files to Git

To add file changes to the staging area, run:

```bash
./gitflow.py add gitflow.py README.md
```

### Commit Changes

To commit the current changes with a specified message, run:

```bash
./gitflow.py commit -m "Updated gitflow script"
```

### Push Changes

To push the committed changes to the remote repository, run:

```bash
./gitflow.py push feature/new-feature
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

### Delete a Branch

To delete a branch using an interactive menu, run:

```bash
./gitflow.py rm
```


### Document the script

To re-create the documentation and write it to the output file, run:

```bash
./gitflow.py doc
```


# License

This script is released under the WTFP License.
