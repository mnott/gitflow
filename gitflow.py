#!/usr/bin/env python3
# encoding: utf-8

r"""
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

To commit changes before finishing:

```bash
./gitflow.py finish -m "Complete feature implementation"
```

For multi-paragraph commit messages, you can use multiple `-m` options:

```bash
./gitflow.py finish -m "Complete user dashboard" -m "Added charts and analytics" -m "Improved responsive design"
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

For multi-paragraph commit messages, you can use multiple `-m` options:

```bash
./gitflow.py commit -m "Fix authentication bug" -m "Updated login validation" -m "Added comprehensive error handling"
```

If you do not specify a commit message, you will be prompted to enter one,
and you'll also be able to use the AI to generate one.


### Push Changes

To push the committed changes to the remote repository, run:

```bash
./gitflow.py push feature/new-feature
```

To commit and push changes with a message in one step:

```bash
./gitflow.py push -m "Deploy new feature"
```

For multi-paragraph commit messages, you can use multiple `-m` options:

```bash
./gitflow.py push -m "Deploy new feature" -m "Includes performance improvements" -m "Added comprehensive error handling"
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
3. If in the gitflow repository (detected by presence of `client/gitwrapper.py` and other files), `__version__` in `gitflow.py` is also updated
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


"""

__version__ = "1.0.23"

from collections import defaultdict
from datetime import datetime, timedelta
from git import Repo, GitCommandError
from InquirerPy import inquirer
from rich import box, pretty, print, traceback
from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing import List, Optional
import glob
import math
import json
import os
import pytz
import re
import shutil
import subprocess
import typer
import typer
import urllib.parse

import json
import re

import tempfile
import subprocess
import os
import time
from pathlib import Path

# Local imports
from client import AIClient, GitConfig, DocGenerator, GitWrapper
from client.issuedoc import IssueDocGenerator

pretty.install()
traceback.install()
console = Console()


app = typer.Typer(
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="GitFlow: A Git Wrapper for Release and Branch Management",
    epilog="To get help about the script, call it with the --help option."
)

def version_callback(value: bool):
    if value:
        git = GitWrapper()
        gitflow_version, repo_version = git.get_version_info()
        console.print(f"GitFlow    version: {gitflow_version or 'unknown'}")
        if repo_version:
            console.print(f"Repository version: {repo_version}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v",
        help="Show the version and exit",
        callback=version_callback,
        is_eager=True
    )
):
    """GitFlow - A tool for managing Git workflows."""
    pass

# Initialize the GitWrapper
git_wrapper = GitWrapper()

# Get the repository root directory
repo_root = git_wrapper.get_repo_root()

# Change the working directory to the repository root
os.chdir(repo_root)


# Get the current week tag
def get_current_week_tag(prefix: str = "cw-") -> str:
    """Generate a tag for the current week."""
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]
    current_tag = f"{prefix}{current_year}-{current_week:02}"
    return current_tag


# Get the next Semantic Versioning (SemVer) tag
def get_next_semver(increment: str, existing_tags: List[str]) -> str:
    """Generate the next Semantic Versioning (SemVer) tag."""
    if not existing_tags:
        return "v1.0.0"

    existing_tags.sort()
    latest_tag = existing_tags[-1]
    major, minor, patch = map(int, latest_tag[1:].split('.'))

    while True:
        if increment == "major":
            major += 1
            minor = 0
            patch = 0
        elif increment == "minor":
            minor += 1
            patch = 0
        elif increment == "patch":
            patch += 1

        new_tag = f"v{major}.{minor}.{patch}"
        if new_tag not in existing_tags:
            return new_tag



# Check for Branch Differences
def has_differences(base_branch: str, compare_branch: str):
    if not git_wrapper.check_network_connection():
        console.print("[yellow]Warning: No network connection. Unable to fetch latest changes.[/yellow]")
        console.print("[yellow]Proceeding with local comparison.[/yellow]")
        try:
            # Use local refs for comparison
            merge_base = git_wrapper.merge_base(base_branch, compare_branch)
            diff = git_wrapper.get_diff(f'{merge_base}..{compare_branch}')
            return bool(diff.strip())
        except GitCommandError as e:
            console.print(f"[yellow]Warning: Error checking local differences: {e}[/yellow]")
            return True  # Assume there are differences if we can't check

    try:
        # Use our custom fetch function to fetch the specific base branch
        fetch(remote="origin", branch=base_branch, prune=False, all_remotes=False)

        # Now we can use the fetched remote branch
        merge_base = git_wrapper.merge_base(f'origin/{base_branch}', compare_branch)
        diff = git_wrapper.get_diff(f'{merge_base}..{compare_branch}')
        return bool(diff.strip())
    except GitCommandError as e:
        console.print(f"[yellow]Warning: Error checking differences with {base_branch}: {e}[/yellow]")
        return True  # Assume there are differences if we can't check


# Create pull requests
def create_pull_request(base_branch: str, branch_name: str, branch_type: str):
    force_create = branch_type == "release"
    console.print(f"[blue]Checking differences between {base_branch} and {branch_name}[/blue]")
    if has_differences(base_branch, branch_name) or force_create:
        try:
            console.print(f"[blue]Attempting to create pull request from {branch_name} to {base_branch}[/blue]")
            result = subprocess.run(
                ["gh", "pr", "create", "--base", base_branch, "--head", branch_name,
                    "--title", f"Merge {branch_name} into {base_branch}",
                    "--body", f"Merge {branch_type} {branch_name} into {base_branch}"],
                capture_output=True, text=True, check=True
            )
            console.print(f"[green]Created pull request to merge {branch_name} into {base_branch}[/green]")
            return True
        except subprocess.CalledProcessError as e:
            if "A pull request for branch" in e.stderr:
                console.print(f"[yellow]A pull request already exists for {branch_name} into {base_branch}[/yellow]")
                return True
            elif "No commits between" in e.stderr:
                console.print(f"[yellow]No commits between {branch_name} and {base_branch}. No pull request created.[/yellow]")
                return False
            else:
                console.print(f"[red]Error creating pull request: {e.stderr}[/red]")
                return False
    else:
        console.print(f"[yellow]No differences found between {branch_name} and {base_branch}. Skipping pull request creation.[/yellow]")
        return False




#
# Configure the API Key and Model
#
@app.command()
def config_ai(
    provider:     Optional[str] = typer.Argument(None,                          help="The AI provider to configure"),
    set_default:           bool = typer.Option  (False,  "-d", "--set-default", help="Set the specified provider as default")
):
    """
    Configure, update, create, delete, clone an AI provider interactively, or set the default provider.

    For reference, here is a typical configuration for GPT and Claude:

    ```ini
    [openai]
    name = openai
    aiprovider = true
    apikey = sk-proj-...
    model = gpt-4o
    url = https://api.openai.com/v1/chat/completions
    header = {Authorization: Bearer {api_key}}
    response = response.json()['choices'][0]['message']['content']

    [claude]
    name = Claude
    aiprovider = true
    apikey = sk-ant-...
    model = claude-3-5-sonnet-20240620
    url = https://api.anthropic.com/v1/messages
    header = {x-api-key: {api_key}, anthropic-version: 2023-06-01}
    response = response.json()['content'][0]['text']
    ```

    """
    git_config = GitConfig()
    available_providers = git_config.get_available_providers()

    if set_default:
        if provider:
            if provider in available_providers:
                git_config.set_default_provider(provider)
                console.print(f"[green]Set {provider} as the default AI provider.[/green]")
            else:
                console.print(f"[red]Provider '{provider}' not found. Cannot set as default.[/red]")
        else:
            if available_providers:
                default_provider = inquirer.select(
                    message="Select the default AI provider:",
                    choices=available_providers
                ).execute()
                git_config.set_default_provider(default_provider)
                console.print(f"[green]Set {default_provider} as the default AI provider.[/green]")
            else:
                console.print("[red]No AI providers found. Cannot set a default provider.[/red]")
        return

    if not available_providers and provider is None:
        console.print("[yellow]No AI providers found. Let's create one.[/yellow]")
        provider = inquirer.text(message="Enter a name for the new provider:").execute()

    if provider is None:
        choices = available_providers + ["Create new provider", "Clone existing provider", "Set default provider"]

        selected = inquirer.select(
            message="Select an action:",
            choices=choices
        ).execute()

        if selected == "Create new provider":
            provider = inquirer.text(message="Enter the name for the new provider:").execute()
        elif selected == "Clone existing provider":
            source_provider = inquirer.select(
                message="Select a provider to clone:",
                choices=available_providers
            ).execute()
            target_provider = inquirer.text(message="Enter the name for the cloned provider:").execute()
            if git_config.clone_provider(source_provider, target_provider):
                provider = target_provider
            else:
                return
        elif selected == "Set default provider":
            default_provider = inquirer.select(
                message="Select the default AI provider:",
                choices=available_providers
            ).execute()
            git_config.set_default_provider(default_provider)
            console.print(f"[green]Set {default_provider} as the default AI provider.[/green]")
            return
        else:
            provider = selected

    git_config.configure_provider(provider)

    # Ask if the user wants to set this provider as default
    if inquirer.confirm(message=f"Do you want to set {provider} as the default AI provider?", default=False).execute():
        git_config.set_default_provider(provider)
        console.print(f"[green]Set {provider} as the default AI provider.[/green]")


#
# Configure the Git Repository
#
@app.command()
def config(
    username: Optional[str] = typer.Option(None,                  "-u", "--username", help="Your GitHub username"),
    token:    Optional[str] = typer.Option(None,                  "-t", "--token",    help="Your GitHub token"),
    email:    Optional[str] = typer.Option(None,                  "-e", "--email",    help="Your email for git config"),
    name:     Optional[str] = typer.Option(None,                  "-n", "--name",     help="Your name for git config"),
    host:     Optional[str] = typer.Option("github.wdf.sap.corp", "-h", "--host",     help="GitHub host", show_default=True)
):
    """
    Configure Git and GitHub settings.

    Prompts for username, token, email, name, and host if not provided via CLI options.
    """
    if username is None:
        username = inquirer.text(message="Enter your GitHub username     :").execute()

    if token is None:
        token = inquirer.secret (message="Enter your GitHub token        :").execute()

    if email is None:
        email = inquirer.text   (message="Enter your email for git config:").execute()

    if name is None:
        name = inquirer.text    (message="Enter your name  for git config:").execute()

    host     = inquirer.text    (message="Enter the GitHub host          :", default="github.wdf.sap.corp").execute()

    # Configure Git settings
    try:
        subprocess.run(f"git config --global user.email {email}", shell=True, check=True)
        subprocess.run(f"git config --global user.name {name}", shell=True, check=True)
        console.print("[green]Git configuration updated successfully.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to configure git: {e.stderr.decode()}[/red]")
        raise typer.Exit()

    # Configure Git credentials for the host
    try:
        subprocess.run(f"git credential approve <<< 'protocol=https\nhost={host}\nusername={username}\npassword={token}'", shell=True, check=True)
        console.print("[green]Git credentials configured successfully.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to configure git credentials: {e.stderr.decode()}[/red]")
        raise typer.Exit()

    # Attempt to authenticate with GitHub
    auth_command = f"echo {token} | gh auth login -h {host} -p https --with-token"
    try:
        subprocess.run(auth_command, shell=True, check=True, capture_output=True)
        console.print("[green]Successfully authenticated with GitHub.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Authentication failed: {e.stderr.decode()}[/red]")
        raise typer.Exit()


