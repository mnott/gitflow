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

## Issue Operations

Github lacks the ability to clone issues. Hence here two commands that can come
in handy:

### Clone an Issue

```bash
./gitflow.py clone-issue 245 -A --title "New Issue Title"
```

### List and Manage Issues

```bash
# List all issues matching a pattern
gf manage-issues -l --search "Manual Imports" --regex

# List only open issues matching a pattern
gf manage-issues -l --search "Manual Imports" -c open --regex

# Close all open issues matching a pattern
gf manage-issues --search "Manual Imports: CW3\d" -s closed -c open --regex

# Open all closed issues matching a pattern
gf manage-issues --search "Manual Imports: CW0[1-3]" -s open -c closed --regex

# Rename issues (with preview)
gf manage-issues --search "Manual Imports : CW" --rename "Manual Imports: CW" --regex-rename --dry-run

# Actually perform the rename
gf manage-issues --search "Manual Imports : CW" --rename "Manual Imports: CW" --regex-rename

# Use regex groups in rename
gf manage-issues --search "Manual Imports: CW(\d)\b" --rename "Manual Imports: CW0\1" --regex-rename
```

The regex patterns follow Python's re module syntax. Some useful patterns:
- `\d` matches any digit
- `\b` matches a word boundary
- `[0-9]` matches any digit
- `[1-3]` matches digits 1 through 3
- `(\d)` captures a digit into group 1, referenced as `\1` in replace pattern
- `.*` matches any characters
- `^` matches start of line
- `$` matches end of line

### Manage Labels

```bash
# List all repository labels
gf manage-labels --list

# Preview creating new labels
gf manage-labels -c "bug:ff0000:Bug reports" -c "feature:00ff00" --dry-run

# Create new labels
gf manage-labels -c "bug:ff0000:Bug reports" -c "feature:00ff00"

# Preview renaming a label
gf manage-labels --rename "old-name:new-name" --dry-run

# Rename a label
gf manage-labels --rename "old-name:new-name"

# Preview deleting labels
gf manage-labels --delete old-label --dry-run

# Delete labels
gf manage-labels --delete old-label

# Preview adding/removing labels for matching issues
gf manage-labels --search "Manual Imports" --regex -r old-label -a new-label --dry-run

# Add/remove labels for matching issues
gf manage-labels --search "Manual Imports" --regex -r old-label -a new-label
```

The regex patterns follow Python's re module syntax. Some useful patterns:
- `\d` matches any digit
- `\b` matches a word boundary
- `[0-9]` matches any digit
- `[1-3]` matches digits 1 through 3
- `(\d)` captures a digit into group 1, referenced as `\1` in replace pattern
- `.*` matches any characters
- `^` matches start of line
- `$` matches end of line


## Document the script

To re-create the documentation and write it to the output file, run:

```bash
./gitflow.py doc
```

# GitFlow Version System

The GitFlow tool maintains two version numbers:

1. **Repository Version** (`.version` file)
   - Stored in the `.version` file at the root of each repository
   - Updated during release branch operations
   - Represents the current version of the repository
   - Used as the source of truth for version numbers

2. **GitFlow Version** (`__version__` in gitflow.py)
   - Stored in `gitflow.py` as `__version__` variable
   - Only updated when in the actual gitflow repository
   - Shown when running `gf -v`
   - Represents the version of the GitFlow tool itself

## Version Update Process

When running `gf finish` on a release branch:

1. The version is extracted from the release branch name (e.g., `release/v1.8.40` → `1.8.40`)
2. The `.version` file is updated with this version number
3. If in the gitflow repository (detected by presence of `client/gitwrapper.py` and other files), `__version__` in `gitflow.py` is also 
updated
4. Changes are committed and merged into `main` and `develop`

This means:
- In the gitflow repository: both `.version` and `gitflow.py` get updated
- In other repositories: only `.version` gets updated
- `gf -v` shows both versions for clarity


## Reverting Changes

The revert functionality provides a comprehensive solution for undoing changes in GitFlow-managed
repositories. This is particularly useful for reverting merged pull requests that may have
introduced bugs or unwanted changes.

### Understanding Git Revert vs Reset

Git revert creates new commits that undo previous changes, preserving history. This is safer
than git reset which modifies history. The revert command is particularly powerful for handling
merge commits in GitFlow workflows.

### Basic Revert Operations

#### Revert a Single Commit

```bash
# Revert a specific commit on the current branch
gf revert abc123

# Revert with dry-run to see what would happen
gf revert abc123 --dry-run

# Revert on all branches containing the commit
gf revert abc123 --all-branches
```

#### Interactive Revert

```bash
# Interactively select which branches to revert on
gf revert abc123 --interactive
```

### Advanced Revert Scenarios

#### Latest PR/Merge Revert

One of the most common use cases is reverting the latest merged PR:

```bash
# Automatically find and revert the latest merge commits on main and develop
gf revert --latest
```

This command:
- Scans main and develop branches for the most recent merge commits
- Shows you what will be reverted with commit details and source branch info
- Handles the different commit hashes that result from the same PR being merged into both branches

#### Related Merge Commits

When the same feature branch is merged into both main and develop (common in GitFlow),
you get different commit hashes for what is logically the same change:

```bash
# Find and revert all merge commits from the same source branch
gf revert abc123 --related
```

This automatically:
- Detects the source branch that was merged
- Finds all merge commits across branches that merged this source branch
- Reverts them appropriately on each branch

#### PR-Based Revert

```bash
# Revert all merge commits associated with a specific PR number
gf revert --pr-number 123

# Revert all merge commits from a specific source branch
gf revert --source-branch feature/new-ui
```

### Merge Commit Handling

Merge commits have multiple parents, and you need to specify which parent to revert to:

```bash
# Explicitly specify parent (1 = target branch, 2 = source branch)
gf revert abc123 --parent 1

# For most GitFlow merges, parent 1 (default) is correct
gf revert abc123  # Uses parent 1 automatically for merge commits
```

The tool automatically detects merge commits and:
- Shows parent commit information
- Uses parent 1 by default (reverts to the target branch state)
- Provides clear feedback about which parent is being used

### Safety Features

#### Conflict Detection

```bash
# Check for conflicts before making changes
gf revert abc123 --all-branches --dry-run
```

The dry-run mode:
- Tests if revert would create conflicts on each branch
- Shows a detailed plan of what would happen
- Displays conflicts that would occur
- Lets you make informed decisions before proceeding

#### Force Mode

```bash
# Skip branches with conflicts, revert only clean branches
gf revert abc123 --all-branches --force
```

### Branch Management

#### Multi-Branch Operations

```bash
# Revert on specific branches only
gf revert abc123 --branch main --branch develop

# Revert on all branches containing the commit
gf revert abc123 --all-branches
```

#### Pull Request vs Direct Push

```bash
# Create pull requests instead of pushing directly (safer for protected branches)
gf revert abc123 --all-branches --pr

# Don't push changes, just make local reverts
gf revert abc123 --no-push
```

### Real-World Examples

#### Emergency Hotfix Revert

```bash
# Someone merged a hotfix that broke production
# Find and revert the latest merge across all branches
gf revert --latest --dry-run  # Check what would happen
gf revert --latest --pr       # Create PRs for review
```

#### Feature Rollback

```bash
# A feature was merged but needs to be rolled back
# Revert PR #456 across all affected branches
gf revert --pr-number 456 --dry-run
gf revert --pr-number 456 --all-branches
```

#### Selective Branch Revert

```bash
# Only revert on main, not develop (maybe develop needs the change)
gf revert abc123 --branch main
```

### Integration with GitFlow

The revert command integrates seamlessly with GitFlow workflows:

1. **Automatic Branch Detection**: Understands GitFlow branch relationships
2. **Merge Commit Intelligence**: Handles the complexity of merge commits in GitFlow
3. **Related Commit Finding**: Knows that the same logical change creates different commits on main/develop
4. **Safe Operations**: Provides dry-run and conflict detection to prevent issues
5. **PR Integration**: Can create pull requests for protected branch workflows

### Safety Best Practices

1. **Always dry-run first** for complex operations:
   ```bash
   gf revert --latest --dry-run
   ```

2. **Use PR mode** for protected branches:
   ```bash
   gf revert abc123 --all-branches --pr
   ```

3. **Check related commits** when dealing with GitFlow merges:
   ```bash
   gf revert abc123 --related --dry-run
   ```

4. **Test on single branch first** if unsure:
   ```bash
   gf revert abc123 --branch develop
   ```

The revert functionality transforms a typically complex and error-prone operation into
a safe, intelligent process that understands GitFlow workflows and prevents common mistakes.