#
# Start a new local, feature, hotfix, or release branch
#
@app.command()
def start(
    name: Optional[str] = typer.Argument(None, help="Specify the feature, local, hotfix, release, or backup name"),
    branch_type: str = typer.Option("local", "-t", "--type", help="Specify the branch type: local, hotfix, feature, release, or backup"),
    week: Optional[int] = typer.Option(None, "-w", "--week", help="Specify the calendar week"),
    increment: str = typer.Option("patch", "-i", "--increment", help="Specify the version increment type: major, minor, patch"),
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Specify a commit message"),
    skip_switch: bool = typer.Option(False, "-s", "--skip-switch", help="Skip switching to main or develop branch before creating the new branch")
):
    # Create GitWrapper instance at the start of the function
    git = GitWrapper()
    offline = not git.check_network_connection()

    if offline:
        console.print("[yellow]Network is unavailable. Operating in offline mode.[/yellow]")

    # Auto-stash if needed
    has_changes = git.is_dirty()
    if has_changes:
        git.stash('save')

    version_tag = None
    existing_tags = git.get_tags()

    if branch_type == "hotfix" and name is None:
        week_number = git.get_week_number(week)
        name = f"week-{week_number}"

    if name:
        if branch_type == "local":
            branch_name = name
        else:
            branch_name = f"{branch_type}/{name}"
    elif branch_type == "release":
        version_tag = get_next_semver(increment, existing_tags)
        print(f"Next version tag: {version_tag}")
        branch_name = f"release/{version_tag}"
    else:
        console.print("[red]Error: A feature or release branch must have a name[/red]")
        return

    if branch_type == "backup":
        skip_switch = True

    base_branch = 'main' if branch_type == 'hotfix' else 'develop'

    try:
        if not skip_switch:
            # Switch to the appropriate base branch
            base_branch = 'main' if branch_type in ['hotfix', 'release'] else 'develop'
            git.checkout(base_branch)

            # Pull changes from remote, but don't try to rebase
            try:
                git.repo.git.pull('origin', base_branch, '--ff-only')
            except GitCommandError as e:
                console.print(f"[red]Error pulling from remote: {e}[/red]")
                raise

            if not offline:
                # Pull the latest changes if online
                git.pull('origin', base_branch)
            else:
                console.print(f"[yellow]Skipping pull from {base_branch} due to offline mode.[/yellow]")

        # Check if the branch already exists
        if branch_name in git.get_branches():
            git.checkout(branch_name)
            console.print(f"[yellow]Switched to existing branch {branch_name}[/yellow]")
        else:
            # Create and checkout the new branch
            git.checkout(branch_name, create=True)
            console.print(f"[green]Created and switched to branch {branch_name}[/green]")

        if message:
            # Commit the initial changes if a message is provided
            git.add('.')
            if git.get_index_diff("HEAD"):
                git.commit(message)
                console.print(f"[green]Initial commit with message: {message}[/green]")
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")

        if branch_type == "release" and version_tag:
            # Create the tag locally, but don't push it yet
            git.create_tag(version_tag, message=f"Release {version_tag}")
            console.print(f"[green]Created local tag {version_tag}[/green]")

        if offline:
            console.print("[yellow]Note: Branch created locally. Remember to push changes when back online.[/yellow]")

        # Restore changes if we stashed them
        if has_changes:
            git.stash('pop')

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Finish a feature, hotfix, or release branch
#
@app.command()
def finish(
    delete: bool = typer.Option(True, "-d", "--delete", help="Delete the branch after finishing"),
    keep_local: bool = typer.Option(False, "-k", "--keep-local", help="Keep the local branch after finishing"),
    messages: List[str] = typer.Option([], "-m", "--message", help="Commit message(s) before finishing (can be used multiple times)")
):
    """
    Finish the current branch according to gitflow conventions.

    If --message is provided, changes will be committed before finishing.
    Multiple -m options can be used to create multi-paragraph commit messages.

    Examples:
        gf finish  # Finish current branch
        gf finish -m "Fix bug" # Commit and finish
        gf finish -m "Fix bug" -m "Detailed explanation" # Multi-paragraph commit and finish
    """
    git = GitWrapper()
    current_branch = git.get_current_branch()

    try:
        if current_branch in ['main', 'develop']:
            console.print("[red]Error: Cannot finish main or develop branches[/red]")
            return

        # Determine branch type from the current branch name
        if current_branch.startswith('feature/'):
            branch_type = 'feature'
        elif current_branch.startswith('hotfix/'):
            branch_type = 'hotfix'
        elif current_branch.startswith('release/'):
            branch_type = 'release'
        else:
            console.print(f"[red]Error: Current branch '{current_branch}' is not a feature, hotfix, or release branch[/red]")
            return

        # Handle commit messages if provided
        if messages:
            # Combine messages and commit changes with proper line wrapping
            combined_message = get_manual_commit_message_from_list(messages)
            git_wrapper.add('.')
            git_wrapper.commit(combined_message)
            console.print(f"[green]Committed changes with message: {combined_message.split(chr(10))[0]}[/green]")
        elif not handle_unstaged_changes(branch_type):
            return

        offline = not git_wrapper.check_network_connection()

        if offline:
            console.print("[yellow]Network is unavailable. Operating in offline mode.[/yellow]")
        else:
            fetch(remote="origin", branch=None, all_remotes=False, prune=False)

        push_changes = git.push_to_remote(current_branch)

        if not push_changes:
            console.print("[yellow]No changes to push. Finishing operation.[/yellow]")
            return

        target_branches = ["main", "develop"] if branch_type in ["hotfix", "release"] else ["develop"]

        if branch_type == "release":
            # Get the version from the branch name
            version = current_branch.split('/')[-1]
            if version.startswith('v'):
                version = version[1:]

            # Update version in the release branch
            git.update_repository_version(version, silent=True)  # Add silent parameter
            git.push('origin', current_branch)
            console.print(f"[green]Updated repository version to {version}[/green]")

            # Push the tag
            tag_name = f"v{version}"
            git.push('origin', tag_name)
            console.print(f"[green]Pushed tag {tag_name} to remote[/green]")

            # First merge into main
            git.checkout('main')
            git.merge(current_branch, no_ff=True)
            git.push('origin', 'main')
            console.print(f"[green]Merged and pushed {current_branch} into main[/green]")

            # Then merge main into develop
            git.checkout('develop')
            git.merge('main', no_ff=True)
            git.push('origin', 'develop')
            console.print(f"[green]Merged and pushed main into develop[/green]")

        # Merge into target branches - the version update will be included automatically
        for target in target_branches:
            git.checkout(target)
            git.merge(current_branch, no_ff=True)
            git.push('origin', target)
            console.print(f"[green]Merged and pushed {current_branch} into {target}[/green]")

        # Delete branches if requested
        if delete and not keep_local:
            git.delete_branch(current_branch, delete_remote=True, delete_local=True)  # Explicitly delete both
            git.cleanup_temp_branches()  # This will only delete local temp branches
        elif keep_local:
            console.print(f"[yellow]Keeping local branch {current_branch} as requested.[/yellow]")
        else:
            console.print(f"[yellow]Branch {current_branch} not deleted due to merge issues.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Sync main with develop
#
@app.command()
def sync(
    force: bool = typer.Option(False, "-f", "--force", help="Force sync even with conflicts"),
    push_changes: bool = typer.Option(True, "--push/--no-push", help="Push changes to remote"),
    remote: str = typer.Option("origin", help="Remote to push to"),
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Custom merge message"),
    body: Optional[str] = typer.Option(None, "-b", "--body", help="Custom merge message body")
):
    """Sync current branch with remote and merge develop into main."""
    try:
        # Save current branch
        original_branch = git_wrapper.get_current_branch()

        # Push current branch if requested
        if push_changes:
            git_wrapper.push_to_remote(original_branch)
            console.print(f"[green]Successfully pushed to {remote}/{original_branch}[/green]")

        # Only try to merge into main if we're on develop
        if original_branch == 'develop':
            # Switch to main
            git_wrapper.checkout('main')

            try:
                # Try to merge develop into main
                if message:
                    git_wrapper.merge('develop', no_ff=True, message=message, body=body)
                else:
                    git_wrapper.merge('develop', no_ff=True)
                console.print("[green]Merged develop into main[/green]")

                # Push main if requested
                if push_changes:
                    git_wrapper.push_to_remote('main')
                    console.print(f"[green]Successfully pushed to {remote}/main[/green]")

            except GitCommandError as e:
                if "CONFLICT" in str(e):
                    console.print("[red]Merge conflict detected![/red]")
                    console.print("[yellow]Please resolve conflicts and then run:[/yellow]")
                    console.print("  1. git add <resolved-files>")
                    console.print("  2. git commit")
                    console.print("  3. git push")
                    return 1
                raise

            # Return to original branch
            git_wrapper.checkout(original_branch)
            console.print(f"[green]Returned to {original_branch}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1

    return 0


def get_worktree_path(branch_name):
    """Helper function to get worktree path for a branch."""
    is_worktree, worktree_path = git_wrapper.is_worktree(branch_name)
    return worktree_path if is_worktree else None


def merge_in_worktree(source_branch, target_branch):
    """Helper function to safely merge in a worktree."""
    target_path = get_worktree_path(target_branch)
    if not target_path:
        raise GitCommandError(f"Cannot find worktree for {target_branch}")

    # Change to the target branch's worktree
    os.chdir(target_path)

    # Merge the source branch
    console.print(f"Merging {source_branch} into {target_branch}...")
    git_wrapper.merge(source_branch, no_ff=True)

    if push:
        git_wrapper.push('origin', target_branch)
        console.print(f"Pushed changes to {target_branch}")


#
# Weekly update hotfix branches
#
# This is specific to our project, so you'll likely not ever
# need it
#
@app.command()
def weekly_update(
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Specify a commit message"),
    body:    Optional[str] = typer.Option(None, "-b", "--body",    help="Specify a commit message body"),
):
    """
    Pull changes from the weekly-updates branch, commit any new changes, push them, and then merge them into develop and main branches.

    Parameters:
    - message: An optional commit message for the merge commits.
    - body   : An optional commit message body for the merge commits.

    Examples:
    - Pull changes, commit, push, and merge them:
        ./gitflow.py weekly_update -m "Merging weekly updates"
    - Pull changes, commit with a message body, push, and merge them:
        ./gitflow.py weekly_update -m "Merging weekly updates" -b "This includes documentation updates from the team."
    """
    try:
        weekly_branch = "weekly-updates"
        develop_branch = "develop"
        main_branch = "main"

        # Store the current branch
        original_branch = git_wrapper.get_current_branch()

        # Ensure the weekly-updates branch is checked out, fetch it if necessary
        if weekly_branch not in git_wrapper.get_branches():
            git_wrapper.fetch('origin', weekly_branch)
            git_wrapper.checkout(weekly_branch, start_point=f'origin/{weekly_branch}', create=True)
        else:
            git_wrapper.checkout(weekly_branch)
            git_wrapper.pull('origin', weekly_branch)
        console.print(f"[green]Pulled changes from {weekly_branch}[/green]")

        # Check for changes
        if git_wrapper.is_dirty():
            # Get the commit message
            full_commit_message = get_commit_message(message, body)

            # Commit changes
            git_wrapper.add('.')
            git_wrapper.commit(full_commit_message)
            console.print("[green]Changes committed.[/green]")

            # Push changes
            git_wrapper.push('origin', weekly_branch)
            console.print(f"[green]Pushed changes to {weekly_branch}[/green]")
        else:
            console.print("[yellow]No changes to commit.[/yellow]")

        # Create pull requests for develop and main branches
        def create_weekly_pr(base_branch: str):
            try:
                result = subprocess.run(
                    ["gh", "pr", "create", "--base", base_branch, "--head", weekly_branch,
                     "--title", f"Merge weekly updates into {base_branch}",
                     "--body", full_commit_message if 'full_commit_message' in locals() else "Merging weekly updates"],
                    capture_output=True, text=True, check=True
                )
                console.print(f"[green]Created pull request to merge {weekly_branch} into {base_branch}[/green]")
                return True
            except subprocess.CalledProcessError as e:
                if "A pull request for branch" in e.stderr:
                    console.print(f"[yellow]A pull request already exists for {weekly_branch} into {base_branch}[/yellow]")
                    return True
                elif "No commits between" in e.stderr:
                    console.print(f"[yellow]No commits between {weekly_branch} and {base_branch}. No pull request created.[/yellow]")
                    return False
                else:
                    console.print(f"[red]Error creating pull request: {e.stderr}[/red]")
                    return False

        prs_created_develop = create_weekly_pr(develop_branch)
        prs_created_main = create_weekly_pr(main_branch)

        if prs_created_develop or prs_created_main:
            console.print(f"[yellow]Weekly updates branch {weekly_branch} not deleted because pull requests were created.[/yellow]")
        else:
            console.print(f"[yellow]No pull requests were created as there were no differences to merge.[/yellow]")

        # Return to the original branch
        git_wrapper.checkout(original_branch)
        console.print(f"[green]Returned to {original_branch}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Update from the cds-view repository
#
# This is specific to our project, so you'll likely not ever
# need it
#
@app.command()
def cds_update(
    remote:  str           = typer.Option("https://github.wdf.sap.corp/I052341/tenantcleanup-cds", "-r", "--remote", help="URL of the remote tenantcleanup-cds repository"),
    local:   str           = typer.Option("cds-views", "-l", "--local",   help="Local path where cds-views content will be synced"),
    message: Optional[str] = typer.Option(None,        "-m", "--message", help="Specify a commit message"),
    body:    Optional[str] = typer.Option(None,        "-b", "--body",    help="Specify a commit message body"),
    create_pr: bool        = typer.Option(False,       "-p", "--pr",      help="Create pull requests instead of pushing directly")
):
    """
    Sync changes from the remote tenantcleanup-cds repository to the cds-views directory.
    """
    try:
        # Step 1: Manual clone process
        subprocess.run(['rm', '-rf', local], check=True)
        subprocess.run(['git', 'clone', remote, local], check=True)
        subprocess.run(['rm', '-rf', os.path.join(local, '.git')], check=True)
        subprocess.run(['git', 'add', local], check=True)

        # Step 2: Check for changes and commit
        status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True).stdout
        if not status.strip():
            console.print("[yellow]No changes to commit.[/yellow]")
            return

        # Get the commit message
        full_commit_message = get_commit_message(message or f"Sync changes from remote tenantcleanup-cds to {local}", body)
        git_wrapper.commit(full_commit_message)
        console.print("[green]Changes committed.[/green]")

        # Step 3: Push or create PRs for main and develop
        current_branch = git_wrapper.get_current_branch()
        for target_branch in ["develop", "main"]:
            if create_pr:
                try:
                    result = subprocess.run(
                        ["gh", "pr", "create", "--base", target_branch, "--head", current_branch,
                         "--title", f"Merge CDS view updates into {target_branch}",
                         "--body", full_commit_message],
                        capture_output=True, text=True, check=True
                    )
                    console.print(f"[green]Created pull request to merge changes into {target_branch}[/green]")
                except subprocess.CalledProcessError as e:
                    if "A pull request for branch" in e.stderr:
                        console.print(f"[yellow]A pull request already exists for {current_branch} into {target_branch}[/yellow]")
                    elif "No commits between" in e.stderr:
                        console.print(f"[yellow]No commits between {current_branch} and {target_branch}. No pull request created.[/yellow]")
                    else:
                        console.print(f"[red]Error creating pull request: {e.stderr}[/red]")
            else:
                try:
                    git_wrapper.checkout(target_branch)
                    git_wrapper.pull('origin', target_branch)
                    git_wrapper.merge(current_branch)
                    git_wrapper.push('origin', target_branch)
                    console.print(f"[green]Successfully merged and pushed changes to {target_branch}[/green]")
                except GitCommandError as e:
                    console.print(f"[red]Error pushing to {target_branch}: {e}[/red]")

            # Return to original branch
            git_wrapper.checkout(current_branch)

    except (subprocess.CalledProcessError, GitCommandError) as e:
        console.print(f"[red]Error: {e}[/red]")



#
# Update from a release branch merging it back into develop
#
@app.command()
def update(
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Specify a commit message"),
    body: Optional[str] = typer.Option(None, "-b", "--body", help="Specify a commit message body")
):
    """
    Update the current release branch and merge it back into the develop branch.
    Must be run from the release branch that is being updated.
    """
    try:
        current_branch = git_wrapper.get_current_branch()

        if not current_branch.startswith('release/'):
            console.print(f"[red]Error: Current branch '{current_branch}' is not a release branch[/red]")
            return

        if not git_wrapper.handle_unstaged_changes('release'):
            return

        offline = not git_wrapper.check_network_connection()

        if offline:
            console.print("[yellow]Network is unavailable. Operating in offline mode.[/yellow]")
        else:
            fetch(remote="origin", branch=None, all_remotes=False, prune=False)

        # Commit changes if a message is provided
        if message:
            full_commit_message = get_commit_message(message, body)
            git_wrapper.add('.')
            git_wrapper.commit(full_commit_message)
            console.print(f"[green]Committed changes with message: {full_commit_message}[/green]")

        push_changes = git_wrapper.push_to_remote(current_branch)

        if not push_changes:
            console.print("[yellow]No changes to push. Continuing with merge.[/yellow]")

        # Check if there are differences between release and develop branches
        changes_made = has_differences('develop', current_branch)
        console.print(f"[blue]Differences detected: {changes_made}[/blue]")

        if not changes_made:
            console.print("[yellow]No differences found between release and develop branches. No update needed.[/yellow]")
            return

        # Merge release branch into develop
        console.print(f"[yellow]Merging {current_branch} into develop...[/yellow]")
        merge_successful = git_wrapper.merge_to_target(current_branch, 'develop')

        if merge_successful:
            console.print(f"[green]Successfully merged {current_branch} into develop.[/green]")

            if not offline:
                # Create a pull request to merge develop into main
                console.print(f"[yellow]Creating pull request to merge develop into main.[/yellow]")
                pr_created = git_wrapper.create_pull_request('main', 'develop', "update")
                if pr_created:
                    console.print(f"[green]Pull request created to merge develop into main.[/green]")
                else:
                    console.print(f"[yellow]No pull request created. Changes may have been pushed directly.[/yellow]")
            else:
                console.print("[yellow]Operating in offline mode. Please create a pull request when online.[/yellow]")
        else:
            console.print(f"[yellow]Failed to merge {current_branch} into develop. Please resolve conflicts manually.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# List all branches
#
@app.command()
def ls(
    format: str = typer.Option(None, "-f", "--format",
        help="Output format: table (default), csv, tsv, plain")
):
    """
    List all branches, including both local and remote, with their comments and worktree information.

    Formats:
    - table: Rich formatted table (default)
    - csv: Comma-separated values
    - tsv: Tab-separated values
    - plain: Simple space-separated format (no network access)
    """
    # Only fetch when using table format (the default interactive view)
    if format is None:
        git_wrapper.fetch('--all', '--prune')

    local_branches = git_wrapper.get_local_branches()
    remote_branches = git_wrapper.get_remote_branches()
    branch_comments = git_wrapper.get_all_branch_comments()

    if format in ['csv', 'tsv', 'plain']:
        # Header
        separator = ',' if format == 'csv' else '\t' if format == 'tsv' else ' '
        if format in ['csv', 'tsv']:
            # For CSV/TSV, quote fields that might contain the separator
            def quote_field(field):
                if separator in field:
                    return f'"{field}"'
                return field

            print(separator.join(['branch', 'type', 'comment', 'worktree']))

            # Local branches
            for branch in local_branches:
                comment = quote_field(branch_comments.get(branch, ""))
                is_worktree, worktree_path = git_wrapper.is_worktree(branch)
                worktree_info = quote_field(f"at {worktree_path}") if is_worktree else ""
                print(separator.join([
                    quote_field(branch),
                    'local',
                    comment,
                    worktree_info
                ]))

            # Remote branches
            for branch in remote_branches:
                branch_name = branch.replace('origin/', '')
                comment = quote_field(branch_comments.get(branch_name, ""))
                print(separator.join([
                    quote_field(branch),
                    'remote',
                    comment,
                    ""
                ]))
        else:  # plain format
            # For plain format, just use simple space-separated output
            for branch in local_branches:
                is_worktree, worktree_path = git_wrapper.is_worktree(branch)
                worktree_info = f"<{worktree_path}>" if is_worktree else ""  # Using <> instead of []
                print(f"{branch} {worktree_info}")
            for branch in remote_branches:
                print(branch)
    else:
        # Original table format
        local_table = Table(title="Local branches", box=box.ROUNDED)
        local_table.add_column("Branch", style="cyan")
        local_table.add_column("Comment", style="green")
        local_table.add_column("Worktree", style="yellow")

        for branch in local_branches:
            comment = branch_comments.get(branch, "")
            is_worktree, worktree_path = git_wrapper.is_worktree(branch)
            worktree_info = f"at {worktree_path}" if is_worktree else ""
            local_table.add_row(branch, comment, worktree_info)

        remote_table = Table(title="Remote branches", box=box.ROUNDED)
        remote_table.add_column("Branch", style="cyan")
        remote_table.add_column("Comment", style="green")

        for branch in remote_branches:
            branch_name = branch.replace('origin/', '')
            comment = branch_comments.get(branch_name, "")
            remote_table.add_row(branch, comment)

        console.print(local_table)
        console.print("\n")
        console.print(remote_table)


#
# Checkout a branch
#
@app.command()
def checkout(
    target: Optional[str] = typer.Argument(None, help="The branch to switch to, or file/directory to revert"),
    force: bool = typer.Option(False, "-f", "--force", help="Force checkout, discarding local changes")
):
    """
    Switch to a different branch or revert changes in files/directories.
    """
    offline = not git_wrapper.check_network_connection()

    try:
        if target is None:
            # Interactive branch selection
            local_branches = []
            for head in git_wrapper.get_heads():
                # Check if branch is in a worktree
                is_worktree, worktree_path = git_wrapper.is_worktree(head.name)
                if is_worktree:
                    local_branches.append(f"Local : {head.name} [worktree at {worktree_path}]")
                else:
                    local_branches.append(f"Local : {head.name}")

            if not offline:
                remote_branches = [f"Remote: {ref.name.replace('origin/', '')}"
                                 for ref in git_wrapper.get_origin_refs()
                                 if ref.name != 'origin/HEAD']
                branches = local_branches + remote_branches
            else:
                branches = local_branches
                console.print("[yellow]Offline mode: Only local branches are available.[/yellow]")

            selected = inquirer.select(message="Select a branch:", choices=branches).execute()
            branch_type, branch_info = selected.split(": ", 1)

            # Extract branch name from selection (remove worktree info if present)
            branch_name = branch_info.split(" [worktree")[0]

            if branch_type == "Remote":
                target = f"origin/{branch_name}"
            else:
                target = branch_name

        # Check if target branch is in a different worktree
        target_branch = target.replace("origin/", "")
        is_worktree, worktree_path = git_wrapper.is_worktree(target_branch)
        current_dir = os.path.normpath(os.getcwd())

        if is_worktree and os.path.normpath(worktree_path) != current_dir:
            console.print(f"[yellow]Branch '{target}' is used in worktree at {worktree_path}[/yellow]")
            console.print(f"[yellow]Use 'cdworktree {target_branch}' to switch to that worktree.[/yellow]")
            return

        # Normal checkout logic
        if target in git_wrapper.get_branches() or (not offline and target.startswith("origin/")):
            # Check for uncommitted changes
            if git_wrapper.is_dirty(untracked_files=True) and not force:
                action = inquirer.select(
                    message="You have uncommitted changes. What would you like to do?",
                    choices=[
                        "Stash changes",
                        "Continue without stashing",
                        "Abort"
                    ]
                ).execute()

                if action == "Stash changes":
                    git_wrapper.stash('push')
                    console.print("[green]Changes stashed.[/green]")
                elif action == "Abort":
                    console.print("[yellow]Operation aborted.[/yellow]")
                    return

            # Switch to the branch
            try:
                if not offline and target.startswith("origin/"):
                    # For remote branches, create a new local branch
                    local_branch_name = target.split("/", 1)[1]
                    if local_branch_name not in git_wrapper.get_branches():
                        git_wrapper.checkout(local_branch_name, target, create=True)
                    else:
                        git_wrapper.checkout(local_branch_name)
                        if not offline:
                            git_wrapper.pull('origin', local_branch_name)
                else:
                    if force:
                        git_wrapper.checkout(target, force=True)
                    else:
                        git_wrapper.checkout(target)
                console.print(f"[green]Switched to branch {target.split('/')[-1]}[/green]")
            except GitCommandError as e:
                console.print(f"[red]Error: {e}[/red]")
        else:
            # Revert changes in file or directory
            try:
                if target == '.':
                    git_wrapper.checkout('.')
                    console.print(f"[green]Reverted all changes in the current directory[/green]")
                else:
                    git_wrapper.checkout('--', target)
                    console.print(f"[green]Reverted changes in {target}[/green]")
            except GitCommandError as e:
                console.print(f"[red]Error: {e}[/red]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Delete a branch
#
@app.command()
def rm(
    branch_names: Optional[List[str]] = typer.Argument(None, help="The branch name(s) to delete"),
    force: bool = typer.Option(False, "-f", "--force", help="Force delete the branch, even if it's not fully merged or has open pull requests"),
    all: bool = typer.Option(False, "-a", "--all", help="Delete both local and remote branches with the same name")
):
    """Delete one or more branches using an interactive menu or by specifying the branch names."""
    if not git_wrapper.check_network_connection():
        console.print("[yellow]Warning: No network connection. Only local operations will be performed.[/yellow]")
        all = False  # Disable remote operations

    if git_wrapper.check_network_connection():
        # Update local and remote references
        git_wrapper.fetch('--all')
        git_wrapper.remote('prune', 'origin')

    local_branches = [head.name for head in git_wrapper.get_repo_heads() if head.name not in ['develop', 'main']]
    remote_branches = []
    if git_wrapper.check_network_connection():
        remote_branches = [ref.name.replace('origin/', '') for ref in git_wrapper.get_origin_refs()
                           if ref.name != 'origin/HEAD' and ref.name.replace('origin/', '') not in ['develop', 'main']]

    if not branch_names:
        # Create the list of choices
        all_branches = []
        seen_branches = set()

        # If -a flag is used, add both local and remote for each branch
        if all:
            all_branch_names = set(local_branches + remote_branches)
            for branch in all_branch_names:
                if branch in local_branches:
                    all_branches.append(f"Local: {branch}")
                if branch in remote_branches:
                    all_branches.append(f"Remote: {branch}")
        else:
            # Original behavior without -a flag
            all_branches.extend(f"Local: {branch}" for branch in local_branches)
            if git_wrapper.check_network_connection():
                all_branches.extend(f"Remote: {branch}" for branch in remote_branches)

        selected_branches = inquirer.checkbox(
            message="Select branch(es) to delete:",
            choices=sorted(all_branches)
        ).execute()

        if not selected_branches:
            console.print("[yellow]No branches selected. Operation aborted.[/yellow]")
            return
    else:
        selected_branches = branch_names

    # Process selected branches
    processed_branches = set()  # Keep track of processed branches
    for branch in selected_branches:
        if "Local: " in branch:
            branch_name = branch.replace("Local: ", "")
        elif "Remote: " in branch:
            branch_name = branch.replace("Remote: ", "")
        else:
            branch_name = branch

        # Skip if we've already processed this branch
        if branch_name in processed_branches:
            continue
        processed_branches.add(branch_name)

        # When using -a, always try to delete both local and remote
        if all:
            git_wrapper.delete_branch(branch_name, delete_remote=True, delete_local=True)
        else:
            # Otherwise, only delete what was selected
            delete_local = any(f"Local: {branch_name}" in b for b in selected_branches)
            delete_remote = any(f"Remote: {branch_name}" in b for b in selected_branches)
            git_wrapper.delete_branch(branch_name, delete_remote=delete_remote, delete_local=delete_local)

    # Switch to develop branch if current branch was deleted
    if git_wrapper.get_current_branch() not in local_branches + ['develop', 'main']:
        git_wrapper.checkout('develop')
        console.print("[green]Switched to 'develop' branch.[/green]")


def check_prs(branch_name: str):
    if not git_wrapper.check_network_connection():
        console.print("[yellow]Cannot check for open pull requests due to no network connection.[/yellow]")
        return False
    result = subprocess.run(
        ["gh", "pr", "list", "--head", branch_name, "--state", "open", "--json", "number"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        prs = result.stdout.strip()
        return prs != "[]"
    else:
        console.print(f"[red]Error checking pull requests: {result.stderr}[/red]")
        return True





#
# Rename a Branch
#
@app.command()
def mv(
    old_name: Optional[str] = typer.Argument(None, help="The current name of the branch"),
    new_name: Optional[str] = typer.Argument(None, help="The new name for the branch"),
    all: bool = typer.Option(False, "-a", "--all", help="Rename both local and remote branches")
):
    """
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
    """
    offline = not git_wrapper.check_network_connection()

    if not offline:
        git_wrapper.fetch('--all')
        git_wrapper.remote('prune', 'origin')

    local_branches = [head.name for head in git_wrapper.get_repo_heads()]
    remote_branches = []
    if not offline:
        remote_branches = [ref.name.replace('origin/', '') for ref in git_wrapper.get_origin_refs() if ref.name != 'origin/HEAD']

    if not old_name:
        all_branches = [f"Local: {branch}" for branch in local_branches]
        if not offline:
            all_branches += [f"Remote: {branch}" for branch in remote_branches]
        old_name = inquirer.select(message="Select a branch to rename:", choices=all_branches).execute()

        if "Local: " in old_name:
            old_name = old_name.replace("Local: ", "")
            rename_local = True
            rename_remote = False
        elif "Remote: " in old_name:
            old_name = old_name.replace("Remote: ", "")
            rename_local = False
            rename_remote = not offline
        else:
            rename_local = True
            rename_remote = all and not offline
    else:
        rename_local = True
        rename_remote = all and not offline

    if not new_name:
        new_name = inquirer.text(message="Enter the new branch name:").execute()

    if old_name in ['develop', 'main'] or new_name in ['develop', 'main']:
        console.print("[red]Error: You cannot rename the develop or main branches.[/red]")
        return

    try:
        # Check for unstaged changes
        if git_wrapper.is_dirty(untracked_files=True):
            console.print("[yellow]You have unstaged changes.[/yellow]")
            action = inquirer.select(
                message="How would you like to proceed?",
                choices=[
                    "Commit changes",
                    "Continue without committing",
                    "Abort"
                ]
            ).execute()

            if action == "Commit changes":
                full_commit_message = get_commit_message()
                git_wrapper.add('.')
                git_wrapper.commit(full_commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Rename operation aborted.[/yellow]")
                return

        # Rename local branch
        if rename_local and old_name in local_branches:
            if old_name == git_wrapper.get_current_branch():
                git_wrapper.branch('-m', new_name)
            else:
                git_wrapper.branch('-m', old_name, new_name)
            console.print(f"[green]Renamed local branch from {old_name} to {new_name}[/green]")

        # Rename remote branch
        if rename_remote and old_name in remote_branches:
            try:
                git_wrapper.push('origin', f'{new_name}')
                git_wrapper.push('origin', f':{old_name}')
                console.print(f"[green]Renamed remote branch from {old_name} to {new_name}[/green]")
            except GitCommandError as e:
                if "protected branch" in str(e).lower():
                    console.print(f"[yellow]Protected branch {old_name} detected. Creating a new branch for pull request.[/yellow]")
                    pr_branch_name = f"rename-{old_name}-to-{new_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    git_wrapper.checkout(pr_branch_name, create=True)
                    git_wrapper.push('origin', pr_branch_name)

                    prs_created = create_pull_request(old_name, pr_branch_name, "rename")
                    if prs_created:
                        console.print(f"[green]Created pull request to rename {old_name} to {new_name}[/green]")
                    else:
                        console.print(f"[red]Failed to create pull request. Please create it manually.[/red]")

                    # Switch back to the original branch
                    git_wrapper.checkout(old_name)
                else:
                    console.print(f"[red]Error renaming remote branch: {e}[/red]")

        # Update tracking for the local branch if both local and remote were renamed
        if rename_local and rename_remote:
            git_wrapper.branch(f'--set-upstream-to=origin/{new_name}', new_name)

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")

    if offline:
        console.print("[yellow]Operating in offline mode. Remote operations were skipped.[/yellow]")
        console.print("[yellow]Please sync changes when online.[/yellow]")


#
# Add files to Git
#
@app.command()
def add(
    file_paths: List[str] = typer.Argument(...,                    help="The path(s) to the file(s) to add"),
    all:        bool      = typer.Option  (False, "-a", "--all",   help="Add changes from all tracked and untracked files"),
    force:      bool      = typer.Option  (False, "-f", "--force", help="Allow adding otherwise ignored files")
):
    """
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
    """
    try:
        if all:
            git_wrapper.add(all=True)
            console.print(f"[green]Added all changes to the staging area[/green]")
        else:
            if force:
                git_wrapper.add(file_paths, force=True)
            else:
                git_wrapper.add(file_paths)
            console.print(f"[green]Added {file_paths} to the staging area[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Stage changes
#
@app.command()
def stage(
    all        : bool      = typer.Option  (False, "-a", "--all",         help="Stage all changes"),
    interactive: bool      = typer.Option  (False, "-i", "--interactive", help="Use interactive mode for staging"),
    files      : List[str] = typer.Argument(None,                         help="Files or directories to stage")
):
    """
    Stage changes for the next commit.

    Examples:
    - Stage all changes          : ./gitflow.py stage --all
    - Stage specific files       : ./gitflow.py stage file1.py file2.py
    - Use interactive staging    : ./gitflow.py stage --interactive
    """
    try:
        if all:
            git_wrapper.add(all=True)
            console.print("[green]Staged all changes.[/green]")
        elif interactive:
            # Get only unstaged files
            status = git_wrapper.status('--porcelain').splitlines()
            unstaged = [s for s in status if s.startswith(' M') or s.startswith('??')]

            if not unstaged:
                console.print("[yellow]No unstaged changes to stage.[/yellow]")
                return

            choices = [f"{s[:2]} {s[3:]}" for s in unstaged]
            selected = inquirer.checkbox(
                message="Select files to stage:",
                choices=choices
            ).execute()

            if selected:
                for item in selected:
                    file = item[3:]  # Remove status indicators
                    git_wrapper.add(file)
                console.print(f"[green]Staged selected files: {', '.join(file[3:] for file in selected)}[/green]")
            else:
                console.print("[yellow]No files selected for staging.[/yellow]")
        elif files:
            git_wrapper.add(files)
            console.print(f"[green]Staged specified files: {', '.join(files)}[/green]")
        else:
            # Get only unstaged files
            status = git_wrapper.status('--porcelain').splitlines()
            unstaged = [s for s in status if s.startswith(' M') or s.startswith('??')]

            if not unstaged:
                console.print("[yellow]No unstaged changes to stage.[/yellow]")
                return

            console.print("[blue]Unstaged changes:[/blue]")
            for s in unstaged:
                console.print(s)

            stage_all = inquirer.confirm(message="Do you want to stage all unstaged changes?", default=False).execute()
            if stage_all:
                git_wrapper.add(all=True)
                console.print("[green]Staged all unstaged changes.[/green]")
            else:
                console.print("[yellow]No changes staged. Use --all or specify files to stage.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Unstage changes
#
@app.command()
def unstage(
    all:         bool      = typer.Option  (False, "-a", "--all",         help="Unstage all changes"),
    interactive: bool      = typer.Option  (False, "-i", "--interactive", help="Use interactive mode for unstaging"),
    files:       List[str] = typer.Argument(None,                         help="Files or directories to unstage")
):
    """
    Unstage changes from the staging area.

    Examples:
    - Unstage all changes        : ./gitflow.py unstage --all
    - Unstage specific files     : ./gitflow.py unstage file1.py file2.py
    - Use interactive unstaging  : ./gitflow.py unstage --interactive
    """
    try:
        if all:
            git_wrapper.reset()
            console.print("[green]Unstaged all changes.[/green]")
        elif interactive:
            status = git_wrapper.get_diff('--name-status', '--cached').splitlines()
            if not status:
                console.print("[yellow]No staged changes to unstage.[/yellow]")
                return

            choices = [f"{s.split()[0]} {s.split()[1]}" for s in status]
            selected = inquirer.checkbox(
                message="Select files to unstage:",
                choices=choices
            ).execute()

            if selected:
                for item in selected:
                    file = item.split()[1]  # Get filename
                    git_wrapper.reset('HEAD', file)
                console.print(f"[green]Unstaged selected files: {', '.join(item.split()[1] for item in selected)}[/green]")
            else:
                console.print("[yellow]No files selected for unstaging.[/yellow]")
        elif files:
            for file in files:
                git_wrapper.reset('HEAD', file)
            console.print(f"[green]Unstaged specified files: {', '.join(files)}[/green]")
        else:
            status = git_wrapper.get_diff('--name-status', '--cached').splitlines()
            if not status:
                console.print("[yellow]No staged changes to unstage.[/yellow]")
                return

            console.print("[blue]Staged changes:[/blue]")
            for s in status:
                console.print(s)

            unstage_all = inquirer.confirm(message="Do you want to unstage all changes?", default=False).execute()
            if unstage_all:
                git_wrapper.reset()
                console.print("[green]Unstaged all changes.[/green]")
            else:
                console.print("[yellow]No changes unstaged. Use --all or specify files to unstage.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")




#
# Stash changes
#
@app.command()
def stash(
    list             : bool          = typer.Option(False, "-l", "--list",      help="List all stashes"),
    show             : Optional[str] = typer.Option(None,  "-s", "--show",      help="Show the changes in a stash"),
    drop             : Optional[str] = typer.Option(None,  "-d", "--drop",      help="Drop a stash"),
    clear            : bool          = typer.Option(False, "-c", "--clear",     help="Clear all stashes"),
    message          : Optional[str] = typer.Option(None,  "-m", "--message",   help="Stash with a custom message"),
    include_untracked: bool          = typer.Option(False, "-u", "--untracked", help="Include untracked files in the stash")
):
    """
    Stash changes in the working directory.

    Examples:
    - Stash changes                   : ./gitflow.py stash
    - Stash changes with a message    : ./gitflow.py stash -m "Work in progress"
    - Stash including untracked files : ./gitflow.py stash --untracked
    - List all stashes                : ./gitflow.py stash --list
    - Show changes in a stash         : ./gitflow.py stash --show stash@{0}
    - Drop a stash                    : ./gitflow.py stash --drop stash@{0}
    - Clear all stashes               : ./gitflow.py stash --clear
    """
    try:
        if list:
            stash_list = git_wrapper.stash('list')
            if stash_list:
                console.print("[blue]Stash list:[/blue]")
                console.print(stash_list)
            else:
                console.print("[yellow]No stashes found.[/yellow]")
        elif show:
            stash_show = git_wrapper.stash('show', '-p', show)
            console.print(f"[blue]Changes in {show}:[/blue]")
            console.print(stash_show)
        elif drop:
            stash_info = git_wrapper.stash('list', show).strip()
            git_wrapper.stash('drop', drop)
            console.print(f"[green]Deleted stash: {stash_info}[/green]")
        elif clear:
            confirm = inquirer.confirm(message="Are you sure you want to clear all stashes?", default=False).execute()
            if confirm:
                git_wrapper.stash('clear')
                console.print("[green]Cleared all stashes.[/green]")
            else:
                console.print("[yellow]Stash clear operation cancelled.[/yellow]")
        else:  # push is the default action
            stash_args = ['push']
            if include_untracked:
                stash_args.append('--include-untracked')
            if message:
                split_message = git_wrapper.split_message_body(message)
                stash_args.extend(['-m', split_message])

            git_wrapper.stash(*stash_args)

            if message:
                console.print(f"[green]Stashed changes with message:[/green]\n{split_message}")
            else:
                console.print("[green]Stashed changes.[/green]")

            if include_untracked:
                console.print("[blue]Included untracked files in the stash.[/blue]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Unstash
#
@app.command()
def unstash(
    apply:       bool          = typer.Option (False, "-a", "--apply",       help="Apply the stash without removing it from the stash list"),
    interactive: bool          = typer.Option (False, "-i", "--interactive", help="Interactively select a stash"),
    stash_id:    Optional[str] = typer.Argument(None,                        help="The stash to apply (e.g., stash@{0})")
):
    """
    Apply and remove a stash (pop), or just apply it.

    Examples:
    - Pop the latest stash                      : ./gitflow.py unstash
    - Apply the latest stash without removing it: ./gitflow.py unstash --apply
    - Pop a specific stash                      : ./gitflow.py unstash stash@{0}
    - Apply a specific stash without removing it: ./gitflow.py unstash --apply stash@{0}
    - Interactively select a stash to pop       : ./gitflow.py unstash --interactive
    - Interactively select a stash to apply     : ./gitflow.py unstash --interactive --apply
    """
    try:
        if interactive or not stash_id:
            stash_list = git_wrapper.stash('list').splitlines()
            if not stash_list:
                console.print("[yellow]No stashes found.[/yellow]")
                return

            selected_stash = inquirer.select(
                message="Select a stash:",
                choices=stash_list
            ).execute()
            stash_id = selected_stash.split(':')[0]

        if apply:
            git_wrapper.stash('apply', stash_id)
            console.print(f"[green]Applied stash {stash_id} without removing it.[/green]")
        else:
            git_wrapper.stash('pop', stash_id)
            console.print(f"[green]Popped stash {stash_id}.[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")



#
# Commit with optional squash: Combine multiple commits into one
#
@app.command()
def commit(
    messages:    List[str]     = typer.Option  ([],    "-m", "--message",     help="Commit message(s) (can be used multiple times)"),
    body:        Optional[str] = typer.Option  (None,  "-b", "--body",        help="The commit message body"),
    add_all:     bool          = typer.Option  (False, "-a", "--all",         help="Add all changes before committing"),
    interactive: bool          = typer.Option  (False, "-i", "--interactive", help="Use interactive mode for commit message"),
    squash:      bool          = typer.Option  (False, "-s", "--squash",      help="Squash all commits ahead of remote into one"),
    files:       List[str]     = typer.Argument(None,                         help="Files or directories to commit")
):
    """
    Squash multiple commits into one, starting from a selected point.

    This command will:
    1. If there's a remote branch, show commits ahead of remote
    2. If no remote branch, let you select a past commit as starting point
    3. Combine all changes since that point into a single commit

    Examples:
    - Squash commits and enter commit message:
        ./gitflow.py squash
    """
    try:
        if not squash:
            _commit(messages, body, add_all, interactive, False, files)
            return

        # First handle any unstaged changes
        if git_wrapper.is_dirty(untracked_files=True):
            if add_all or inquirer.confirm(message="Do you want to stage all changes?", default=True).execute():
                git_wrapper.add(all=True)
                wip_message = get_manual_commit_message_from_list(messages) if messages else "WIP: Changes to be squashed"
                git_wrapper.commit(wip_message)
                console.print("[green]Auto-committed changes for squashing[/green]")

        current_branch = git_wrapper.get_current_branch()

        # Get the merge base with develop or main to find branch point
        try:
            base_commit = git_wrapper.merge_base("HEAD", "develop")
        except GitCommandError:
            try:
                base_commit = git_wrapper.merge_base("HEAD", "main")
            except GitCommandError:
                base_commit = None

        # Get commits only since branch point, excluding merge commits
        if base_commit:
            commits = git_wrapper.log(f"{base_commit}..HEAD", "--oneline", "--no-merges").splitlines()
        else:
            commits = git_wrapper.log("HEAD", "--oneline", "--no-merges", "-n", "10").splitlines()

        # Filter out commits that are already on any remote branch
        try:
            # First check current branch's remote
            try:
                remote_commit = git_wrapper.execute_git_command(['rev-parse', f"origin/{current_branch}"])
                commits = [c for c in commits if git_wrapper.rev_list(f"{remote_commit}..{c.split()[0]}").strip() != ""]
            except GitCommandError:
                pass  # Current branch might not be on remote yet

            # Then check develop and main
            for remote_branch in ["develop", "main"]:
                try:
                    remote_commit = git_wrapper.execute_git_command(['rev-parse', f"origin/{remote_branch}"])
                    commits = [c for c in commits if git_wrapper.rev_list(f"{remote_commit}..{c.split()[0]}").strip() != ""]
                except GitCommandError:
                    pass  # Skip if remote branch doesn't exist
        except GitCommandError:
            pass  # Silently ignore if remote access fails

        if not commits:
            console.print("[yellow]No commits available for squashing.[/yellow]")
            return

        selected = inquirer.select(
            message="Select the commit to squash from (all commits after this will be combined):",
            choices=commits
        ).execute()

        # Get the parent of the selected commit
        selected_hash = selected.split()[0]
        base_commit = f"{selected_hash}^"  # Parent of selected commit

        # Show commits that will be squashed
        commits_to_squash = git_wrapper.log(f"{base_commit}..HEAD", "--oneline").splitlines()
        console.print("[blue]Commits to be squashed:[/blue]")
        for commit_msg in commits_to_squash:
            console.print(commit_msg)

        # Only ask for confirmation if there's more than one commit
        if len(commits_to_squash) > 1 and not inquirer.confirm(message="Do you want to squash these commits?", default=True).execute():
            return

        # Perform the squash
        git_wrapper.reset('--soft', base_commit)
        git_wrapper.add(all=True)  # Auto-stage everything after squash
        console.print("[green]Successfully squashed commits[/green]")

        # Call internal commit function with interactive=True for squash
        _commit(messages, body, True, True, False, files)  # Force interactive for squash

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")




#
# Commit changes. Made internal to handle squash option.
#
def _commit(
    messages:    List[str]    = None,
    body:        Optional[str] = None,
    add_all:     bool         = False,
    interactive: bool         = False,
    squash:      bool         = False,
    files:       List[str]    = None
):
    """Internal commit function that handles the actual commit logic."""
    try:
        current_branch = git_wrapper.get_current_branch()

        if squash:
            try:
                # First handle any unstaged changes
                if git_wrapper.is_dirty(untracked_files=True):
                    if add_all or inquirer.confirm(message="Do you want to stage all changes?", default=True).execute():
                        git_wrapper.add(all=True)
                        console.print("[green]Added all changes to the staging area[/green]")

                # Determine base commit based on whether we have a merge base with main or develop
                base_commit = None
                try:
                    base_commit = git_wrapper.merge_base("HEAD", "main")
                except GitCommandError:
                    try:
                        base_commit = git_wrapper.merge_base("HEAD", "develop")
                    except GitCommandError:
                        # If no merge base found, use first commit of branch
                        base_commit = git_wrapper.rev_list("--max-parents=0", "HEAD").strip()

                # Get the complete diff from base to current
                if not git_wrapper.get_index_diff("HEAD") and not git_wrapper.get_untracked_files():
                    console.print("[yellow]No changes to commit.[/yellow]")
                    return

                # Generate or use provided commit message
                if not messages:
                    console.print("[blue]Analyzing all changes for commit message...[/blue]")
                    # Get all commits between base and HEAD to analyze
                    commits = git_wrapper.log(f"{base_commit}..HEAD", "--pretty=format:%H").splitlines()
                    if commits:
                        # Pass just the commit range to explain
                        full_commit_message = explain(None, None, base_commit, "HEAD", None, False, False, False, None, False, False)
                    else:
                        # If no commits, analyze the current changes
                        full_commit_message = explain(None, None, None, None, None, False, False, False, None, False, False)
                else:
                    full_commit_message = get_manual_commit_message_from_list(messages)

                if not full_commit_message or not full_commit_message.strip():
                    console.print("[red]Error: Empty commit message[/red]")
                    return

                # Perform the squash
                git_wrapper.reset('--soft', base_commit)
                git_wrapper.commit(full_commit_message)
                console.print(f"[green]Successfully squashed all changes into one commit:[/green]\n{full_commit_message}")

            except GitCommandError as e:
                console.print(f"[red]Error: {e}[/red]")
                return

        else:
            # Original commit logic
            if files:
                git_wrapper.add(files)
                console.print(f"[green]Added specified files to the staging area: {', '.join(files)}[/green]")
            elif add_all:
                git_wrapper.add(all=True)
                console.print("[green]Added all changes to the staging area[/green]")
            elif git_wrapper.is_dirty(untracked_files=True):
                console.print("[yellow]You have unstaged changes.[/yellow]")
                add_all = inquirer.confirm(message="Do you want to stage all changes?", default=True).execute()
                if add_all:
                    git_wrapper.add(all=True)
                    console.print("[green]Added all changes to the staging area[/green]")
                else:
                    console.print("[yellow]Proceeding with only staged changes.[/yellow]")

            # Ensure there are changes to commit
            if not git_wrapper.get_index_diff("HEAD") and not git_wrapper.get_untracked_files():
                console.print("[yellow]No changes to commit.[/yellow]")
                return

            api_key = git_wrapper.get_git_metadata("openai.apikey")
            if api_key and (interactive or not messages):
                # For AI generation, use the first message if available or None
                first_message = messages[0] if messages else None
                full_commit_message = get_commit_message(first_message, body)
            else:
                full_commit_message = get_manual_commit_message_from_list(messages)

            # Show the full commit message and ask for confirmation
            confirm = True

            if not confirm:
                console.print("[yellow]Commit aborted.[/yellow]")
                return

            # Perform the commit
            git_wrapper.commit(full_commit_message)
            console.print(f"[green]Committed changes with message.")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")



def get_commit_message(message=None, body=None):
    use_ai = inquirer.confirm(message="Do you want to use AI to generate a commit message?", default=True).execute()
    if use_ai:
        generated_message = explain(files=None, commit=None, start=None, end=None, as_command=False, days=None, daily_summary=False, summary=False, improve=False, custom_prompt=None, examples=False)
        if generated_message:
            console.print("[green]AI-generated commit message:[/green]")
            console.print(generated_message)

            edit_message = inquirer.confirm(message="Do you want to edit this message?", default=False).execute()
            if edit_message:
                edited_message = edit_in_editor(generated_message)
                console.print("[green]Edited commit message:[/green]")
                console.print(edited_message)
                full_commit_message = edited_message
            else:
                full_commit_message = generated_message
        else:
            console.print("[yellow]Failed to generate AI message. Falling back to manual entry.[/yellow]")
            full_commit_message = get_manual_commit_message(message, body)
    else:
        full_commit_message = get_manual_commit_message(message, body)

    # Final confirmation
    if not inquirer.confirm(message="Do you want to use this commit message?", default=True).execute():
        return get_commit_message(message, body)  # Recursively call the function if the user doesn't confirm

    return full_commit_message

def combine_messages(messages: List[str]) -> str:
    """
    Combine multiple messages into a single commit message with double newlines.
    Similar to how Git CLI handles multiple -m options.

    Args:
        messages: List of message strings

    Returns:
        Combined message string with double newlines between messages
    """
    if not messages:
        return ""

    # Filter out empty messages
    non_empty_messages = [msg.strip() for msg in messages if msg.strip()]

    if not non_empty_messages:
        return ""

    # Join messages with double newlines like Git CLI
    return "\n\n".join(non_empty_messages)


def get_manual_commit_message_from_list(messages: List[str]) -> str:
    """
    Get a commit message from a list of messages, with proper formatting.

    Args:
        messages: List of message strings

    Returns:
        Formatted commit message string
    """
    if not messages:
        return ""

    combined = combine_messages(messages)

    # Apply line wrapping at 72 characters for the body
    lines = combined.split('\n')
    formatted_lines = []

    for i, line in enumerate(lines):
        if i == 0:  # First line (subject) - keep as is
            formatted_lines.append(line)
        else:
            if line.strip():  # Non-empty line
                formatted_lines.append(split_message_body(line))
            else:  # Empty line
                formatted_lines.append(line)

    return '\n'.join(formatted_lines)


def get_manual_commit_message(message, body):
    if not message:
        message = inquirer.text(message="Enter commit message:").execute()
    if not body:
        body = inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()

    full_commit_message = message
    if body:
        full_commit_message += "\n\n" + split_message_body(body)

    # Show the message that will be used
    console.print(f"[blue]Commit message:[/blue]\n{full_commit_message}")

    # Remove the confirmation here since it's handled in the calling function
    return full_commit_message


#
# Helper Function to split a commit message body at the 72nd character
#
def split_message_body(body: str) -> str:
    """Splits the commit message body at the 72nd character, avoiding word splits.

    Also converts literal \\n sequences to actual newlines for proper formatting.
    """
    # Convert literal \n sequences to actual newlines
    body = body.replace('\\n', '\n')

    lines = []
    for paragraph in body.split('\n'):
        while len(paragraph) > 72:
            split_pos = paragraph.rfind(' ', 0, 72)
            if split_pos == -1:
                split_pos = 72
            lines.append(paragraph[:split_pos])
            paragraph = paragraph[split_pos:].strip()
        lines.append(paragraph)
    return '\n'.join(lines)



def handle_unstaged_changes(branch_type):
    if git_wrapper.is_dirty(untracked_files=True):
        console.print("[yellow]You have unstaged changes.[/yellow]")
        action = inquirer.select(
            message="How would you like to proceed?",
            choices=[
                "Commit changes",
                "Stash changes",
                "Continue without committing",
                "Abort"
            ]
        ).execute()

        if action == "Commit changes":
            full_commit_message = get_commit_message()
            git_wrapper.add('.')
            git_wrapper.commit(full_commit_message)
            console.print("[green]Changes committed.[/green]")
        elif action == "Stash changes":
            git_wrapper.stash('save', f"Stashed changes before finishing {branch_type}")
            console.print("[green]Changes stashed.[/green]")
        elif action == "Abort":
            console.print("[yellow]Finish operation aborted.[/yellow]")
            return False
    return True


#
# Explain Code Changes using AI
#
@app.command()
def explain(
    files:         List[str]     = typer.Argument(None,                      help="Files to explain. If not provided, uses the current state."),
    commit:        Optional[str] = typer.Option  (None,  "-c", "--commit",   help="If we are to analyze only one given commit hash."),
    start:         Optional[str] = typer.Option  (None,  "-s", "--start",    help="Starting commit hash."),
    end:           Optional[str] = typer.Option  (None,  "-e", "--end",      help="Ending commit hash. If not provided, uses HEAD."),
    days:          Optional[int] = typer.Option  (None,  "-d", "--days",     help="Number of days to look back in history"),
    daily_summary: bool          = typer.Option  (False,       "--daily",    help="Provide a summary on a daily basis instead of per commit"),
    summary:       bool          = typer.Option  (False,       "--summary",  help="Provide a high-level summary of what the file is for"),
    improve:       bool          = typer.Option  (False, "-i", "--improve",  help="Provide suggestions for improving the file"),
    custom_prompt: Optional[str] = typer.Option  (None,  "-p", "--prompt",   help="Additional custom prompt to include in the request"),
    examples:      bool          = typer.Option  (False,       "--examples", help="Include specific code examples in improvement suggestions"),
    as_command:    bool          = typer.Option  (True, hidden=True)
):
    """
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
    """
    try:
        if files:
            file_contents = {}
            file_histories = {}
            for file in files:
                if os.path.isdir(file):
                    console.print(f"[yellow]Skipping directory: {file}[/yellow]")
                    continue

                # Fetch file history
                file_history = get_file_history(file, days, daily_summary)
                if file_history is None or file_history.strip() == '':
                    console.print(f"[yellow]No history found for file: {file}. Using current content only.[/yellow]")
                    file_history = "No commit history available."

                # Get the current content of the file from Git
                try:
                    current_content = git_wrapper.show(f'HEAD:{file}')
                except GitCommandError:
                    console.print(f"[yellow]Warning: Couldn't retrieve current content of {file} from Git. Using local file.[/yellow]")
                    try:
                        with open(file, 'r') as f:
                            current_content = f.read()
                    except FileNotFoundError:
                        console.print(f"[red]Error: File not found: {file}[/red]")
                        continue

                file_contents[file] = current_content[:30000]  # Limit to first 30000 characters
                file_histories[file] = file_history

            if not file_contents:
                console.print("[red]No valid files to analyze.[/red]")
                return None

            if improve:
                prompt = prompt_improve(file_contents, file_histories, examples)
            elif summary:
                prompt = prompt_summary(file_contents, file_histories)
            elif daily_summary:
                prompt = prompt_files_daily_summary(file_contents, file_histories)
            else:
                prompt = prompt_files_details(file_contents, file_histories)
        else:
            # Determine the diff based on provided commits
            if commit:
                diff = git_wrapper.show(f'{commit}^..{commit}')
            elif days is not None:
                start = get_first_commit_last_n_days(days)
                command_parts = [
                    f"{start}..HEAD",
                    "--pretty=format:'%C(auto)%h %cd'",
                    "--date=short",
                    "-p"
                ]
                diff = git_wrapper.log(*command_parts)
            elif start and end:
                diff = git_wrapper.get_diff(start, end)
            elif start:
                command_parts = [
                    f"{start}..HEAD",
                    "--pretty=format:'%C(auto)%h %cd'",
                    "--date=short",
                    "-p"
                ]
                diff = git_wrapper.log(*command_parts)
            else:
                # Get diff of unstaged changes
                unstaged_diff = git_wrapper.get_diff()
                # Get diff of staged changes
                staged_diff = git_wrapper.get_diff('--cached')
                # Combine unstaged and staged diffs
                diff = unstaged_diff + "\n" + staged_diff

            prompt = prompt_commit(diff)

        if custom_prompt:
            prompt += f"\n\nAdditional instructions: \n{custom_prompt}"

        # Use the AI client to generate the explanation
        ai_client = AIClient(config_provider=GitConfig())
        current_provider = ai_client.get_current_provider_name()

        # Determine the appropriate message based on the command context
        if improve:
            action_msg = "Analyzing code and generating improvement suggestions"
        elif summary:
            action_msg = "Analyzing code and generating summary"
        elif daily_summary:
            action_msg = "Analyzing commit history and generating daily summary"
        elif commit or start or end or days:
            action_msg = "Analyzing commit history and generating explanation"
        else:
            action_msg = "Analyzing changes and generating explanation"

        # Show spinner while generating content
        with console.status(f"[bold blue]{action_msg} using {current_provider}...") as status:
            generated_message = ai_client.prompt(prompt)

            if as_command:
                # Get repository URL for clickable links
                repo_url = git_wrapper.get_remote_url()
                if repo_url.endswith('.git'):
                    repo_url = repo_url[:-4]

                # Process the message to add clickable links
                processed_message = ""
                for line in generated_message.split('\n'):
                    if "- Commit: " in line:
                        commit_hash = line.split("- Commit: ")[1].strip()
                        processed_line = f"- Commit: [link={repo_url}/commit/{commit_hash}]{commit_hash}[/link]"
                        processed_message += processed_line + "\n"
                    else:
                        processed_message += line + "\n"

                console.print("[green]Generated explanation:[/green]")
                console.print(processed_message)
            else:
                return generated_message

    except Exception as e:
        console.print(f"[red]Error generating explanation: {e}[/red]")
        return None

def prompt_improve(file_contents, file_histories, examples):
    prompt = f"""
    Analyze the following file(s) and provide suggestions for improvement.
    Consider each file's current content, its development history, and best practices
    for the file's language or purpose.

    Files to analyze:
    {', '.join(file_contents.keys())}

    For each file, please provide:
    1. A brief overview of the file's current state and purpose.
    2. 3-5 specific suggestions for improvement, considering:
    - Code quality and readability
    - Performance optimizations
    - Best practices for the file's language or framework
    - Potential bugs or security issues
    - Architecture and design patterns
    3. Any notable trends or patterns in the file's development history
    that might inform future improvements.

    {"For each suggestion, provide a specific code example of how to implement the improvement." if examples else ""}

    Format your response as follows:
    - Start with an overview of each file
    - List each suggestion with a brief explanation
    {"- Follow each suggestion with a code example, clearly marked" if examples else ""}
    - Conclude with insights from the development history

    Important: Be specific and provide actionable suggestions.
    Explain the rationale behind each suggestion.
    {"When providing code examples, ensure they are relevant, concise, and clearly illustrate the suggested improvement." if examples else ""}

    File contents and histories:
    """
    for file, content in file_contents.items():
        prompt += f"\n\n{file} content:\n{content}\n\nHistory:\n{file_histories[file]}"
    return prompt


def prompt_summary(file_contents, file_histories):
    prompt = f"""
    Provide a high-level summary of what the following file(s) are for.
    Consider their current content and development history to explain their purpose,
    main functionalities, and their role within the project.

    Files to summarize:
    {', '.join(file_contents.keys())}

    For each file, please provide:
    1. The main purpose of the file
    2. Key functionalities or components
    3. How it fits into the overall project structure
    4. Any significant changes or trends in its development history

    Format your response as a concise yet comprehensive summary for each file.

    Important: Start your response directly with the summary. Do not use
    any introductory phrases like "Sure," "Here's," or "Certainly."

    File contents and histories:
    """
    for file, content in file_contents.items():
        prompt += f"\n\n{file} content:\n{content}\n\nHistory:\n{file_histories[file]}"
    return prompt


def prompt_files_daily_summary(file_contents, file_histories):
    prompt = f"""
    Explain the development history of the following file(s) over time.
    Provide a summary for each day that had changes, following this structure:

    1. Date of changes
    2. Overall interpretation of the day's changes (purpose, theme, or goal)
    3. Brief summary of all changes made that day, including:
    - Key modifications
    - Overall impact or purpose of the day's changes
    - Number of commits

    Present the history from past to present, highlighting major milestones or significant refactors.

    Important: Start your response directly with the explanation. Do not use
    any introductory phrases like "Sure," "Here's," or "Certainly."

    Format:
    - Use plain text only. No markup language or formatting (except as noted below).
    - Limit each line to a maximum of 70 characters.
    - Use bullet points (- ) for lists.
    - Separate sections with a blank line.
    - Do not use asterisks (*) for headlines or emphasis.
    - Summarize all changes for each day, don't list individual commits.

    Example structure:

    2023-05-25:
    Overall: Improved script functionality and documentation

    - Key changes: Re-enabled regex for scripts, removed dependencies,
    updated documentation
    - Impact: Enhanced filtering capabilities, simplified codebase,
    improved maintainability
    - Commits: 3

    Files to explain:
    {', '.join(file_contents.keys())}

    File histories:
    """
    for file, history in file_histories.items():
        prompt += f"\n\n{file} history:\n{history}"
    return prompt


def prompt_files_details(file_contents, file_histories):
    """Generate a prompt for explaining file histories with clickable commit links."""
    # Get repository URL for clickable links
    repo_url = git_wrapper.get_remote_url()
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]

    prompt = f"""
    Explain the development history of the following file(s) over time.
    For each significant change, provide:

    1. Timestamp of the change
    2. Brief description of what was modified
    3. The impact or purpose of the change
    4. Commit hash (shortened to 7 characters)

    Present the history from past to present, highlighting major milestones or significant refactors.

    Important: Start your response directly with the explanation. Do not use
    any introductory phrases like "Sure," "Here's," or "Certainly."

    Format:
    - Use plain text only. No markup language or formatting (except as noted below).
    - Limit each line to a maximum of 70 characters.
    - Use bullet points (- ) for lists.
    - Separate sections with a blank line.
    - Do not use asterisks (*) for headlines or emphasis.
    - If the description is the same as the commit message, do not repeat it.
    - Format commit lines exactly as: "- Commit: HASH" (7 characters)

    Example structure:

    2023-05-25 14:30:00: Re-enabled regex for scripts directory
    - Impact: Improved script filtering capabilities
    - Commit: a48dfba

    2023-05-25 15:45:00: Removed Obsidian exporter dependency
    - Impact: Simplified codebase and reduced external dependencies
    - Commit: d402328

    2023-05-25 16:20:00: Updated documentation
    - Impact: Improved user guidance and code maintainability
    - Commit: bc32dba

    Files to explain:
    {', '.join(file_contents.keys())}

    File histories:
    """
    for file, history in file_histories.items():
        prompt += f"\n\n{file} history:\n{history}"
    return prompt


def prompt_commit(diff):
    prompt = """
    Generate a concise and meaningful commit message body for the following code changes. Follow these guidelines:

    0. At the very beginning, write a concise headline that summarizes the changes. Use at a maximum 72 characters.

    1. Start with a brief summary (2-3 bullet points) of the high-level changes and intentions.

    2. Then, describe the changes in more detail, grouped by file or related functionality.

    3. Format:
    - Use plain text only. No markup language or formatting (except as noted below).
    - Limit each line to a maximum of 70 characters.
    - Use bullet points (- ) for lists.
    - Separate sections with a blank line.
    - Do not use asterics (*) for headlines or emphasis.

    4. Code references:
    - Minimize code blocks. Only use them for critical, short snippets.
    - When necessary, place code on its own line, indented by 2 spaces.
    - For function or class names, use single backticks (e.g., `function_name`).

    5. Focus on conveying the meaning and impact of the changes, not just listing them.

    6. If changes span multiple branches, organize the description by branch.

    7. Aim for a comprehensive yet concise message. Don't omit important details, but also avoid unnecessary verbosity.

    8. Remember, no line is to exceed 70 characters in length.

    9. Really remember, no line is to exceed 70 characters in length. Do an extra check for this.

    Remember, the goal is to create a clear, informative commit message that future developers
    (including yourself) will find helpful when reviewing the project history.

    Changes:
    """
    prompt += diff[:100000]  # Truncated for API limits
    return prompt



def edit_in_editor(initial_message):
    # Create a temporary file
    fd, temp_path = tempfile.mkstemp(suffix=".tmp")
    try:
        with os.fdopen(fd, 'w') as temp_file:
            temp_file.write(initial_message)

        editor = os.environ.get('EDITOR', 'vim')  # Default to vim if EDITOR is not set
        subprocess.call([editor, temp_path])

        # Read the edited content
        with open(temp_path, 'r') as temp_file:
            edited_content = temp_file.read().strip()

        return edited_content

    finally:
        # Make sure we remove the temporary file
        os.unlink(temp_path)


def get_file_history(filename, days=None, daily_summary=False):
    try:
        # Prepare the git log command
        log_command = ['--follow', '--format=%H,%at,%s', '--', filename]

        # If days is specified, add the date filter
        if days is not None:
            since_date = datetime.now() - timedelta(days=days)
            log_command = ['--since', since_date.strftime('%Y-%m-%d')] + log_command

        # Get the git log for the specific file
        log_output = git_wrapper.log(*log_command)

        # Process the log output
        if daily_summary:
            daily_commits = defaultdict(list)
            for line in log_output.split('\n'):
                if line:
                    commit_hash, timestamp, message = line.split(',', 2)
                    date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
                    daily_commits[date].append(f"{message} (Commit: {commit_hash[:7]})")

            history = []
            for date, commits in sorted(daily_commits.items()):
                history.append(f"{date}:")
                for commit in commits:
                    history.append(f"  - {commit}")
        else:
            history = []
            for line in log_output.split('\n'):
                if line:
                    commit_hash, timestamp, message = line.split(',', 2)
                    date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                    history.append(f"{date} - {message} (Commit: {commit_hash[:7]})")

        return '\n'.join(history)
    except GitCommandError as e:
        console.print(f"[yellow]Warning: Error fetching file history: {e}[/yellow]")
        return None


def get_first_commit_last_n_days(n_days, hash_length=8):
    # Adjust start_date to the beginning of the day, n_days ago
    start_date = (datetime.now() - timedelta(days=n_days)).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date_str = start_date.strftime('%Y-%m-%d')

    commits = git_wrapper.get_commits(since=start_date_str)

    first_commit_of_day = None
    last_commit_processed = None  # Variable to keep track of the last commit processed
    for commit in commits:
        commit_date = datetime.fromtimestamp(commit.committed_date)
        # Update last_commit_processed on each iteration
        last_commit_processed = commit
        # Check if commit_date is on the specified start_date
        if (commit_date - timedelta(days=1)).date() == start_date.date():
            if first_commit_of_day is None or commit.committed_date < first_commit_of_day.committed_date:
                first_commit_of_day = commit

    if first_commit_of_day:
        return(first_commit_of_day.hexsha[:hash_length])
    else:
        # Use the last commit processed if no commit was found for the specified day
        if last_commit_processed:
            #print(f"No commit found for the specified day. Using last commit found: {last_commit_processed.hexsha[:hash_length]}")
            return(last_commit_processed.hexsha[:hash_length])
        else:
            print("No commits found.")
            return None


#
# Fetch
#
@app.command()
def fetch(
    remote:      Optional[str] = typer.Argument(None,                    help="The name of the remote to fetch from (default is 'origin')"),
    branch:      Optional[str] = typer.Option  (None, "-b",  "--branch", help="Specific branch to fetch"),
    prune:       bool          = typer.Option  (False, "-p", "--prune",  help="Prune deleted branches from the remote repository"),
    all_remotes: bool          = typer.Option  (False, "-a", "--all",    help="Fetch changes from all remotes")
):
    """
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
    """
    if not git_wrapper.check_network_connection():
        console.print("[red]Error: No network connection. Unable to fetch.[/red]")
        return

    try:
        if all_remotes:
            console.print("[blue]Fetching changes from all remotes...[/blue]")
            if prune:
                git_wrapper.fetch('--all', '--prune')
            else:
                git_wrapper.fetch('--all')
            console.print("[green]Fetched changes from all remotes.[/green]")
        else:
            remote_name = remote or 'origin'
            if branch:
                console.print(f"[blue]Fetching branch {branch} from remote {remote_name}...[/blue]")
                git_wrapper.fetch(remote_name, branch)
                console.print(f"[green]Fetched branch {branch} from remote {remote_name}.[/green]")
            else:
                console.print(f"[blue]Fetching changes from remote {remote_name}...[/blue]")
                if prune:
                    git_wrapper.fetch('--prune', remote_name)
                else:
                    git_wrapper.fetch(remote_name)
                console.print(f"[green]Fetched changes from remote {remote_name}.[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error fetching changes: {e}[/red]")


#
# Merge
#
@app.command()
def merge(
    source: Optional[str] = typer.Argument(None, help="The source branch to merge from"),
    target: Optional[str] = typer.Argument(None, help="The target branch to merge into"),
    squash: bool = typer.Option(False, "--squash", help="Squash commits when merging"),
    no_ff: bool = typer.Option(True, "--no-ff", help="Create a merge commit even when fast-forward is possible")
):
    """Merge one local branch into another."""
    try:
        # Store original branch
        original_branch = git_wrapper.get_current_branch()

        # Use the current branch if no source is provided
        if source is None:
            source = original_branch

        # If no target is provided, use the current branch
        if target is None:
            target = original_branch

        # Check if target branch is in a worktree
        is_worktree, worktree_path = git_wrapper.is_worktree(target)
        current_dir = os.path.realpath(os.getcwd())
        if is_worktree and os.path.realpath(worktree_path) != current_dir:
            console.print(f"[yellow]Target branch '{target}' is used in worktree at {worktree_path}[/yellow]")
            console.print("[yellow]To merge into this branch, cd to the worktree directory first.[/yellow]")
            return 1

        # Check if there are differences to merge
        try:
            merge_base = git_wrapper.merge_base(source, target)
            source_commit = git_wrapper.rev_parse(source)
            target_commit = git_wrapper.rev_parse(target)

            if merge_base == source_commit and merge_base == target_commit:
                console.print(f"[yellow]Already up to date. No differences between {source} and {target}.[/yellow]")
                return 0

            # Only switch to target branch if there are differences
            git_wrapper.checkout(target)

            # Perform the merge
            if squash:
                git_wrapper.merge(source, squash=True)
            else:
                git_wrapper.merge(source, no_ff=no_ff)
            console.print(f"[green]Successfully merged {source} into {target}[/green]")

            # Return to original branch unless we're already there
            if original_branch != target:
                git_wrapper.checkout(original_branch)
                console.print(f"[green]Returned to {original_branch}[/green]")

        except GitCommandError as e:
            console.print(f"[red]Error merging: {e}[/red]")
            # Try to return to original branch on error
            if original_branch != git_wrapper.get_current_branch():
                git_wrapper.checkout(original_branch)
            return 1

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1

    return 0


#
# Push changes
#
@app.command()
def push(
    remote: str = typer.Option("origin", help="Remote to push to"),
    branch: Optional[str] = typer.Argument(None, help="Branch to push (defaults to current)"),
    messages: List[str] = typer.Option([], "-m", "--message", help="Commit message(s) before pushing (can be used multiple times)"),
    body: Optional[str] = typer.Option(None, "-b", "--body", help="Commit message body"),
    force: bool = typer.Option(False, "-f", "--force", help="Force push")
):
    """
    Push changes to remote repository.

    If --message is provided, changes will be committed before pushing.
    Use --body to add a detailed message body to the commit.

    Examples:
        gf push  # Push current branch
        gf push feature/test  # Push specific branch
        gf push -m "Fix bug" # Commit and push
        gf push -m "Fix bug" -b "Detailed explanation" # Commit with body and push
    """
    try:
        # Get current branch if none specified
        if branch is None:
            branch = git_wrapper.get_current_branch()

        # Check if branch is in a worktree
        is_worktree, worktree_path = git_wrapper.is_worktree(branch)
        if is_worktree and worktree_path != os.getcwd():
            console.print(f"[yellow]Branch '{branch}' is used in worktree at {worktree_path}[/yellow]")
            console.print("[yellow]To push this branch, cd to the worktree directory first.[/yellow]")
            return 1

        # Check for network connection
        offline = not git_wrapper.check_network_connection()
        if offline:
            console.print("[yellow]No network connection. Changes will be pushed when online.[/yellow]")

        # Handle uncommitted changes
        if git_wrapper.is_dirty(untracked_files=True):
            if messages:
                # Commit changes with provided messages
                full_message = get_manual_commit_message_from_list(messages)
                if body:
                    full_message += "\n\n" + split_message_body(body)
                git_wrapper.add('.')
                git_wrapper.commit(full_message)
                console.print("[green]Changes committed.[/green]")
            else:
                console.print("[yellow]You have unstaged changes.[/yellow]")
                action = inquirer.select(
                    message="How would you like to proceed?",
                    choices=[
                        "Commit changes",
                        "Continue without committing",
                        "Abort"
                    ]
                ).execute()

                if action == "Commit changes":
                    full_message = get_commit_message()
                    git_wrapper.add('.')
                    git_wrapper.commit(full_message)
                    console.print("[green]Changes committed.[/green]")
                elif action == "Abort":
                    console.print("[yellow]Push aborted.[/yellow]")
                    return 1

        if not offline:
            # Check for remote changes
            git_wrapper.fetch(remote)
            try:
                ahead_behind = git_wrapper.rev_list('--left-right', '--count', f'{remote}/{branch}...HEAD').split()
                behind = int(ahead_behind[0])
                ahead = int(ahead_behind[1])

                if behind > 0 and not force:
                    console.print(f"[yellow]Your local branch is {behind} commit(s) behind the remote branch.[/yellow]")
                    action = inquirer.select(
                        message="How would you like to proceed?",
                        choices=[
                            "Pull and rebase",
                            "Force push",
                            "Abort"
                        ]
                    ).execute()

                    if action == "Pull and rebase":
                        git_wrapper.pull('--rebase', remote, branch)
                    elif action == "Force push":
                        force = True
                    else:
                        console.print("[yellow]Push aborted.[/yellow]")
                        return 1

            except GitCommandError:
                # Remote branch doesn't exist yet
                pass

            # Push changes
            git_wrapper.push(remote, branch, force=force)
            console.print(f"[green]Successfully pushed to {remote}/{branch}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1

    return 0


#
# Pull changes
#
@app.command()
def pull(
    remote:       str           = typer.Option("origin",                help="The name of the remote to pull from"),
    branch:       Optional[str] = typer.Option(None,                    help="The branch to pull. If not specified, pulls the current branch"),
    all_branches: bool          = typer.Option(False,"-a",  "--all",    help="Pull all branches"),
    prune:        bool          = typer.Option(False,"-p",  "--prune",  help="Prune remote-tracking branches no longer on remote"),
    rebase:       bool          = typer.Option(False,"-r",  "--rebase", help="Rebase the current branch on top of the upstream branch after fetching")
):
    """Pull changes from the remote repository."""
    git = GitWrapper()

    # Fetch changes first
    git.fetch(remote, None, False, prune)
    console.print("Fetched changes from remote.")

    if all_branches:
        console.print("Pulling changes for all local branches...")
        current_branch = git.get_current_branch()
        current_path = Path.cwd()
        console.print(f"[blue]Current branch: {current_branch}[/blue]")

        # First pull the current branch
        console.print(f"[blue]Pulling current branch {current_branch}...[/blue]")
        pull_args = ['git', 'pull', remote]
        if rebase:
            pull_args.insert(2, '--rebase')
        result = subprocess.run(pull_args, capture_output=True, text=True)
        if result.returncode == 0:
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('Updating'):
                        console.print(f"[blue]{line}[/blue]")
                    elif line.startswith('Fast-forward'):
                        console.print(f"[green]{line}[/green]")
                    elif line.startswith('Already up to date'):
                        console.print(f"[yellow]{line}[/yellow]")
                    else:
                        if line.startswith('+++') or line.startswith('---'):
                            console.print(line)
                        else:
                            colored_line = ''
                            for char in line:
                                if char == '+':
                                    colored_line += '[green]+[/green]'
                                elif char == '-':
                                    colored_line += '[red]-[/red]'
                                else:
                                    colored_line += char
                            console.print(colored_line)
            if "Already up to date" in result.stdout:
                console.print(f"[yellow]Branch {current_branch} is up to date.[/yellow]")
            else:
                console.print(f"[green]Pulled changes for branch {current_branch}[/green]")
        else:
            console.print(f"[red]Error pulling current branch: {result.stderr}[/red]")

        # Then pull all other branches
        local_branches = git.get_local_branches()
        console.print(f"[blue]Found {len(local_branches)} local branches[/blue]")

        for local_branch in local_branches:
            if local_branch == current_branch:
                console.print(f"[blue]Skipping current branch {local_branch} as it was already pulled[/blue]")
                continue

            console.print(f"[blue]Processing branch {local_branch}...[/blue]")
            try:
                # Check if branch is in a worktree
                is_worktree, worktree_path = git.is_worktree(local_branch)
                if is_worktree:
                    console.print(f"[yellow]Skipping branch {local_branch} - it's used in worktree at {worktree_path}[/yellow]")
                    continue

                # Check if the branch has an upstream or if the remote branch exists
                branch_status = git.get_branch_status(local_branch)
                has_upstream = branch_status.get('has_upstream', False)

                # Check if remote branch exists
                remote_branch_exists = False
                try:
                    git.repo.git.ls_remote('--exit-code', '--heads', remote, local_branch)
                    remote_branch_exists = True
                except GitCommandError:
                    remote_branch_exists = False

                if not has_upstream and not remote_branch_exists:
                    console.print(f"[yellow]Skipping branch {local_branch} - no upstream configured and no remote branch found[/yellow]")
                    continue

                # Switch to branch and pull
                console.print(f"[blue]Switching to branch {local_branch}...[/blue]")
                git.checkout(local_branch)

                # Use direct git pull to show the actual output
                pull_args = ['git', 'pull', remote]

                # If no upstream is configured but remote branch exists, specify the branch explicitly
                if not has_upstream and remote_branch_exists:
                    pull_args.append(local_branch)
                    # Also set up tracking for future pulls
                    git.repo.git.branch('--set-upstream-to', f'{remote}/{local_branch}')
                    console.print(f"[blue]Set up tracking for {local_branch} -> {remote}/{local_branch}[/blue]")

                if rebase:
                    pull_args.insert(2, '--rebase')

                result = subprocess.run(pull_args, capture_output=True, text=True)
                if result.returncode == 0:
                    if result.stdout:
                        for line in result.stdout.strip().split('\n'):
                            if line.startswith('Updating'):
                                console.print(f"[blue]{line}[/blue]")
                            elif line.startswith('Fast-forward'):
                                console.print(f"[green]{line}[/green]")
                            elif line.startswith('Already up to date'):
                                console.print(f"[yellow]{line}[/yellow]")
                            else:
                                if line.startswith('+++') or line.startswith('---'):
                                    console.print(line)
                                else:
                                    colored_line = ''
                                    for char in line:
                                        if char == '+':
                                            colored_line += '[green]+[/green]'
                                        elif char == '-':
                                            colored_line += '[red]-[/red]'
                                        else:
                                            colored_line += char
                                    console.print(colored_line)
                    if "Already up to date" in result.stdout:
                        console.print(f"[yellow]Branch {local_branch} is up to date.[/yellow]")
                    else:
                        console.print(f"[green]Pulled changes for branch {local_branch}[/green]")
                else:
                    error_msg = result.stderr.lower()
                    if "no such ref was fetched" in error_msg or "couldn't find remote ref" in error_msg:
                        console.print(f"[yellow]Branch {local_branch} no longer exists on remote - skipping[/yellow]")
                    else:
                        console.print(f"[red]Error pulling branch {local_branch}: {result.stderr}[/red]")

                # Switch back to current branch
                console.print(f"[blue]Switching back to branch {current_branch}...[/blue]")
                git.checkout(current_branch)

            except Exception as e:
                console.print(f"[red]Error processing branch {local_branch}: {e}[/red]")
                # Try to switch back to current branch in case of error
                try:
                    git.checkout(current_branch)
                except:
                    pass

        # Final check to ensure we're on the original branch
        if current_branch != git.get_current_branch():
            console.print(f"[blue]Returning to original branch {current_branch}...[/blue]")
            git.checkout(current_branch)
        return

    else:
        # Pull single branch
        pull_args = ['git', 'pull', remote]
        if branch:
            pull_args.append(branch)
        if rebase:
            pull_args.append('--rebase')

        try:
            result = subprocess.run(pull_args, capture_output=True, text=True)
            if result.returncode == 0:
                if result.stdout:
                    # Split the output into lines and print with appropriate colors
                    for line in result.stdout.strip().split('\n'):
                        if line.startswith('Updating'):
                            console.print(f"[blue]{line}[/blue]")
                        elif line.startswith('Fast-forward'):
                            console.print(f"[green]{line}[/green]")
                        elif line.startswith('Already up to date'):
                            console.print(f"[yellow]{line}[/yellow]")
                        else:
                            # Handle diff output
                            if line.startswith('+++') or line.startswith('---'):
                                console.print(line)  # Keep original color for file names
                            else:
                                # Color all + and - characters in the line
                                colored_line = ''
                                for char in line:
                                    if char == '+':
                                        colored_line += '[green]+[/green]'
                                    elif char == '-':
                                        colored_line += '[red]-[/red]'
                                    else:
                                        colored_line += char
                                console.print(colored_line)
                if "Already up to date" in result.stdout:
                    console.print("[yellow]Branch is up to date.[/yellow]")
                else:
                    console.print("[green]Pulled changes successfully.[/green]")
            else:
                console.print(f"[red]Error pulling changes: {result.stderr}[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")




#
# Status
#
@app.command()
def status():
    """
    Display a concise status of the current Git repository in a single, comprehensive table.
    """
    console = Console()

    try:
        # Create main status table
        status_table = Table(title="Git Repository Status", box=box.HEAVY_EDGE)
        status_table.add_column("Category", style="cyan", no_wrap=True)
        status_table.add_column("Details", style="green")

        # Get current branch
        current_branch = git_wrapper.get_current_branch()
        status_table.add_row("Current Branch", current_branch)

        # Get commit information
        last_commit = git_wrapper.get_last_commit()
        commit_message = last_commit.message.strip()
        commit_author = last_commit.author.name
        commit_date = last_commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
        status_table.add_row("Last Commit", f"{commit_message[:50]}..." if len(commit_message) > 50 else commit_message)
        status_table.add_row("Commit Author", commit_author)
        status_table.add_row("Commit Date", commit_date)

        # Get ahead/behind info
        try:
            ahead_behind = git_wrapper.rev_list('--left-right', '--count', f'origin/{current_branch}...HEAD').split()
            behind = int(ahead_behind[0])
            ahead = int(ahead_behind[1])
            status_table.add_row("Commits Ahead/Behind", f"Ahead by {ahead}, Behind by {behind}")
        except GitCommandError:
            status_table.add_row("Commits Ahead/Behind", "Unable to determine")

        # Get status
        status = git_wrapper.status(porcelain=True)
        staged = [line for line in status.split('\n') if line.startswith(('A', 'M', 'R', 'D')) and len(line) > 1]
        unstaged = [line for line in status.split('\n') if line.startswith('??') or (line.startswith(' ') and len(line) > 1)]

        # Add changes to table
        if staged or unstaged:
            changes = []
            for change in staged:
                changes.append(f"Staged: {change[3:]}")
            for change in unstaged:
                changes.append(f"Unstaged: {change[3:]}")
            status_table.add_row("Changes", "\n".join(changes))
        else:
            status_table.add_row("Changes", "Working tree clean")

        # Add remotes to table
        remotes = git_wrapper.get_remotes()
        if remotes:
            remote_info = []
            for remote_name, remote_url in remotes:
                remote_info.append(f"{remote_name}: {remote_url}")
            status_table.add_row("Remotes", "\n".join(remote_info))

        # Display the table
        console.print(status_table)

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Compare
#
@app.command()
def compare(
    file_path: str           = typer.Argument(...,  help="The path to the file to compare"),
    branch1:   Optional[str] = typer.Argument(None, help="The first branch to compare"),
    branch2:   Optional[str] = typer.Argument(None, help="The second branch to compare")
):
    """
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
    """
    try:
        # List branches
        local_branches  = git_wrapper.get_local_branches()
        remote_branches = [ref.name.replace('origin/', '') for ref in git_wrapper.get_origin_refs() if ref.name != 'origin/HEAD']

        if branch1 is None:
            branches = local_branches + remote_branches
            branch1 = inquirer.select(message="Select the first branch:", choices=branches).execute()

        if branch2 is None:
            branches = local_branches + remote_branches
            branch2 = inquirer.select(message="Select the second branch:", choices=branches).execute()

        # Perform the diff
        diff = git_wrapper.get_diff(f'{branch1}:{file_path}', f'{branch2}:{file_path}')
        console.print(diff if diff else "[green]No differences found.[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Cherry-pick a file from the current branch into a target branch
#
@app.command()
def cp(
    file_path:      str           = typer.Argument(...,                 help="The path to the file or directory to copy"),
    target_branches: List[str]    = typer.Argument(None,                help="The target branch(es) to copy into"),
    push:           bool          = typer.Option  (True, "--push",      help="Push the changes to the remote repository after copying"),
    create_pr:      bool          = typer.Option  (False, "-p", "--pr", help="Create a pull request instead of pushing directly")
):
    """
    Copy files from the current branch into one or more target branches.
    """
    try:
        offline = not git_wrapper.check_network_connection()
        original_branch = git_wrapper.get_current_branch()

        # Check for uncommitted changes
        if git_wrapper.has_uncommitted_changes(file_path):
            console.print(f"[yellow]Warning: There are uncommitted changes in {file_path}[/yellow]")
            console.print("[yellow]Only committed changes will be copied. Commit your changes first if you want to include them.[/yellow]")

        # If target_branches is not provided, show a list of branches to select from
        if not target_branches:
            branches = [head.name for head in git_wrapper.get_heads() if head.name != original_branch]
            target_branches = inquirer.checkbox(
                message="Select branch(es) to copy into:",
                choices=branches
            ).execute()

        # Get list of files to copy before switching branches
        if git_wrapper.is_directory(f"{original_branch}:{file_path}"):
            files = git_wrapper.get_tracked_files(original_branch, file_path)
            if not files:
                console.print(f"[yellow]No tracked files found in {file_path}[/yellow]")
                return
            paths_to_copy = files
        else:
            paths_to_copy = [file_path]

        # Read all file contents from current branch before switching
        file_contents = {}
        for path in paths_to_copy:
            try:
                file_contents[path] = git_wrapper.show(f"{original_branch}:{path}")
            except GitCommandError:
                console.print(f"[red]Error: {path} not found in {original_branch}[/red]")
                continue

        for target_branch in target_branches:
            # Checkout the target branch
            git_wrapper.checkout(target_branch)
            console.print(f"[green]Switched to branch {target_branch}[/green]")

            changes_made = False
            for path in paths_to_copy:
                if path not in file_contents:
                    continue

                # Read the file content from the target branch
                try:
                    # First check if file exists and is identical in working directory
                    try:
                        with open(path, 'r') as f:
                            current_content = f.read()
                            if current_content == file_contents[path]:
                                console.print(f"[yellow]File {path} is identical in {target_branch}. Skipping copy.[/yellow]")
                                continue
                    except FileNotFoundError:
                        pass  # File doesn't exist yet, will be added

                    # If file doesn't exist or is different, copy it
                    console.print(f"[green]Copying {path} to {target_branch}[/green]")
                except GitCommandError:
                    console.print(f"[green]Adding {path} to {target_branch}[/green]")

                # Create directory if it doesn't exist (but only if there's a directory part)
                dir_name = os.path.dirname(path)
                if dir_name:  # Only create directories if path has a directory component
                    os.makedirs(dir_name, exist_ok=True)

                # Write the content from the current branch into the target branch
                with open(path, 'w') as target_file:
                    target_file.write(file_contents[path])

                try:
                    # Add the file and check if it actually changed
                    git_wrapper.add(path)
                    # Check if the file was actually modified
                    status = git_wrapper.repo.git.status('--porcelain', path)
                    if status.strip():
                        changes_made = True
                except GitCommandError as e:
                    console.print(f"[red]Error adding {path}: {e}[/red]")
                    continue

            if changes_made:
                # Commit all changes for this branch
                try:
                    commit_message = f"Copy latest changes for {file_path} from {original_branch} to {target_branch}"
                    git_wrapper.commit(commit_message)
                    console.print(f"[green]Copied the latest changes into {target_branch}[/green]")
                except GitCommandError as e:
                    if "nothing to commit" not in str(e):
                        raise

                # Push changes or create a pull request
                if push or create_pr:
                    if not offline:
                        try:
                            if create_pr:
                                # Create a new branch for the pull request
                                pr_branch_name = f"cp-{file_path.replace('/', '-')}-{target_branch}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                                git_wrapper.checkout(pr_branch_name, create=True)
                                git_wrapper.push('origin', pr_branch_name)

                                # Create pull request
                                result = subprocess.run(
                                    ["gh", "pr", "create", "--base", target_branch, "--head", pr_branch_name,
                                     "--title", f"Copy changes for {file_path} into {target_branch}",
                                     "--body", f"Automated pull request to copy changes for {file_path} from {original_branch} into {target_branch}"],
                                    capture_output=True, text=True
                                )
                                if result.returncode != 0:
                                    console.print(f"[red]Error creating pull request: {result.stderr}[/red]")
                                else:
                                    console.print(f"[green]Created pull request to merge changes into {target_branch}[/green]")
                            else:
                                git_wrapper.push('origin', target_branch)
                                console.print(f"[green]Pushed changes to {target_branch}[/green]")
                        except GitCommandError as e:
                            if "protected branch" in str(e):
                                console.print(f"[yellow]Protected branch {target_branch} detected. Creating a pull request instead.[/yellow]")
                                # Create a new branch for the pull request
                                pr_branch_name = f"cp-{file_path.replace('/', '-')}-{target_branch}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                                git_wrapper.checkout(pr_branch_name, create=True)
                                git_wrapper.push('origin', pr_branch_name)

                                # Create pull request
                                result = subprocess.run(
                                    ["gh", "pr", "create", "--base", target_branch, "--head", pr_branch_name,
                                     "--title", f"Copy changes for {file_path} into {target_branch}",
                                     "--body", f"Automated pull request to copy changes for {file_path} from {original_branch} into {target_branch}"],
                                    capture_output=True, text=True
                                )
                                if result.returncode != 0:
                                    console.print(f"[red]Error creating pull request: {result.stderr}[/red]")
                                else:
                                    console.print(f"[green]Created pull request to merge changes into {target_branch}[/green]")
                            else:
                                console.print(f"[red]Error while pushing: {e}[/red]")
                    else:
                        console.print(f"[yellow]No network connection. Changes for {target_branch} will be pushed when online.[/yellow]")

        # Return to the original branch
        git_wrapper.checkout(original_branch)
        console.print(f"[green]Returned to branch {original_branch}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Revert commits
#
@app.command()
def revert(
    commit:         Optional[str] = typer.Argument(None,                         help="The commit hash to revert"),
    all_branches:   bool          = typer.Option  (False, "-a", "--all-branches", help="Revert on all branches containing the commit"),
    branches:       List[str]     = typer.Option  (None,  "-b", "--branch",      help="Specific branch(es) to revert on"),
    parent:         Optional[int] = typer.Option  (None,  "-p", "--parent",      help="For merge commits, specify parent (1 or 2, default: 1)"),
    dry_run:        bool          = typer.Option  (False, "-d", "--dry-run",     help="Show what would be done without making changes"),
    interactive:    bool          = typer.Option  (False, "-i", "--interactive", help="Interactively select branches to revert on"),
    create_pr:      bool          = typer.Option  (False,       "--pr",          help="Create pull requests instead of direct push"),
    no_push:        bool          = typer.Option  (False,       "--no-push",     help="Don't push changes to remote"),
    force:          bool          = typer.Option  (False, "-f", "--force",       help="Skip branches with conflicts"),
    latest:         bool          = typer.Option  (False,       "--latest",      help="Revert latest merge commits on main and develop"),
    related:        bool          = typer.Option  (False,       "--related",     help="Find and revert related merge commits from same source"),
    pr_number:      Optional[int] = typer.Option  (None,        "--pr-number",   help="Revert all merge commits for specific PR number"),
    source_branch:  Optional[str] = typer.Option  (None,        "--source-branch", help="Revert all merges from specific source branch")
):
    """
    Revert a commit on one or more branches with GitFlow-aware automation.

    This command can automatically detect merge commits and revert them on the appropriate
    branches according to GitFlow conventions. It includes safety checks and dry-run capabilities.

    Examples:
    - Revert a commit on current branch:
        gf revert abc123

    - Revert on all branches containing the commit:
        gf revert abc123 --all-branches

    - Dry run to see what would happen:
        gf revert abc123 --all-branches --dry-run

    - Revert a merge commit (auto-detects and uses parent 1):
        gf revert abc123

    - Revert merge commit with specific parent:
        gf revert abc123 --parent 2

    - Interactive branch selection:
        gf revert abc123 --interactive

    - Create PRs instead of direct push:
        gf revert abc123 --all-branches --pr

    - Revert on specific branches:
        gf revert abc123 --branch main --branch develop

    - Revert latest merge commits (GitFlow aware):
        gf revert --latest

    - Find and revert related merge commits:
        gf revert abc123 --related

    - Revert by PR number:
        gf revert --pr-number 123

    - Revert by source branch:
        gf revert --source-branch feature/new-ui
    """
    try:
        git = GitWrapper()

        # Handle different input modes
        target_commits = {}  # branch -> commit_hash mapping

        if latest:
            # Find latest merge commits on main and develop
            console.print("[blue]Finding latest merge commits on main and develop...[/blue]")

            latest_commits = {}
            for branch in ['main', 'develop']:
                try:
                    # Get the latest merge commit on this branch
                    log_output = git.log('--oneline', '--merges', '-n', '1', branch)
                    if log_output.strip():
                        commit_hash = log_output.split()[0]
                        latest_commits[branch] = commit_hash
                        console.print(f"  Latest merge on {branch}: {commit_hash}")
                    else:
                        console.print(f"  No merge commits found on {branch}")
                except GitCommandError:
                    console.print(f"  Branch {branch} not found")

            if not latest_commits:
                console.print("[yellow]No latest merge commits found.[/yellow]")
                return

            target_commits = latest_commits

        elif pr_number:
            # Find all merge commits for a specific PR
            console.print(f"[blue]Searching for merge commits from PR #{pr_number}...[/blue]")

            for branch in git.get_branches():
                try:
                    # Search for merge commits mentioning the PR number
                    log_output = git.log('--grep', f'#{pr_number}', '--merges', '--oneline', branch)
                    for line in log_output.strip().split('\n'):
                        if line.strip():
                            commit_hash = line.split()[0]
                            target_commits[branch] = commit_hash
                            console.print(f"  Found PR #{pr_number} merge on {branch}: {commit_hash}")
                except GitCommandError:
                    continue

        elif source_branch:
            # Find all merge commits from a specific source branch
            console.print(f"[blue]Searching for merge commits from {source_branch}...[/blue]")

            for branch in git.get_branches():
                try:
                    # Look for merge commits that mention the source branch
                    log_output = git.log('--grep', source_branch, '--merges', '--oneline', branch)
                    for line in log_output.strip().split('\n'):
                        if line.strip():
                            commit_hash = line.split()[0]
                            # Verify this is actually from the source branch
                            source = git.get_merge_commit_source_branch(commit_hash)
                            if source and source == source_branch:
                                target_commits[branch] = commit_hash
                                console.print(f"  Found {source_branch} merge on {branch}: {commit_hash}")
                except GitCommandError:
                    continue

        elif related and commit:
            # Find related merge commits from the same source branch
            console.print(f"[blue]Finding related merge commits for {commit}...[/blue]")

            # First get the source branch for the provided commit
            source = git.get_merge_commit_source_branch(commit)
            if not source:
                console.print(f"[yellow]Could not determine source branch for {commit}[/yellow]")
                target_commits = {git.get_current_branch(): commit}
            else:
                console.print(f"  Source branch: {source}")
                # Find all merge commits from this source branch
                related_commits = git.find_related_merge_commits(commit)
                target_commits = related_commits
                for branch, hash in related_commits.items():
                    console.print(f"  Found related merge on {branch}: {hash}")

        elif commit:
            # Single commit mode - determine target branches
            target_branches = []

            if all_branches:
                target_branches = git.get_branches_containing_commit(commit)
            elif branches:
                target_branches = branches
            elif interactive:
                available_branches = git.get_branches_containing_commit(commit)
                target_branches = inquirer.checkbox(
                    message="Select branches to revert on:",
                    choices=available_branches
                ).execute()
            else:
                target_branches = [git.get_current_branch()]

            # Set the same commit for all target branches
            target_commits = {branch: commit for branch in target_branches}

        else:
            console.print("[red]Error: Must specify a commit hash or use --latest, --pr-number, or --source-branch[/red]")
            return 1

        if not target_commits:
            console.print("[yellow]No commits found to revert.[/yellow]")
            return 0

        # Validate all commits and gather information
        revert_plan = []
        has_conflicts = False

        console.print(f"\n[blue]Planning revert operations...[/blue]")

        for branch, commit_hash in target_commits.items():
            # Validate commit hash
            commit_info = git.get_commit_info(commit_hash)
            if not commit_info:
                console.print(f"[red]Error: Invalid commit hash '{commit_hash}' for branch {branch}[/red]")
                continue

            # Check if it's a merge commit
            is_merge, parent_count, parents = git.is_merge_commit(commit_hash)

            # Display commit information
            console.print(f"\n[blue]Commit to revert on {branch}:[/blue]")
            console.print(f"  Hash: {commit_info['hash']} ({commit_info['full_hash']})")
            console.print(f"  Message: {commit_info['message']}")
            console.print(f"  Author: {commit_info['author']}")
            console.print(f"  Date: {commit_info['date']}")

            if is_merge:
                console.print(f"  [yellow]Merge commit with {parent_count} parents:[/yellow]")
                for i, parent_hash in enumerate(parents, 1):
                    parent_info = git.get_commit_info(parent_hash)
                    console.print(f"    Parent {i}: {parent_hash} - {parent_info['message'][:50]}...")

                # Auto-select parent 1 if not specified
                selected_parent = parent or 1
                console.print(f"  [green]Using parent {selected_parent} for revert[/green]")
            else:
                selected_parent = None

            # Check if revert would be clean
            can_revert, conflicts = git.can_revert_cleanly(commit_hash, branch, selected_parent)

            plan_item = {
                'branch': branch,
                'commit': commit_hash,
                'commit_info': commit_info,
                'is_merge': is_merge,
                'parent': selected_parent,
                'can_revert': can_revert,
                'conflicts': conflicts,
                'action': 'skip' if not can_revert else 'revert'
            }
            revert_plan.append(plan_item)

            if can_revert:
                console.print(f"  ✓ {branch}: Clean revert possible")
            else:
                has_conflicts = True
                console.print(f"  ✗ {branch}: Would create conflicts")
                if conflicts:
                    for conflict in conflicts[:3]:  # Show first 3 conflicts
                        console.print(f"    - {conflict}")
                    if len(conflicts) > 3:
                        console.print(f"    ... and {len(conflicts) - 3} more conflicts")

        if not revert_plan:
            console.print("[red]No valid commits to revert.[/red]")
            return 1

        # Handle conflicts
        if has_conflicts and not force:
            console.print(f"\n[yellow]Some branches would have conflicts during revert.[/yellow]")
            action = inquirer.select(
                message="How would you like to proceed?",
                choices=[
                    "Skip conflicted branches and continue",
                    "Abort operation",
                    "Show detailed conflict information"
                ]
            ).execute()

            if action == "Abort operation":
                console.print("[yellow]Operation aborted.[/yellow]")
                return 0
            elif action == "Show detailed conflict information":
                for item in revert_plan:
                    if not item['can_revert'] and item['conflicts']:
                        console.print(f"\n[red]Conflicts in {item['branch']}:[/red]")
                        for conflict in item['conflicts']:
                            console.print(f"  - {conflict}")
                return 0

        # Show dry-run results
        if dry_run:
            console.print(f"\n[yellow]DRY RUN - No changes will be made[/yellow]")

            table = Table(title="Revert Plan")
            table.add_column("Branch", style="cyan")
            table.add_column("Commit", style="yellow")
            table.add_column("Message", style="white")
            table.add_column("Action", style="green")

            for item in revert_plan:
                action_text = "✓ Revert" if item['can_revert'] else "✗ Skip (conflicts)"
                action_style = "green" if item['can_revert'] else "red"

                table.add_row(
                    item['branch'],
                    item['commit_info']['hash'],
                    item['commit_info']['message'][:50] + "...",
                    Text(action_text, style=action_style)
                )

            console.print(table)
            console.print(f"\n[blue]Summary:[/blue]")
            success_count = sum(1 for item in revert_plan if item['can_revert'])
            skip_count = len(revert_plan) - success_count
            console.print(f"  - {success_count} branches would be reverted successfully")
            console.print(f"  - {skip_count} branches would be skipped due to conflicts")

            if not no_push and not create_pr:
                console.print(f"  - Changes would be pushed to remote")
            elif create_pr:
                console.print(f"  - Pull requests would be created")

            return 0

        # Final confirmation
        revertable_branches = [p['branch'] for p in revert_plan if p['can_revert']]
        if not revertable_branches:
            console.print("[yellow]No branches can be reverted cleanly. Operation cancelled.[/yellow]")
            return 0

        if not inquirer.confirm(
            message=f"Proceed with reverting on {len(revertable_branches)} branch(es)?",
            default=False
        ).execute():
            console.print("[yellow]Operation cancelled.[/yellow]")
            return 0

        # Perform the reverts
        console.print(f"\n[blue]Performing reverts...[/blue]")

        results = []
        for item in revert_plan:
            if not item['can_revert']:
                console.print(f"[yellow]Skipping {item['branch']} due to conflicts[/yellow]")
                continue

            branch = item['branch']
            commit_hash = item['commit']
            parent = item['parent']

            console.print(f"\n[blue]Reverting on {branch}...[/blue]")

            result = git.perform_revert_on_branch(
                commit=commit_hash,
                branch=branch,
                parent=parent,
                create_pr=create_pr,
                no_push=no_push
            )

            results.append(result)

            if result['success']:
                console.print(f"[green]Successfully reverted {commit_hash} on {branch}[/green]")
                if result.get('pr_created'):
                    console.print(f"[green]Created pull request for {branch}[/green]")
                elif not no_push:
                    console.print(f"[green]Pushed changes to {branch}[/green]")
            else:
                console.print(f"[red]Failed to revert on {branch}: {result.get('error', 'Unknown error')}[/red]")

        # Summary
        successful_reverts = [r for r in results if r['success']]
        failed_reverts = [r for r in results if not r['success']]

        console.print(f"\n[blue]Revert Summary:[/blue]")
        console.print(f"  ✓ {len(successful_reverts)} successful reverts")
        console.print(f"  ✗ {len(failed_reverts)} failed reverts")

        if failed_reverts:
            console.print(f"\n[red]Failed branches:[/red]")
            for result in failed_reverts:
                console.print(f"  - {result['branch']}: {result.get('error', 'Unknown error')}")

        return 0 if successful_reverts else 1

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


LABEL_COLORS = {
    "bug":         "#CB233A",
    "description": "#185ED2",
    "duplicate":   "#C5C9CE",
    "enhancement": "#94EBEA",
    "help wanted": "#10745E",
    "invalid":     "#DDE457",
    "question":    "#CC59DD",
    "wontfix":     "#FFFFFF",
    "project":     "#5319E7"
}

def format_date(date_string):
    if not date_string:
        return ""
    try:
        date = datetime.fromisoformat(date_string.rstrip('Z'))
        now = datetime.now(pytz.utc)
        delta = now - date.replace(tzinfo=pytz.utc)

        if delta.days == 0:
            if delta.seconds < 3600:
                return f"{delta.seconds // 60} minutes ago"
            else:
                return f"{delta.seconds // 3600} hours ago"
        elif delta.days == 1:
            return "yesterday"
        elif delta.days < 7:
            return f"{delta.days} days ago"
        elif delta.days < 30:
            return f"{delta.days // 7} weeks ago"
        elif delta.days < 365:
            return f"{delta.days // 30} months ago"
        else:
            return f"{delta.days // 365} years ago"
    except AttributeError:
        return "N/A"

def format_author(author, use_login=False):
    if not author:
        return "N/A"
    return author.get('login' if use_login else 'name', 'N/A')

def format_assignees(assignees, use_login=False):
    if not assignees:
        return "N/A"
    return ", ".join([a.get('login' if use_login else 'name', 'N/A') for a in assignees])

import re
from rich.console import Console

def perform_search(search, issues, regex=False, search_in_body=False):
    try:
        # Determine if the search string is a regex or not
        if regex:
            search_regex = re.compile(search, re.IGNORECASE | re.DOTALL)
        else:
            # Treat search as a plain string and escape special characters
            search_regex = re.compile(re.escape(search), re.IGNORECASE | re.DOTALL)

        filtered_issues = []
        for issue in issues:
            title = issue.get('title', '')
            body  = issue.get('body',  '')

            # Check for negation search (if search string starts with '!')
            if search.startswith('!'):
                neg_search = search[1:].strip()  # Remove '!' and strip any extra whitespace
                if regex:
                    neg_search_regex = re.compile(neg_search, re.IGNORECASE | re.DOTALL)
                else:
                    neg_search_regex = re.compile(re.escape(neg_search), re.IGNORECASE | re.DOTALL)

                # If title (and optionally body) do not contain the negation search, add to filtered issues
                if search_in_body:
                    if not neg_search_regex.search(title) and not neg_search_regex.search(body):
                        filtered_issues.append(issue)
                else:
                    if not neg_search_regex.search(title):
                        filtered_issues.append(issue)
            else:
                # Regular search: add to filtered issues if title or body matches the search
                if search_in_body:
                    if search_regex.search(title) or search_regex.search(body):
                        filtered_issues.append(issue)
                else:
                    if search_regex.search(title):
                        filtered_issues.append(issue)

        issues = filtered_issues
    except re.error as e:
        console = Console()
        console.print(f"[red]Invalid regex pattern: {e}[/red]")
        return []
    return issues


#
# List GitHub issues
#
@app.command()
def list_issues(
    assignee:        Optional[str] = typer.Option(None,      "-a", "--assignee",  help="Filter by assignee"),
    author:          Optional[str] = typer.Option(None,      "-A", "--author",    help="Filter by author"),
    label:     Optional[List[str]] = typer.Option(None,      "-l", "--label",     help="Filter by label(s)"),
    limit:                     int = typer.Option(100,       "-L", "--limit",     help="Maximum number of issues to fetch"),
    mention:         Optional[str] = typer.Option(None,            "--mention",   help="Filter by mention"),
    milestone:       Optional[str] = typer.Option(None,      "-m", "--milestone", help="Filter by milestone number or title"),
    search:          Optional[str] = typer.Option(None,      "-s", "--search",    help="Search issues with query (supports regex)"),
    search_in_body:           bool = typer.Option(False,     "-b", "--body",      help="Search in Body"),
    regex:                    bool = typer.Option(False,     "-R", "--regex",     help="Use regex for searching"),
    state:                     str = typer.Option("open",    "-S", "--state",     help="Filter by state: {open|closed|all}"),
    web:                      bool = typer.Option(False,     "-w", "--web",       help="List issues in the web browser"),
    sort_by:                   str = typer.Option("updated", "-o", "--order-by",  help="Sort issues by: created, updated"),
    order:                     str = typer.Option("asc",     "-O", "--order",     help="Sort order: asc or desc"),
    involved:                 bool = typer.Option(False,     "-i", "--involved",  help="Show only issues where you are involved"),
    columns:   Optional[List[str]] = typer.Option(None,      "-c", "--column",    help="Specify columns to display"),
    use_login:                bool = typer.Option(False,     "-L", "--use-login", help="Use login instead of name for author and assignees"),
):
    """
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
    """
    # Define default columns
    default_columns = ["number", "state", "labels", "updatedAt", "author", "title", "url"]

    # Use default columns if no columns are specified
    if columns is None:
        columns = default_columns

    if web:
        # Get the current repository URL
        try:
            repo_url = subprocess.run(["gh", "repo", "view", "--json", "url"], capture_output=True, text=True, check=True)
            repo_data = json.loads(repo_url.stdout)
            base_url = f"{repo_data['url']}/issues"
        except subprocess.CalledProcessError:
            console = Console()
            console.print("[red]Error: Unable to determine the current repository URL.[/red]")
            return

        # Construct the GitHub web URL with parameters
        params = []
        if assignee:
            params.append(f"assignee={assignee}")
        if author:
            params.append(f"author={author}")
        if label:
            params.extend([f"label={l}" for l in label])
        if mention:
            params.append(f"mentions={mention}")
        if milestone:
            params.append(f"milestone={milestone}")
        if search:
            params.append(f"q={urllib.parse.quote(search)}")
        if sort_by:
            params.append(f"sort={sort_by}")
        if order:
            params.append(f"direction={order}")
        params.append(f"state={state}")

        url = f"{base_url}?{'&'.join(params)}"
        typer.launch(url)
        return

    try:
        # Construct the gh issue list command
        cmd = ["gh", "issue", "list", "--json", "number,title,state,labels,createdAt,updatedAt,author,assignees,comments,body,closed,closedAt,url"]

        if assignee:
            cmd.extend(["--assignee", assignee])
        if author:
            cmd.extend(["--author", author])
        if label:
            for l in label:
                cmd.extend(["--label", l])
        if mention:
            cmd.extend(["--mention", mention])
        if milestone:
            cmd.extend(["--milestone", milestone])
        if involved:
            cmd.extend(["--search", "involves:@me"])
        cmd.extend(["--state", state])

        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(result.stdout)

        # Client-side filtering based on search term (now supports regex)
        if search:
            issues =  perform_search(search, issues, regex, search_in_body)

        # Sort issues
        if sort_by:
            sort_by = sort_by.lower()
            if sort_by == "created":
                issues.sort(key=lambda x: x.get('createdAt', ''), reverse=(order == "desc"))
            elif sort_by == "updated":
                issues.sort(key=lambda x: x.get('updatedAt', ''), reverse=(order == "desc"))
            elif sort_by == "title":
                issues.sort(key=lambda x: x.get('title', ''), reverse=(order == "desc"))
            elif sort_by == "number" or sort_by == "id":
                issues.sort(key=lambda x: x.get('ID', ''), reverse=(order == "desc"))

        # Limit the number of issues
        issues = issues[:limit]

        # Create and populate the table
        table = Table(title="GitHub Issues")
        for column in columns:
            if column in ['number', 'state']:
                table.add_column(column.capitalize(), style="cyan", no_wrap=True, overflow='fold', min_width=6)
            elif column == 'url':
                table.add_column(column.capitalize(), style="cyan", no_wrap=True, overflow='fold', min_width=61)
            elif column == 'title':
                table.add_column(column.capitalize(), style="cyan", no_wrap=True, overflow='ellipsis', max_width=76)
            elif column == 'lables':
                table.add_column(column.capitalize(), style="cyan", no_wrap=False, overflow='ellipsis', max_width=10)
            else:
                table.add_column(column.capitalize(), style="cyan", no_wrap=True)

        for issue in issues:
            row = []
            for column in columns:
                if column == 'labels':
                    labels_text = Text()
                    for label in issue.get('labels', []):
                        color = LABEL_COLORS.get(label['name'].lower(), "#FFFFFF")
                        label_style = f"on {color}"
                        if color == "#FFFFFF":
                            label_style += " black"
                        labels_text.append(f" {label['name']:^20} ", style=label_style)
                    row.append(labels_text)
                elif column in ['createdAt', 'updatedAt', 'closedAt']:
                    row.append(format_date(issue.get(column)))
                elif column == 'author':
                    row.append(format_author(issue.get('author'), use_login))
                elif column == 'assignees':
                    row.append(format_assignees(issue.get('assignees'), use_login))
                elif column == 'body':
                    body = issue.get('body', '')
                    row.append(body[:100] + '...' if len(body) > 100 else body)
                else:
                    row.append(str(issue.get(column, '')))
            table.add_row(*row)

        # Display the table
        console = Console()
        console.print(table)

        # Print the total number of issues found
        console.print(f"\nTotal issues found: {len(issues)}")

    except subprocess.CalledProcessError as e:
        console = Console()
        console.print(f"[red]Error: {e.stderr}[/red]")
    except Exception as e:
        console = Console()
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print(f"[red]Error type: {type(e).__name__}[/red]")

@app.command()
def clone_issue(
    issue_number:              int = typer.Argument(..., help="The number of the issue to clone"),
    empty_checkboxes:         bool = typer.Option  (True,  "--empty-checkboxes/--keep-checkboxes", help="Empty checkboxes in the description"),
    replace:         Optional[str] = typer.Option  (None,  "-s", "--search",                       help="String or regex pattern to replace in the title"),
    with_str:        Optional[str] = typer.Option  (None,  "-r", "--replace",                      help="String to replace with in the title"),
    regex:                    bool = typer.Option  (True,  "-R", "--regex",                        help="Use regex for string replacement in title"),
    new_title:       Optional[str] = typer.Option  (None,  "-t", "--title",                        help="Replace the entire title with a new one"),
    keep_assignees:           bool = typer.Option  (True,  "-A", "--keep-assignees",               help="Keep the original assignees"),
    assignees: Optional[List[str]] = typer.Option  (None,  "-a", "--assignee",                     help="List of assignees to add to the new issue")
):
    """
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
    """
    try:
        console = Console()
        # Fetch the original issue details
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number), "--json", "title,body,labels,assignees"],
            capture_output=True, text=True, check=True
        )
        issue_data = json.loads(result.stdout)

        # Modify the body to empty checkboxes if requested
        if empty_checkboxes:
            issue_data['body'] = re.sub(r'\[x\]', '[ ]', issue_data['body'])

        # Handle title replacement
        if new_title:
            issue_data['title'] = new_title
        elif replace and with_str:
            if regex:
                try:
                    issue_data['title'] = re.sub(replace, with_str, issue_data['title'])
                except re.error as e:
                    console.print(f"[red]Invalid regex pattern: {e}[/red]")
                    return
            else:
                issue_data['title'] = issue_data['title'].replace(replace, with_str)

        # Prepare the new issue creation command
        create_cmd = [
            "gh", "issue", "create",
            "--title", issue_data['title'],
            "--body", issue_data['body']
        ]

        # Add labels
        for label in issue_data['labels']:
            create_cmd.extend(["--label", label['name']])  # Fixed missing closing bracket

        # Handle assignees
        if keep_assignees:
            for assignee in issue_data['assignees']:
                create_cmd.extend(["--assignee", assignee['login']])
        elif assignees:
            for assignee in assignees:
                create_cmd.extend(["--assignee", assignee])
        else:
            # If no assignees specified and not keeping original, assign to current user
            create_cmd.extend(["--assignee", "@me"])

        # Create the new issue
        result = subprocess.run(create_cmd, capture_output=True, text=True, check=True)
        new_issue_url = result.stdout.strip()
        new_issue_number = new_issue_url.split('/')[-1]

        console.print(f"[green]Created new issue: {new_issue_url}[/green]")

        # Fetch comments from the original issue
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number), "--comments"],
            capture_output=True, text=True, check=True
        )
        comments = result.stdout.strip().split('\n\n')

        # Add comments to the new issue
        for comment in comments:
            if comment.strip():  # Check if the comment is not empty
                try:
                    # Extract the comment body (everything after the first newline)
                    comment_parts = comment.split('\n', 1)
                    if len(comment_parts) > 1:
                        comment_body = comment_parts[1].strip()
                        comment_cmd = ["gh", "issue", "comment", new_issue_number, "--body", comment_body]
                        subprocess.run(comment_cmd, check=True, capture_output=True, text=True)
                    else:
                        console.print(f"[yellow]Warning: Skipping comment due to unexpected format: {comment}[/yellow]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Error adding comment: {e.stderr}[/red]")
                    console.print(f"[red]Command that failed: {' '.join(comment_cmd)}[/red]")

        console.print(f"[green]Cloned issue #{issue_number} to #{new_issue_number} with all comments[/green]")

    except subprocess.CalledProcessError as e:
        console = Console()
        console.print(f"[red]Error: {e.stderr}[/red]")
        console.print(f"[red]Command that failed: {' '.join(e.cmd)}[/red]")
    except Exception as e:
        console = Console()
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print(f"[red]Error type: {type(e).__name__}[/red]")
        import traceback
        console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")



@app.command()
def issue_doc(
    issue_number: int,
    max_depth: int = typer.Option(1, "-d", "--depth", help="Maximum depth to traverse"),
    max_issues: Optional[int] = typer.Option(None, "-m", "--max", help="Maximum number of issues to process"),
    output: str = typer.Option("issue_doc.docx", "-o", "--output", help="Output file name"),
    include_comments: bool = typer.Option(False, "-c", "--comments", help="Include issue comments")
):
    """Generate documentation from GitHub issues."""
    doc_generator = IssueDocGenerator()
    doc = doc_generator.generate_doc(issue_number, max_depth, max_issues, include_comments)
    doc.save(output)
    console.print(f"Documentation generated successfully: {output}")


@app.command()
def log(
    limit:     Optional[int] = typer.Option(None,  "-n", "--limit",     help="Limit the number of commits to show"),
    all:              bool   = typer.Option(False, "-a", "--all",       help="Show all branches"),
    no_merges:        bool   = typer.Option(True,  "-m", "--no-merges", help="Exclude merge commits"),
    search:    Optional[str] = typer.Option(None,  "-s", "--search",    help="Search pattern (in messages or code if -c is used)"),
    code_search:      bool   = typer.Option(False, "-c", "--code-search", help="Search within code changes instead of commit messages"),
    files:     Optional[str] = typer.Option(None,  "-f", "--files",     help="Restrict code search to files matching pattern (e.g. '*.py,*.sql')"),
    author:    Optional[str] = typer.Option(None,  "-u", "--author",    help="Filter by author"),
    branch:    Optional[str] = typer.Option(None,  "-b", "--branch",    help="Show commits from specific branch"),
    page_size:         int   = typer.Option(20,    "-p", "--page-size", help="Number of commits per page")
):
    """
    Show commit history in a paginated table with clickable links.
    """
    try:
        # Get repository URL for clickable links
        repo_url = git_wrapper.get_remote_url()
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]

        # Build git log command
        log_format = '%C(yellow)%h%C(red)%d %cr %C(reset)%s%C(blue) [%cn]'
        cmd = ['log', f'--pretty=format:{log_format}', '--decorate']

        if no_merges:
            cmd.append('--no-merges')
        if all:
            cmd.append('--all')
        if limit:
            cmd.extend(['-n', str(limit)])
        if search:
            if code_search:
                # Search in code changes
                cmd.extend(['-S', search, '--pickaxe-regex'])
                if files:
                    # Add file patterns to search
                    for pattern in files.split(','):
                        cmd.extend(['--', pattern.strip()])
            else:
                # Search in commit messages
                cmd.extend(['--grep', search, '--regexp-ignore-case', '--extended-regexp'])
        if author:
            cmd.extend(['--author', author])
        if branch:
            cmd.append(branch)

        # Show spinner while getting commits
        with console.status("[bold green]Searching commits...") as status:
            # Get commit history
            log_output = git_wrapper.execute_git_command(cmd)
            commits = log_output.strip().split('\n')

            if not commits or commits[0] == '':
                console.print("[yellow]No commits found.[/yellow]")
                return

            status.update("[bold green]Processing results...")

        # Calculate total pages
        total_commits = len(commits)
        total_pages = math.ceil(total_commits / page_size)
        current_page = 1

        while True:
            # Create and populate the table
            table = Table(
                title=f"Git History (Page {current_page}/{total_pages})",
                show_lines=True
            )
            table.add_column("Hash", style="yellow", no_wrap=True)
            table.add_column("Time", style="green")
            table.add_column("Message", style="white")  # Removed expand parameter
            table.add_column("Author", style="blue")
            table.add_column("Branches/Tags", style="red")

            # Calculate slice for current page
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, total_commits)

            for commit in commits[start_idx:end_idx]:
                # Parse commit info using regex for better accuracy
                import re

                # Updated pattern to handle various time formats and better message separation
                pattern = r'([a-f0-9]+)(\s*(?:\(([^)]+)\))?)?\s+((?:\d+\s+(?:year|month|week|day|hour|minute|second)s?,?\s*)+ago)\s+(.+?)\s+\[([^\]]+)\]'
                match = re.match(pattern, commit)

                if match:
                    hash_part = match.group(1)
                    decorations = match.group(3) or ""
                    time_part = match.group(4).strip()
                    msg_part = match.group(5).strip()
                    author_part = match.group(6)

                    # Create clickable hash
                    commit_url = f"{repo_url}/commit/{hash_part}"
                    hash_text = Text(hash_part, style="link " + commit_url)

                    table.add_row(
                        hash_text,
                        time_part,
                        msg_part,
                        author_part,
                        decorations
                    )
                else:
                    # Improved fallback for unmatched formats
                    # Try to at least get the hash
                    hash_match = re.match(r'([a-f0-9]+)', commit)
                    if hash_match:
                        hash_part = hash_match.group(1)
                        hash_text = Text(hash_part, style="link " + f"{repo_url}/commit/{hash_part}")
                        table.add_row(hash_text, "", commit, "", "")
                    else:
                        table.add_row("", "", commit, "", "")

            # Clear screen and show table
            console.clear()
            console.print(table)

            # Navigation options
            if total_pages > 1:
                console.print("\nNavigation: \\[n]ext page, \\[p]revious page, \\[q]uit, or click commit hash to view on GitHub")
                key = inquirer.text(
                    message="Enter option:",
                    validate=lambda x: x.lower() in ['n', 'p', 'q', '']
                ).execute()

                if key.lower() == 'n' and current_page < total_pages:
                    current_page += 1
                elif key.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif key.lower() in ['q', '']:  # Added empty string to handle Enter key
                    break
            else:
                console.print("\nPress Enter to exit, or click commit hash to view on GitHub")
                inquirer.text(message="").execute()  # Removed the if condition to exit on any input
                break

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


# Add this command after the 'mv' command and before the 'add' command

@app.command()
def comment(
    branch: Optional[str] = typer.Argument(None, help="The branch to comment on"),
    message: Optional[str] = typer.Option(None, "-m", "--message", help="The comment to set"),
    list: bool = typer.Option(False, "-l", "--list", help="List all branch comments"),
    delete: bool = typer.Option(False, "-d", "--delete", help="Delete the comment for the specified branch")
):
    """
    Set, get, list or delete comments for branches.

    Parameters:
    - branch : The branch to comment on. If not specified, uses current branch.
    - message: The comment to set. If not specified, shows current comment.
    - list   : List all branch comments.
    - delete : Delete the comment for the specified branch.

    Examples:
    - Set a comment for current branch:
        ./gitflow.py comment -m "Feature branch for UI redesign"
    - Set a comment for specific branch:
        ./gitflow.py comment feature/new-ui -m "UI redesign implementation"
    - View comment for current branch:
        ./gitflow.py comment
    - View comment for specific branch:
        ./gitflow.py comment feature/new-ui
    - List all branch comments:
        ./gitflow.py comment --list
    - Delete comment for current branch:
        ./gitflow.py comment --delete
    """
    try:
        git_wrapper = GitWrapper()

        if list:
            comments = git_wrapper.get_all_branch_comments()
            if comments:
                table = Table(title="Branch Comments")
                table.add_column("Branch", style="cyan")
                table.add_column("Comment", style="green")

                for branch_name, comment in comments.items():
                    table.add_row(branch_name, comment)

                console.print(table)
            else:
                console.print("[yellow]No branch comments found.[/yellow]")
            return

        # If no branch specified, use current branch
        if not branch:
            branch = git_wrapper.get_current_branch()

        if delete:
            # Delete comment by setting it to empty string
            git_wrapper.set_branch_comment(branch, "")
            console.print(f"[green]Deleted comment for branch '{branch}'[/green]")
            return

        if message:
            # Set new comment
            git_wrapper.set_branch_comment(branch, message)
        else:
            # Show current comment
            comment = git_wrapper.get_branch_comment(branch)
            if comment:
                console.print(f"[green]Comment for branch '{branch}':[/green] {comment}")
            else:
                console.print(f"[yellow]No comment found for branch '{branch}'[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Issue commands
#
@app.command()
def manage_issues(
    search:        Optional[str] = typer.Option(None,        "--search",       help="Search issues by title (supports regex)"),
    regex:                  bool = typer.Option(False, "-R", "--regex",       help="Use regex for searching"),
    state:                  str  = typer.Option(None,  "-s", "--state",       help="Set issue state (open/closed)"),
    current_state:          str  = typer.Option(None,  "-c", "--current-state", help="Only match issues in this state (open/closed)"),
    rename:         Optional[str] = typer.Option(None,       "--rename",      help="Rename matching issues (format: search:replace)"),
    regex_rename:           bool = typer.Option(False,       "--regex-rename", help="Use regex for renaming"),
    dry_run:               bool = typer.Option(False, "-d", "--dry-run",     help="Show what would be done without making changes"),
    list_only:             bool = typer.Option(False, "-l", "--list",        help="Only list matching issues without modifying"),
    limit:                  int  = typer.Option(10000,       "--limit",       help="Maximum number of issues to process"),
):
    r"""
    Manage GitHub issues - list, open, close, or rename issues matching a search pattern.

    Examples:
    - List issues matching a pattern:
        gf manage-issues --search "Cleanup Rules" --list

    - Close all open issues matching a pattern:
        gf manage-issues --search "Cleanup Rules" -s closed -c open

    - Open all closed issues matching a regex:
        gf manage-issues --search "^PROJ-\d+" --regex -s open -c closed

    - Rename issues (replace text):
        gf manage-issues --search "Manual Imports:" --rename "Manual Imports : "

    - Rename issues using regex:
        gf manage-issues --search "Manual Imports" --rename "CW(\d+):CW0\1" --regex-rename

    - Preview renaming without making changes:
        gf manage-issues --search "Manual Imports" --rename "CW(\d+):CW0\1" --regex-rename --dry-run
    """
    try:
        # Get all issues and filter by search
        cmd = ["gh", "issue", "list",
               "--json", "number,title,labels,state",
               "--state", "all",
               "--limit", "10000"]  # Increased limit significantly
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(result.stdout)

        # Respect the user's limit if specified
        if limit and len(issues) > limit:
            issues = issues[:limit]

        # Filter issues by title using regex or plain text
        try:
            if regex:
                pattern = re.compile(search, re.IGNORECASE)
            else:
                pattern = re.compile(re.escape(search), re.IGNORECASE)

            filtered_issues = [issue for issue in issues
                     if pattern.search(issue['title'])]

            # Filter by current state if specified
            if current_state:
                current_state = current_state.upper()
                filtered_issues = [issue for issue in filtered_issues
                         if issue['state'].upper() == current_state]

        except re.error as e:
            console.print(f"[red]Invalid regex pattern: {e}[/red]")
            return

        if not filtered_issues:
            console.print("[yellow]No matching issues found[/yellow]")
            return

        # Handle renaming first if specified
        if rename:
            table = Table(title="Preview of Issue Renaming")
            table.add_column("Number", style="cyan")
            table.add_column("Current Title", style="yellow")
            table.add_column("New Title", style="green")

            changes_found = False
            for issue in filtered_issues:
                current_title = issue['title']
                if regex_rename:
                    try:
                        new_title = re.sub(search, rename, current_title)
                    except re.error as e:
                        console.print(f"[red]Invalid regex pattern: {e}[/red]")
                        return
                else:
                    new_title = current_title.replace(search, rename)

                if new_title != current_title:
                    changes_found = True
                    table.add_row(
                        f"#{issue['number']}",
                        current_title,
                        new_title
                    )

            if changes_found:
                console.print(table)
                if dry_run:
                    console.print("\n[yellow]This was a dry run. No changes were made.[/yellow]")
                    return

                # Confirm before modifying issues
                if not inquirer.confirm(
                    message=f"Are you sure you want to rename these issues?",
                    default=False
                ).execute():
                    console.print("[yellow]Operation cancelled.[/yellow]")
                    return

                # Perform the renaming
                for issue in filtered_issues:
                    try:
                        current_title = issue['title']
                        if regex_rename:
                            new_title = re.sub(search, rename, current_title)
                        else:
                            new_title = current_title.replace(search, rename)

                        if new_title != current_title:
                            cmd = ["gh", "issue", "edit", str(issue['number']), "--title", new_title]
                            subprocess.run(cmd, check=True, capture_output=True)
                            console.print(f"[green]Renamed issue #{issue['number']}:[/green] {current_title} -> {new_title}")
                    except subprocess.CalledProcessError as e:
                        console.print(f"[red]Error renaming issue #{issue['number']}: {e.stderr}[/red]")
            else:
                console.print("[yellow]No changes would be made with this pattern.[/yellow]")
            return

        # Display matching issues (only if not renaming)
        table = Table(title=f"Matching Issues")
        table.add_column("Number", style="cyan")
        table.add_column("Title")
        table.add_column("Labels", style="magenta")
        table.add_column("State", style="green")

        for issue in filtered_issues:
            table.add_row(
                f"#{issue['number']}",
                issue['title'],
                ", ".join(label['name'] for label in issue['labels']),
                issue['state']
            )

        console.print(table)
        console.print(f"\nTotal issues found: {len(filtered_issues)}")

        # If only listing or no state change requested, return here
        if list_only or not state:
            return

        # Validate state transition
        if current_state and current_state.upper() == state.upper():
            console.print(f"[yellow]Issues are already in {state} state[/yellow]")
            return

        # Confirm before modifying issues
        if not inquirer.confirm(
            message=f"Are you sure you want to {state} {len(filtered_issues)} issues?",
            default=False
        ).execute():
            console.print("[yellow]Operation cancelled.[/yellow]")
            return

        # Update issue states
        for issue in filtered_issues:
            try:
                if state.lower() == 'closed':
                    cmd = ["gh", "issue", "close", str(issue['number'])]
                else:
                    cmd = ["gh", "issue", "reopen", str(issue['number'])]
                subprocess.run(cmd, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Error updating issue #{issue['number']}: {e.stderr}[/red]")

        console.print(f"[green]Successfully {state}d {len(filtered_issues)} issues[/green]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


#
# Label commands
#
@app.command()
def manage_labels(
    labels:           List[str] = typer.Option(None, "-l",  "--label",  help="Labels to filter/modify issues"),
    add_labels:       List[str] = typer.Option(None, "-a",  "--add",    help="Labels to add to matching issues"),
    remove_labels:    List[str] = typer.Option(None, "-r",  "--remove", help="Labels to remove from matching issues"),
    rename:      Optional[str]  = typer.Option(None,       "--rename", help="Rename a label (format: old_name:new_name)"),
    create:           List[str] = typer.Option(None, "-c",  "--create", help="Create new labels (format: name:color[:description])"),
    delete:           List[str] = typer.Option(None,       "--delete", help="Delete labels"),
    list_labels:           bool = typer.Option(False,       "--list",   help="List all repository labels"),
    state:                 str  = typer.Option("all", "-s", "--state",  help="Issue state to filter by (open/closed/all)"),
    search:       Optional[str] = typer.Option(None,        "--search", help="Search issues by title (supports regex)"),
    regex:                 bool = typer.Option(False, "-R", "--regex",  help="Use regex for searching"),
    dry_run:              bool = typer.Option(False, "-d", "--dry-run", help="Show what would be done without making changes"),
):
    r"""
    Manage GitHub issue labels - list, create, add, remove, or rename labels.

    Examples:
    - List all repository labels:
        gf manage-labels --list

    - Create new labels (with preview):
        gf manage-labels -c "bug:ff0000:Bug reports" -c "feature:00ff00" --dry-run

    - Rename a label (with preview):
        gf manage-labels --rename "old-name:new-name" --dry-run

    - Delete labels (with preview):
        gf manage-labels --delete old-label --dry-run

    - Preview label changes for matching issues:
        gf manage-labels --search "Manual Imports" --regex -r old-label -a new-label --dry-run

    - Apply label changes to matching issues:
        gf manage-labels --search "Manual Imports" --regex -r old-label -a new-label

    All operations support:
    - Previewing changes with --dry-run
    - Regex search patterns with --regex
    - Before/after preview tables
    - Confirmation prompts
    - Progress feedback
    """
    try:
        git = GitWrapper()

        # List all labels
        if list_labels:
            labels_data = git.get_repo_labels()
            table = Table(title="Repository Labels")
            table.add_column("Name", style="cyan")
            table.add_column("Color", style="magenta")
            table.add_column("Description")

            for label in labels_data:
                table.add_row(
                    label['name'],
                    f"#{label['color']}",
                    label.get('description', '')
                )

            console.print(table)
            return

        # Create new labels
        if create:
            # First show preview
            table = Table(title="Label Creation Preview")
            table.add_column("Name", style="cyan")
            table.add_column("Color", style="magenta")
            table.add_column("Description", style="green")

            labels_to_create = []  # Store parsed labels
            for label_spec in create:
                parts = label_spec.split(':', 2)
                name = parts[0]
                color = parts[1] if len(parts) > 1 else "cccccc"
                description = parts[2] if len(parts) > 2 else ""

                labels_to_create.append((name, color, description))
                table.add_row(name, f"#{color}", description)

            console.print(table)
            if dry_run:
                console.print("\n[yellow]This was a dry run. No labels were created.[/yellow]")
                return

            if not inquirer.confirm(
                message=f"Are you sure you want to create these labels?",
                default=False
            ).execute():
                console.print("[yellow]Operation cancelled.[/yellow]")
                return

            # Then create the labels using stored data
            for name, color, description in labels_to_create:
                git.create_label(name, color, description)
                console.print(f"[green]Created label '{name}'[/green]")

        # Get issues either by labels or search
        issues = []
        if labels:
            issues = git.list_issues_by_label(labels, state)
        elif search:
            # Get all issues and filter by search
            cmd = ["gh", "issue", "list",
                  "--json", "number,title,labels,state",
                  "--state", state,
                  "--limit", "10000"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            all_issues = json.loads(result.stdout)

            # Filter issues by title using regex or plain text
            try:
                if regex:
                    pattern = re.compile(search, re.IGNORECASE)
                else:
                    pattern = re.compile(re.escape(search), re.IGNORECASE)

                issues = [issue for issue in all_issues
                         if pattern.search(issue['title'])]
            except re.error as e:
                console.print(f"[red]Invalid regex pattern: {e}[/red]")
                return

        if issues:
            if add_labels or remove_labels:
                # Show preview of label changes
                table = Table(title="Label Changes Preview")
                table.add_column("Number", style="cyan")
                table.add_column("Title")
                table.add_column("Current Labels", style="yellow")
                table.add_column("New Labels", style="green")

                for issue in issues:
                    current_labels = {label['name'] for label in issue['labels']}
                    new_labels = current_labels.copy()

                    if add_labels:
                        new_labels.update(add_labels)
                    if remove_labels:
                        new_labels.difference_update(remove_labels)

                    if new_labels != current_labels:
                        table.add_row(
                            f"#{issue['number']}",
                            issue['title'],
                            ", ".join(sorted(current_labels)),
                            ", ".join(sorted(new_labels))
                        )

                console.print(table)
                if dry_run:
                    console.print("\n[yellow]This was a dry run. No labels were modified.[/yellow]")
                    return

                if not inquirer.confirm(
                    message=f"Are you sure you want to modify labels for these issues?",
                    default=False
                ).execute():
                    console.print("[yellow]Operation cancelled.[/yellow]")
                    return

                # Perform the label modifications
                for issue in issues:
                    if add_labels:
                        git.add_labels_to_issue(issue['number'], add_labels)
                    if remove_labels:
                        git.remove_labels_from_issue(issue['number'], remove_labels)
                    console.print(f"[green]Updated labels for issue #{issue['number']}[/green]")

            else:
                # Just display the matching issues
                table = Table(title=f"Matching Issues")
                table.add_column("Number", style="cyan")
                table.add_column("Title")
                table.add_column("Labels", style="magenta")
                table.add_column("State", style="green")

                for issue in issues:
                    table.add_row(
                        f"#{issue['number']}",
                        issue['title'],
                        ", ".join(label['name'] for label in issue['labels']),
                        issue['state']
                    )

                console.print(table)
                console.print(f"\nTotal issues found: {len(issues)}")

        else:
            console.print("[yellow]No matching issues found[/yellow]")

        # Handle label rename
        if rename:
            old_name, new_name = rename.split(':', 1)
            # Show preview
            table = Table(title="Label Rename Preview")
            table.add_column("Current Name", style="yellow")
            table.add_column("New Name", style="green")
            table.add_row(old_name, new_name)

            console.print(table)
            if dry_run:
                console.print("\n[yellow]This was a dry run. No labels were renamed.[/yellow]")
                return

            if not inquirer.confirm(
                message=f"Are you sure you want to rename label '{old_name}' to '{new_name}'?",
                default=False
            ).execute():
                console.print("[yellow]Operation cancelled.[/yellow]")
                return

            git.rename_label(old_name, new_name)
            console.print(f"[green]Renamed label '{old_name}' to '{new_name}'[/green]")
            return

        # Handle label deletion
        if delete:
            table = Table(title="Label Deletion Preview")
            table.add_column("Label", style="red")
            table.add_column("Description", style="yellow")

            labels_data = git.get_repo_labels()
            labels_to_delete = []
            for label_name in delete:
                for label in labels_data:
                    if label['name'] == label_name:
                        labels_to_delete.append(label)
                        table.add_row(label['name'], label.get('description', ''))
                        break

            console.print(table)
            if dry_run:
                console.print("\n[yellow]This was a dry run. No labels were deleted.[/yellow]")
                return

            if not inquirer.confirm(
                message=f"Are you sure you want to delete these labels?",
                default=False
            ).execute():
                console.print("[yellow]Operation cancelled.[/yellow]")
                return

            for label in labels_to_delete:
                git.delete_label(label['name'])
                console.print(f"[green]Deleted label '{label['name']}'[/green]")
            return

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")



#
# Worktree commands
#
worktree_app = typer.Typer(help="Manage Git worktrees")
app.add_typer(worktree_app, name="worktree")

@worktree_app.command(name="ls")
def worktree_ls():
    """
    List all worktrees in the repository.
    """
    try:
        result = git_wrapper.list_worktrees()
        # Create a table for better formatting
        table = Table(title="Git Worktrees")
        table.add_column("Path", style="cyan")
        table.add_column("Branch", style="green")
        table.add_column("Commit", style="yellow")

        # Parse the worktree list output
        for line in result.split('\n'):
            if line.strip():
                if '[main-worktree]' in line:
                    continue
                parts = line.split()
                path = parts[0]
                commit = parts[1] if len(parts) > 1 else ""
                # Look for [branch_name] pattern in the output
                branch = ""
                for part in parts[2:]:  # Start from third part
                    if part.startswith('[') and part.endswith(']'):
                        branch = part[1:-1]  # Remove brackets
                        break
                table.add_row(path, branch, commit)

        console.print(table)
    except GitCommandError as e:
        console.print(f"[red]Error listing worktrees: {e}[/red]")

@worktree_app.command(name="add")
def worktree_add(
    branch: str = typer.Argument(..., help="Branch to checkout or create"),
    path: str = typer.Argument(..., help="Path where to create the worktree")
):
    """
    Add a new worktree.

    If the branch doesn't exist, it will be created from the current HEAD.
    If the branch exists in another worktree or main repo, you'll be offered to move it.
    The path should be relative to the current repository root or absolute.

    Example:
        gf worktree add feature/test ../tc-worktrees/test
    """
    try:
        # Check if branch exists in a worktree
        is_worktree, existing_path = git_wrapper.is_worktree(branch)
        main_repo = os.path.realpath(git_wrapper.repo.working_dir)
        current_branch = git_wrapper.get_current_branch()

        # Clean up any existing temp branches and worktrees at the target path
        if os.path.exists(path):
            try:
                git_wrapper.remove_worktree(path, force=True)
            except GitCommandError:
                pass
            try:
                shutil.rmtree(path)
            except (OSError, IOError):
                pass

        # Clean up any existing temp branches
        for b in git_wrapper.get_branches():
            branch_name = b.name
            if branch_name.startswith('_gf_temp_'):
                try:
                    git_wrapper.delete_branch(branch_name, quiet=True)  # Add quiet parameter to GitWrapper
                except GitCommandError:
                    pass

        if is_worktree or (branch == current_branch and os.path.realpath(os.getcwd()) == main_repo):
            is_main = os.path.realpath(existing_path) == main_repo if is_worktree else True
            location = "main repository" if is_main else f"worktree at {existing_path}"

            # Ask if user wants to move the branch to new worktree
            console.print(f"[yellow]Branch '{branch}' is already used in {location}[/yellow]")
            move = inquirer.confirm(
                message="Would you like to move it to the new location?",
                default=True
            ).execute()

            if move:
                # If we're currently on the branch we want to move, switch to develop first
                if current_branch == branch:
                    git_wrapper.checkout('develop')
                    console.print("[green]Switched to develop branch temporarily[/green]")

                # Now create the worktree with the branch directly
                git_wrapper.add_worktree(path, branch)
                console.print(f"[green]Successfully moved worktree for {branch} to {path}[/green]")

                # If it was in another worktree (not main), remove that worktree
                if not is_main and existing_path != main_repo:
                    git_wrapper.remove_worktree(existing_path, force=True)
                    console.print(f"[green]Removed old worktree at {existing_path}[/green]")

                return
            else:
                console.print("[yellow]Operation cancelled.[/yellow]")
                return

        # Check if branch exists
        if branch not in git_wrapper.get_branches():
            # Create branch from current HEAD
            current = git_wrapper.get_current_branch()
            console.print(f"[yellow]Branch '{branch}' doesn't exist, creating from {current}[/yellow]")
            git_wrapper.create_branch(branch)

        # Now create the worktree
        result = git_wrapper.add_worktree(path, branch)
        console.print(f"[green]Successfully created worktree at {path}[/green]")
        if result:
            console.print(result)
    except GitCommandError as e:
        console.print(f"[red]Error adding worktree: {e}[/red]")
        # Try to clean up on error
        try:
            if os.path.exists(path):
                git_wrapper.remove_worktree(path, force=True)
                shutil.rmtree(path)
        except:
            pass

@worktree_app.command(name="rm")
def worktree_rm(
    path_or_branch: Optional[str] = typer.Argument(None, help="Path of the worktree or branch name to remove"),
    force: bool = typer.Option(False, "-f", "--force", help="Force removal even with uncommitted changes")
):
    try:
        # Get main repo path - get it directly from git_wrapper
        main_repo = os.path.realpath(git_wrapper.get_repo_root())
        current_dir = os.path.realpath(os.getcwd())

        # Get list of worktrees
        worktree_output = git_wrapper.list_worktrees()

        # Find the main repo path from worktree list
        for line in worktree_output.split('\n'):
            if line.strip() and '[main-worktree]' in line:
                main_repo = os.path.realpath(line.split()[0])
                break

        # Parse worktree list and exclude main working tree
        choices = []
        for line in worktree_output.split('\n'):
            if line.strip() and '[main-worktree]' not in line:
                parts = line.split()
                path = parts[0]
                # Look for [branch_name] pattern
                branch = None
                for part in parts[2:]:
                    if part.startswith('[') and part.endswith(']'):
                        branch = part[1:-1]
                        break
                if branch:
                    choices.append(f"{branch} ({path})")

        if not choices:
            console.print("[yellow]No removable worktrees found.[/yellow]")
            return

        # Let user select which worktree to remove
        if not path_or_branch:
            selected = inquirer.select(
                message="Select worktree to remove:",
                choices=choices
            ).execute()
            if not selected:
                console.print("\nAborted.")
                return
            path = selected.split('(')[1].rstrip(')')
            branch = selected.split(' (')[0]
        else:
            # Handle direct path/branch input
            is_worktree, worktree_path = git_wrapper.is_worktree(path_or_branch)
            if is_worktree:
                path = worktree_path
            else:
                path = path_or_branch

            # Get branch name from worktree info
            for line in worktree_output.split('\n'):
                if path in line:
                    for part in line.split()[2:]:
                        if part.startswith('[') and part.endswith(']'):
                            branch = part[1:-1]
                            break

        # Remove the worktree
        git_wrapper.remove_worktree(path, force=force)
        console.print(f"[green]Successfully removed worktree at {path}[/green]")

        # If we were in the removed worktree, suggest changing to main repo
        in_removed_worktree = current_dir.startswith(os.path.realpath(path))
        if in_removed_worktree:
            console.print(f"[yellow]Note: Current directory no longer exists.[/yellow]")
            console.print(f"[yellow]Please run: cd {main_repo}[/yellow]")

        # Move branch back to main repo if it exists
        if branch and branch not in ['HEAD', 'main', 'develop']:
            try:
                # Change to main repo before moving branch
                os.chdir(main_repo)
                git_wrapper.checkout(branch)
                console.print(f"[green]Moved branch '{branch}' back to main repository[/green]")
            except (GitCommandError, OSError) as e:
                console.print(f"[yellow]Note: Could not move branch '{branch}' back: {e}[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error removing worktree: {e}[/red]")

@worktree_app.command(name="prune")
def worktree_prune():
    """
    Prune worktree administrative files with unreachable working trees.
    """
    try:
        result = git_wrapper.repo.git.worktree('prune')
        console.print("[green]Successfully pruned worktree administrative files[/green]")
        if result:
            console.print(result)
    except GitCommandError as e:
        console.print(f"[red]Error pruning worktrees: {e}[/red]")

@worktree_app.command(name="finish")
def worktree_finish(
    delete: bool = typer.Option(True, "-d", "--delete", help="Delete the branch and worktree after finishing"),
    keep_local: bool = typer.Option(False, "-k", "--keep-local", help="Keep the local branch after finishing")
):
    """
    Finish a feature/hotfix/release branch that is in a worktree.
    This will:
    1. Push any pending changes
    2. Remove the worktree
    3. Notify you to finish the branch from the main repository
    """
    try:
        # Get current branch and verify we're in a worktree
        current_branch = git_wrapper.get_current_branch()
        is_worktree, worktree_path = git_wrapper.is_worktree(current_branch)

        if not is_worktree:
            console.print("[red]Error: This command should be run from a worktree, not the main repository[/red]")
            console.print("[yellow]Use 'gf finish' in the main repository instead[/yellow]")
            return 1

        # Get main repository path by finding the worktree that's not us
        worktree_output = git_wrapper.list_worktrees()
        main_repo = None
        for line in worktree_output.split('\n'):
            if line.strip():
                path = line.split()[0]
                if os.path.realpath(path) != os.path.realpath(worktree_path):
                    main_repo = path
                    break

        if not main_repo:
            console.print("[red]Error: Could not find main repository path[/red]")
            return 1

        current_dir = os.path.realpath(os.getcwd())

        # Double check we're actually in the worktree directory
        if current_dir != os.path.realpath(worktree_path):
            console.print(f"[red]Error: Must run this command from the worktree at {worktree_path}[/red]")
            return 1

        # Verify this is a feature/hotfix/release branch
        if not any(current_branch.startswith(prefix) for prefix in ['feature/', 'hotfix/', 'release/']):
            console.print(f"[red]Error: Current branch '{current_branch}' is not a feature, hotfix, or release branch[/red]")
            return 1

        # Push any pending changes
        if not git_wrapper.push_to_remote(current_branch):
            console.print("[yellow]No changes to push[/yellow]")

        # Remove the worktree
        git_wrapper.remove_worktree(worktree_path, force=True)
        console.print(f"[green]Removed worktree at {worktree_path}[/green]")
        console.print("\n[yellow]Note: Current directory no longer exists.[/yellow]")
        console.print(f"[yellow]Please run:[/yellow]")
        console.print(f"[yellow]1. cd {main_repo}[/yellow]")
        console.print(f"[yellow]2. gf checkout {current_branch}[/yellow]")
        console.print(f"[yellow]3. gf finish[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


#
# Command: Doc
#
@app.command()
def doc(
    ctx: typer.Context,
    title: str = typer.Option(None, help="The title of the document"),
    toc: bool = typer.Option(False, help="Whether to create a table of contents"),
    full: bool = typer.Option(False, "-f", "--full", help="Show complete documentation (default: top section only)")
) -> None:
    """
    Generate documentation for the script.

    By default, shows only the top section with overview and basic usage.
    Use --full to see complete documentation including all commands.

    Examples:
        gf doc  # Show top section only
        gf doc --full  # Show complete documentation
        gf doc --toc  # Include table of contents
        gf doc --title "My Git Flow" # Custom title
    """
    result = DocGenerator.generate_doc(__file__, title, toc, full_doc=full)
    print(result)


#
# Main function
#
if __name__ == "__main__":
    try:
        app()
    except SystemExit as e:
        if e.code != 0:
            raise










