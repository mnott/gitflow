#!/usr/bin/env python3
# encoding: utf-8
r"""
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

"""


import sys
import os
import glob
import subprocess
from datetime import datetime
from pathlib import Path
from rich import print
from rich import traceback
from rich import pretty
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import typer
from git import Repo, GitCommandError
from typing import Optional, List
from InquirerPy import inquirer

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

# Initialize the Git repository
def find_git_repo(path):
    try:
        return Repo(path, search_parent_directories=True)
    except GitCommandError:
        return None

# Try to find the Git repository
current_path = Path.cwd()
repo = find_git_repo(current_path)

if repo is None:
    console.print("[red]Error: Not in a valid Git repository[/red]")
    sys.exit(1)

# Get the repository root directory
repo_root = Path(repo.git.rev_parse("--show-toplevel"))

# Change the working directory to the repository root
os.chdir(repo_root)


# Get the current week number
def get_week_number(week: Optional[int] = None) -> str:
    """Get the current week number in the format YYYY-WW."""
    if week is None:
        week = datetime.now().isocalendar()[1]
    return f"{datetime.now().year}-{week:02}"


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


# Check whether we are online with the remote
def check_network_connection():
    try:
        repo.git.ls_remote('--exit-code', '--quiet', 'origin')
        return True
    except GitCommandError:
        return False


# Check for Branch Differences
def has_differences(base_branch: str, compare_branch: str):
    if not check_network_connection():
        console.print("[yellow]Warning: No network connection. Unable to fetch latest changes.[/yellow]")
        console.print("[yellow]Proceeding with local comparison.[/yellow]")
        try:
            # Use local refs for comparison
            merge_base = repo.git.merge_base(base_branch, compare_branch)
            diff = repo.git.diff(f'{merge_base}..{compare_branch}')
            return bool(diff.strip())
        except GitCommandError as e:
            console.print(f"[yellow]Warning: Error checking local differences: {e}[/yellow]")
            return True  # Assume there are differences if we can't check
    
    try:
        # Use our custom fetch function to fetch the specific base branch
        fetch(remote="origin", branch=base_branch, prune=False, all_remotes=False)
        
        # Now we can use the fetched remote branch
        merge_base = repo.git.merge_base(f'origin/{base_branch}', compare_branch)
        diff = repo.git.diff(f'{merge_base}..{compare_branch}')
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
# Helper Function to split a commit message body at the 72nd character
#
def split_message_body(body: str) -> str:
    """Splits the commit message body at the 72nd character, avoiding word splits."""
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
# Start a new feature, hotfix, or release branch
#
@app.command()
def start(
    name:        Optional[str] = typer.Option(None,     "-n", "--name",        help="Specify the feature, hotfix, release, or backup name"),
    branch_type: str           = typer.Option("hotfix", "-t", "--type",        help="Specify the branch type: local, hotfix, feature, release, or backup"),
    week:        Optional[int] = typer.Option(None,     "-w", "--week",        help="Specify the calendar week"),
    increment:   str           = typer.Option("patch",  "-i", "--increment",   help="Specify the version increment type: major, minor, patch"),
    message:     Optional[str] = typer.Option(None,     "-m", "--message",     help="Specify a commit message"),
    skip_switch: bool          = typer.Option(False,    "-s", "--skip-switch", help="Skip switching to main or develop branch before creating the new branch")
):
    """
    Start a new feature, hotfix, or release branch.

    If a name is provided, create a feature, hotfix, or release branch.
    Otherwise, create a weekly update hotfix branch.

    Parameters:
    - name       : The name of the feature, hotfix, or release branch.
    - branch_type: The type of branch to create ('local', 'hotfix', 'feature', or 'release').
    - week       : The calendar week for a weekly hotfix branch.
    - increment  : The version increment type for release branches ('major', 'minor', or 'patch').
    - message    : An optional commit message.
    - skip_switch: Whether to skip switching to the main or develop branch before creating the new branch. True is assumed for -t backup.
    """
    offline = not check_network_connection()
    if offline:
        console.print("[yellow]Network is unavailable. Operating in offline mode.[/yellow]")

    version_tag = None
    existing_tags = [tag.name for tag in repo.tags]
    if name and branch_type != "release":
        if branch_type == "local":
            branch_name = name
        else:
            branch_name = f"{branch_type}/{name}"
    elif branch_type == "hotfix":
        week_number = get_week_number(week)
        branch_name = f"hotfix/week-{week_number}"
    elif branch_type == "release":
        version_tag = get_next_semver(increment, existing_tags)
        print(f"Next version tag: {version_tag}")
        if name is None:
            name = version_tag
        branch_name = f"release/{name}"
    else:
        console.print("[red]Error: A feature or release branch must have a name[/red]")
        return

    if branch_type == "backup":
        skip_switch = True

    base_branch = 'main' if branch_type == 'hotfix' else 'develop'

    try:
        if not skip_switch:
            # Checkout base branch
            repo.git.checkout(base_branch)
            if not offline:
                # Pull the latest changes if online
                repo.git.pull('origin', base_branch)
            else:
                console.print(f"[yellow]Skipping pull from {base_branch} due to offline mode.[/yellow]")

        # Check if the branch already exists
        if branch_name in repo.branches:
            repo.git.checkout(branch_name)
            console.print(f"[yellow]Switched to existing branch {branch_name}[/yellow]")
        else:
            # Create and checkout the new branch
            repo.git.checkout('-b', branch_name)
            console.print(f"[green]Created and switched to branch {branch_name}[/green]")

        if message:
            # Commit the initial changes if a message is provided
            repo.git.add('.')
            if repo.index.diff("HEAD"):
                repo.git.commit('-m', message)
                console.print(f"[green]Initial commit with message: {message}[/green]")
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")

        if branch_type == "release" and version_tag:
            # Create the tag locally, but don't push it yet
            repo.create_tag(version_tag, message=f"Release {version_tag}")
            console.print(f"[green]Created local tag {version_tag}[/green]")

        if offline:
            console.print("[yellow]Note: Branch created locally. Remember to push changes when back online.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Finish a feature, hotfix, or release branch
#
@app.command()
def finish(
    name:        Optional[str] = typer.Option(None,     "-n", "--name",    help="Specify the feature, hotfix, or release name"),
    branch_type: str           = typer.Option("hotfix", "-t", "--type",    help="Specify the branch type: local, hotfix, feature, or release"),
    week:        Optional[int] = typer.Option(None,     "-w", "--week",    help="Specify the calendar week"),
    message:     Optional[str] = typer.Option(None,     "-m", "--message", help="Specify a commit message"),
    body:        Optional[str] = typer.Option(None,     "-b", "--body",    help="Specify a commit message body"),
    delete:      bool          = typer.Option(True,     "-d", "--delete",  help="Delete the feature, hotfix, or release branch after finishing")
):
    """
    Finish the feature, hotfix, or release by creating pull requests for main and/or develop.

    Parameters:
    - name       : The name of the feature, hotfix, or release branch.
    - branch_type: The type of branch to finish ('hotfix', feature, or 'release').
    - week       : The calendar week for a weekly hotfix branch.
    - message    : An optional commit message.
    - body       : An optional commit message body.
    - delete     : Whether to delete the feature, hotfix, or release branch after creating PRs.
    """
    offline = not check_network_connection()
    if offline:
        console.print("[yellow]Network is unavailable. Operating in offline mode.[/yellow]")
    
    # Determine the branch name
    if name and branch_type != "release":
        if branch_type == "local":
            branch_name = name
        else:
            branch_name = f"{branch_type}/{name}"
    else:
        if branch_type == "hotfix":
            week_number = get_week_number(week)
            branch_name = f"hotfix/week-{week_number}"
        elif branch_type == "release":
            if name:
                branch_name = f"release/{name}"
            else:
                console.print("[red]Error: Release branch name must be provided[/red]")
                return
        else:
            console.print("[red]Error: A feature branch must have a name[/red]")
            return

    try:
        original_branch = repo.active_branch.name

        # Ensure we're on the correct branch
        repo.git.checkout(branch_name)

        # Check for unstaged changes
        if repo.is_dirty(untracked_files=True):
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
                commit_message = message or inquirer.text(message="Enter commit message:").execute()
                commit_body = body or inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()
                full_commit_message = commit_message + "\n\n" + split_message_body(commit_body) if commit_body else commit_message
                repo.git.add('.')
                repo.git.commit('-m', full_commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Stash changes":
                repo.git.stash('save', f"Stashed changes before finishing {branch_type}")
                console.print("[green]Changes stashed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Finish operation aborted.[/yellow]")
                return
            # If "Continue without committing" is selected, we just proceed
        elif message:
            # If there are no unstaged changes but a message was provided, commit any staged changes
            commit_body = body or inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()
            full_commit_message = message + "\n\n" + split_message_body(commit_body) if commit_body else message
            if repo.index.diff("HEAD"):
                repo.git.commit('-m', full_commit_message)
                console.print(f"[green]Committed changes with message: {full_commit_message}[/green]")
            else:
                console.print("[yellow]No changes to commit.[/yellow]")

        # Push the branch to the remote
        if not offline:
            try:
                repo.git.push('origin', branch_name)
            except GitCommandError as e:
                if "non-fast-forward" in str(e):
                    console.print(f"[yellow]Branch already exists on remote. Pulling changes and pushing again.[/yellow]")
                    repo.git.pull('origin', branch_name, '--rebase')
                    repo.git.push('origin', branch_name)
                else:
                    raise e
        else:
            console.print("[yellow]Skipping push to remote due to offline mode.[/yellow]")

        if not offline:
            prs_created = False

            if branch_type == "release":
                # Push the tag to the remote
                tag_name = name if name else repo.git.describe('--tags', '--abbrev=0')
                repo.git.push('origin', tag_name)
                console.print(f"[green]Pushed tag {tag_name} to remote[/green]")

            if branch_type == "release" or branch_type == "hotfix":
                prs_created_main    = create_pull_request("main",    branch_name, branch_type)
                prs_created_develop = create_pull_request("develop", branch_name, branch_type)
                prs_created = prs_created_main or prs_created_develop
            else:  # feature
                prs_created = create_pull_request("develop", branch_name, branch_type)

            if prs_created:
                console.print(f"[yellow]Branch {branch_name} not deleted because pull requests were created.[/yellow]")
            else:
                console.print(f"[yellow]No pull requests were created as there were no differences to merge.[/yellow]")

            if delete and not prs_created:
                # Delete the branch locally and remotely
                repo.git.checkout('develop')
                repo.git.branch('-D', branch_name)
                try:
                    repo.git.push('origin', '--delete', branch_name)
                    console.print(f"[green]Deleted branch {branch_name} locally and remotely.[/green]")
                except GitCommandError:
                    console.print(f"[yellow]Could not delete remote branch {branch_name}. It may not exist or you may not have permission.[/yellow]")
        else:
            console.print(f"[yellow]Branch {branch_name} was not deleted. Remote operations skipped due to offline mode.[/yellow]")

        # Return to develop branch if we're not already on it
        if repo.active_branch.name != 'develop':
            repo.git.checkout('develop')
            console.print("[green]Returned to develop branch.[/green]")

        # If changes were stashed, ask if the user wants to pop them
        if 'action' in locals() and action == "Stash changes":
            pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
            if pop_stash:
                try:
                    repo.git.stash('pop')
                    console.print("[green]Stashed changes reapplied.[/green]")
                except GitCommandError as e:
                    console.print(f"[red]Error reapplying stashed changes: {e}[/red]")
                    console.print("[yellow]Your changes are still in the stash. You may need to manually resolve conflicts.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        # Ensure we return to the develop branch if something went wrong
        if repo.active_branch.name != 'develop':
            repo.git.checkout('develop')
            console.print("[green]Returned to develop branch.[/green]")

    if offline:
        console.print("[yellow]Finish operation completed in offline mode. Remember to push changes and create pull requests when back online.[/yellow]")


#
# Weekly update hotfix branches
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
        original_branch = repo.active_branch.name

        # Ensure the weekly-updates branch is checked out, fetch it if necessary
        if weekly_branch not in repo.branches:
            repo.git.fetch('origin', weekly_branch)
            repo.git.checkout('-b', weekly_branch, f'origin/{weekly_branch}')
        else:
            repo.git.checkout(weekly_branch)
            repo.git.pull('origin', weekly_branch)
        console.print(f"[green]Pulled changes from {weekly_branch}[/green]")

        # Check for changes
        if repo.is_dirty(untracked_files=True):
            # Prepare the commit message
            if message is None:
                message = inquirer.text(message="Enter commit message:").execute()
            if body is None:
                body = inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()

            full_commit_message = message
            if body:
                full_commit_message += "\n\n" + split_message_body(body)

            # Commit changes
            repo.git.add('.')
            repo.git.commit('-m', full_commit_message)
            console.print("[green]Changes committed.[/green]")

            # Push changes
            repo.git.push('origin', weekly_branch)
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
        repo.git.checkout(original_branch)
        console.print(f"[green]Returned to {original_branch}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Update from a release branch merging it back into develop
#
@app.command()
def update(
    name:    Optional[str] = typer.Option(None, "-n", "--name",    help="Specify the release name"),
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Specify a commit message"),
    body:    Optional[str] = typer.Option(None, "-b", "--body",    help="Specify a commit message body")
):
    """
    Update a release branch and merge it back into the develop branch.
    """
    branch_name = f"release/{name}"

    offline = not check_network_connection()

    if not offline:
        console.print("[yellow]Warning: No network connection detected.[/yellow]")
        offline = inquirer.confirm(message="Do you want to proceed in offline mode?", default=True).execute()
        if not offline:
            console.print("[red]Update operation aborted.[/red]")
            return

    try:
        original_branch = repo.active_branch.name

        # Checkout the release branch
        repo.git.checkout(branch_name)
        console.print(f"[blue]Checked out {branch_name}[/blue]")

        # Check for unstaged changes
        if repo.is_dirty(untracked_files=True):
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
                commit_message = message or inquirer.text(message="Enter commit message:").execute()
                commit_body = body or inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()
                full_commit_message = commit_message + "\n\n" + split_message_body(commit_body) if commit_body else commit_message
                repo.git.add('.')
                repo.git.commit('-m', full_commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Stash changes":
                repo.git.stash('save', f"Stashed changes before updating {branch_name}")
                console.print("[green]Changes stashed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Update operation aborted.[/yellow]")
                return
        elif message:
            if repo.index.diff("HEAD"):
                commit_body = body or inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()
                full_commit_message = message + "\n\n" + split_message_body(commit_body) if commit_body else message
                repo.git.commit('-m', full_commit_message)
                console.print(f"[green]Committed changes with message: {full_commit_message}[/green]")
            else:
                console.print("[yellow]No changes to commit.[/yellow]")

        if not offline:
            try:
                # Use the fetch function we constructed earlier
                fetch(remote="origin", branch=None, all_remotes=False, prune=False)

                # Push the release branch to remote
                repo.git.push('origin', branch_name)
                console.print(f"[green]Pushed changes to remote {branch_name}[/green]")
            except GitCommandError as e:
                console.print(f"[yellow]Warning: Unable to perform network operations. Error: {e}[/yellow]")
                console.print("[yellow]Proceeding with local merge.[/yellow]")

        # Check if there are differences between release and develop branches
        changes_made = has_differences('develop', branch_name)
        console.print(f"[blue]Differences detected: {changes_made}[/blue]")

        if not changes_made:
            console.print("[yellow]No differences found between release and develop branches. No update needed.[/yellow]")
            return

        # Merge release branch into develop
        console.print(f"[yellow]Merging {branch_name} into develop...[/yellow]")
        repo.git.checkout('develop')
        try:
            repo.git.merge(branch_name, '--no-ff')
            console.print(f"[green]Successfully merged {branch_name} into develop.[/green]")
        except GitCommandError as e:
            console.print(f"[red]Merge conflict occurred: {e}[/red]")
            console.print("[yellow]Please resolve conflicts manually, then commit the changes.[/yellow]")
            return

        if not offline:
            try:
                # Push develop branch to remote
                repo.git.push('origin', 'develop')
                console.print("[green]Pushed updated develop branch to remote.[/green]")

                # Create a pull request (if applicable)
                console.print(f"[yellow]Creating pull request to merge develop into main.[/yellow]")
                prs_created = create_pull_request('main', 'develop', "update")
                if prs_created:
                    console.print(f"[green]Pull request created to merge develop into main.[/green]")
                else:
                    console.print(f"[red]Failed to create pull request. Please create it manually.[/red]")
                    console.print(f"[yellow]You can use the GitHub web interface to create a pull request from develop to main.[/yellow]")
            except GitCommandError as e:
                console.print(f"[yellow]Warning: Unable to push or create pull request. Error: {e}[/yellow]")
                console.print("[yellow]Local merge is complete. Please push changes and create pull request when online.[/yellow]")
        else:
            console.print("[yellow]Operating in offline mode. Local merge is complete.[/yellow]")
            console.print("[yellow]Please push changes and create pull request when online.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        # Return to the original branch
        repo.git.checkout(original_branch)
        console.print(f"[green]Returned to {original_branch}[/green]")

        # If changes were stashed, ask if the user wants to pop them
        if 'action' in locals() and action == "Stash changes":
            pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
            if pop_stash:
                try:
                    repo.git.stash('pop')
                    console.print("[green]Stashed changes reapplied.[/green]")
                except GitCommandError as e:
                    console.print(f"[red]Error reapplying stashed changes: {e}[/red]")
                    console.print("[yellow]Your changes are still in the stash. You may need to manually resolve conflicts.[/yellow]")


#
# List all branches
#
@app.command()
def ls():
    """
    List all branches, including both local and remote.

    Examples:
    - List all branches:
        ./gitflow.py ls
    """
    local_branches = [head.name for head in repo.heads]
    remote_branches = [ref.name for ref in repo.remote().refs if ref.name != 'origin/HEAD']

    console.print("[cyan]Local branches:[/cyan]")
    for branch in local_branches:
        console.print(f"  - {branch}")

    console.print("[cyan]Remote branches:[/cyan]")
    for branch in remote_branches:
        console.print(f"  - {branch}")


#
# Checkout a branch
#
@app.command()
def checkout(
    target: Optional[str] = typer.Argument(None,                   help="The branch to switch to, or file/directory to revert"),
    force:  bool          = typer.Option  (False, "-f", "--force", help="Force checkout, discarding local changes")
):
    """
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
    """
    offline = not check_network_connection()

    try:
        if target is None:
            # Interactive branch selection
            local_branches = [f"Local : {head.name}" for head in repo.heads]
            if not offline:
                remote_branches = [f"Remote: {ref.name.replace('origin/', '')}" for ref in repo.remotes.origin.refs if ref.name != 'origin/HEAD']
                branches = local_branches + remote_branches
            else:
                branches = local_branches
                console.print("[yellow]Offline mode: Only local branches are available.[/yellow]")
            
            selected = inquirer.select(message="Select a branch:", choices=branches).execute()
            branch_type, branch_name = selected.split(": ")
            
            if branch_type == "Remote":
                target = f"origin/{branch_name}"
            else:
                target = branch_name

        # Check if target is a branch
        if target in repo.branches or (not offline and target.startswith("origin/")):
            # Check if there are uncommitted changes
            if repo.is_dirty(untracked_files=True) and not force:
                action = inquirer.select(
                    message="You have uncommitted changes. What would you like to do?",
                    choices=[
                        "Stash changes",
                        "Continue without stashing",
                        "Abort"
                    ]
                ).execute()

                if action == "Stash changes":
                    repo.git.stash('push')
                    console.print("[green]Changes stashed.[/green]")
                elif action == "Abort":
                    console.print("[yellow]Operation aborted.[/yellow]")
                    return

            # Switch to the branch
            try:
                if not offline and target.startswith("origin/"):
                    # For remote branches, create a new local branch
                    local_branch_name = target.split("/", 1)[1]
                    if local_branch_name not in repo.branches:
                        repo.git.checkout('-b', local_branch_name, target)
                    else:
                        repo.git.checkout(local_branch_name)
                        if not offline:
                            repo.git.pull('origin', local_branch_name)
                else:
                    if force:
                        repo.git.checkout(target, force=True)
                    else:
                        repo.git.checkout(target)
                console.print(f"[green]Switched to branch {target.split('/')[-1]}[/green]")
            except GitCommandError as e:
                console.print(f"[red]Error: {e}[/red]")
        else:
            # Revert changes in file or directory
            try:
                if target == '.':
                    repo.git.checkout('.')
                    console.print(f"[green]Reverted all changes in the current directory[/green]")
                else:
                    repo.git.checkout('--', target)
                    console.print(f"[green]Reverted changes in {target}[/green]")
            except GitCommandError as e:
                console.print(f"[red]Error: {e}[/red]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")

    # If changes were stashed, ask if the user wants to pop them
    if 'action' in locals() and action == "Stash changes":
        pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
        if pop_stash:
            try:
                repo.git.stash('pop')
                console.print("[green]Stashed changes reapplied.[/green]")
            except GitCommandError as e:
                console.print(f"[red]Error reapplying stashed changes: {e}[/red]")
                console.print("[yellow]Your changes are still in the stash. You may need to manually resolve conflicts.[/yellow]")


#
# Delete a branch
#
@app.command()
def rm(
    branch_name: Optional[str] = typer.Argument(None,                   help="The branch name to delete"),
    force:       bool          = typer.Option  (False, "-f", "--force", help="Force delete the branch, even if it's not fully merged or has open pull requests"),
    all:         bool          = typer.Option  (False, "-a", "--all",   help="Delete both local and remote branches with the same name")
):
    """
    Delete a branch using an interactive menu or by specifying the branch name.

    Parameters:
    - branch_name: The branch name to delete.
    - force      : Force delete the branch, even if it's not fully merged or has open pull requests.
    - all        : Delete both local and remote branches with the same name.

    Examples:
    - Delete a branch using a menu:
        ./gitflow.py rm
    - Delete a specific branch:
        ./gitflow.py rm feature/old-feature
    - Force delete a branch (local or remote):
        ./gitflow.py rm feature/old-feature -f
    - Delete both local and remote branches with the same name:
        ./gitflow.py rm -a
    """
    if not check_network_connection():
        console.print("[yellow]Warning: No network connection. Only local operations will be performed.[/yellow]")
        all = False  # Disable remote operations

    if check_network_connection():
        # Update local and remote references
        repo.git.fetch('--all')
        repo.git.remote('prune', 'origin')

    local_branches = [head.name for head in repo.heads]
    remote_branches = []
    if check_network_connection():
        remote_branches = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs if ref.name != 'origin/HEAD']

    if not branch_name:
        all_branches = [f"Local: {branch}" for branch in local_branches]
        if check_network_connection():
            all_branches += [f"Remote: {branch}" for branch in remote_branches]
        branch_name = inquirer.select(message="Select a branch to delete:", choices=all_branches).execute()

    if "Local: " in branch_name:
        branch_name = branch_name.replace("Local: ", "")
        delete_local = True
        delete_remote = False
    elif "Remote: " in branch_name:
        branch_name = branch_name.replace("Remote: ", "")
        delete_local = False
        delete_remote = True
    else:
        delete_local = True
        delete_remote = all and check_network_connection()

    if branch_name in ['develop', 'main']:
        console.print("[red]Error: You cannot delete the develop or main branches.[/red]")
        return

    if branch_name == repo.active_branch.name:
        console.print("[yellow]Switching to 'develop' branch before deletion.[/yellow]")
        try:
            # Check for unstaged changes
            if repo.is_dirty(untracked_files=True):
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
                    commit_message = inquirer.text(message="Enter commit message:").execute()
                    repo.git.add('.')
                    repo.git.commit('-m', commit_message)
                    console.print("[green]Changes committed.[/green]")
                elif action == "Stash changes":
                    repo.git.stash('save', f"Stashed changes before switching to 'develop'")
                    console.print("[green]Changes stashed.[/green]")
                elif action == "Abort":
                    console.print("[yellow]Delete operation aborted.[/yellow]")
                    return
                # If "Continue without committing" is selected, we just proceed

            repo.git.checkout('develop')
            console.print("[green]Switched to 'develop' branch.[/green]")
        except GitCommandError as e:
            console.print(f"[red]Error switching to 'develop' branch: {e}[/red]")
            return

    def check_prs(branch_name: str):
        if not check_network_connection():
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

    def delete_branch(branch_name: str, delete_local: bool, delete_remote: bool):
        if delete_local and branch_name in local_branches:
            try:
                repo.git.branch('-d' if not force else '-D', branch_name)
                console.print(f"[green]Deleted local branch {branch_name}[/green]")
                local_branches.remove(branch_name)  # Remove from list after successful deletion
            except GitCommandError as e:
                console.print(f"[red]Error deleting local branch {branch_name}: {e}[/red]")

        if delete_remote and branch_name in remote_branches and check_network_connection():
            # Verify if the branch actually exists on the remote
            remote_branches_actual = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs]
            if branch_name in remote_branches_actual:
                has_open_prs = check_prs(branch_name)
                if has_open_prs and not force:
                    console.print(f"[yellow]There are open pull requests for the branch {branch_name}. Use -f to force delete the remote branch.[/yellow]")
                else:
                    if has_open_prs:
                        console.print(f"[yellow]Warning: Deleting remote branch {branch_name} with open pull requests.[/yellow]")
                    try:
                        repo.git.push('origin', '--delete', branch_name)
                        console.print(f"[green]Deleted remote branch {branch_name}[/green]")
                        remote_branches.remove(branch_name)  # Remove from list after successful deletion
                    except GitCommandError as e:
                        console.print(f"[red]Error deleting remote branch {branch_name}: {e}[/red]")
            else:
                console.print(f"[red]Error: Remote branch {branch_name} does not exist[/red]")

    try:
        delete_branch(branch_name, delete_local, delete_remote)

        # If the -a flag is specified, delete both local and remote branches with the same name
        if all:
            if branch_name in local_branches:
                delete_branch(branch_name, True, False)
            if branch_name in remote_branches and check_network_connection():
                delete_branch(branch_name, False, True)

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


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
    offline = not check_network_connection()

    if not offline:
        repo.git.fetch('--all')
        repo.git.remote('prune', 'origin')

    local_branches = [head.name for head in repo.heads]
    remote_branches = []
    if not offline:
        remote_branches = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs if ref.name != 'origin/HEAD']

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
        if repo.is_dirty(untracked_files=True):
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
                commit_message = inquirer.text(message="Enter commit message:").execute()
                commit_body = inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()
                full_commit_message = commit_message
                if commit_body:
                    full_commit_message += "\n\n" + split_message_body(commit_body)
                repo.git.add('.')
                repo.git.commit('-m', full_commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Rename operation aborted.[/yellow]")
                return

        # Rename local branch
        if rename_local and old_name in local_branches:
            if old_name == repo.active_branch.name:
                repo.git.branch('-m', new_name)
            else:
                repo.git.branch('-m', old_name, new_name)
            console.print(f"[green]Renamed local branch from {old_name} to {new_name}[/green]")

        # Rename remote branch
        if rename_remote and old_name in remote_branches:
            try:
                repo.git.push('origin', f'{new_name}')
                repo.git.push('origin', f':{old_name}')
                console.print(f"[green]Renamed remote branch from {old_name} to {new_name}[/green]")
            except GitCommandError as e:
                if "protected branch" in str(e).lower():
                    console.print(f"[yellow]Protected branch {old_name} detected. Creating a new branch for pull request.[/yellow]")
                    pr_branch_name = f"rename-{old_name}-to-{new_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    repo.git.checkout('-b', pr_branch_name)
                    repo.git.push('origin', pr_branch_name)

                    prs_created = create_pull_request(old_name, pr_branch_name, "rename")
                    if prs_created:
                        console.print(f"[green]Created pull request to rename {old_name} to {new_name}[/green]")
                    else:
                        console.print(f"[red]Failed to create pull request. Please create it manually.[/red]")

                    # Switch back to the original branch
                    repo.git.checkout(old_name)
                else:
                    console.print(f"[red]Error renaming remote branch: {e}[/red]")

        # Update tracking for the local branch if both local and remote were renamed
        if rename_local and rename_remote:
            repo.git.branch(f'--set-upstream-to=origin/{new_name}', new_name)

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
            repo.git.add('--all')
            console.print(f"[green]Added all changes to the staging area[/green]")
        else:
            if force:
                repo.git.add(file_paths, force=True)
            else:
                repo.git.add(file_paths)
            console.print(f"[green]Added {file_paths} to the staging area[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


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
            repo.git.add('--all')
            console.print("[green]Staged all changes.[/green]")
        elif interactive:
            # Get only unstaged files
            status = repo.git.status('--porcelain').splitlines()
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
                    repo.git.add(file)
                console.print(f"[green]Staged selected files: {', '.join(file[3:] for file in selected)}[/green]")
            else:
                console.print("[yellow]No files selected for staging.[/yellow]")
        elif files:
            repo.git.add(files)
            console.print(f"[green]Staged specified files: {', '.join(files)}[/green]")
        else:
            # Get only unstaged files
            status = repo.git.status('--porcelain').splitlines()
            unstaged = [s for s in status if s.startswith(' M') or s.startswith('??')]
            
            if not unstaged:
                console.print("[yellow]No unstaged changes to stage.[/yellow]")
                return

            console.print("[blue]Unstaged changes:[/blue]")
            for s in unstaged:
                console.print(s)

            stage_all = inquirer.confirm(message="Do you want to stage all unstaged changes?", default=False).execute()
            if stage_all:
                repo.git.add('--all')
                console.print("[green]Staged all unstaged changes.[/green]")
            else:
                console.print("[yellow]No changes staged. Use --all or specify files to stage.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
        

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
            repo.git.reset()
            console.print("[green]Unstaged all changes.[/green]")
        elif interactive:
            status = repo.git.diff('--name-status', '--cached').splitlines()
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
                    repo.git.reset('HEAD', file)
                console.print(f"[green]Unstaged selected files: {', '.join(item.split()[1] for item in selected)}[/green]")
            else:
                console.print("[yellow]No files selected for unstaging.[/yellow]")
        elif files:
            for file in files:
                repo.git.reset('HEAD', file)
            console.print(f"[green]Unstaged specified files: {', '.join(files)}[/green]")
        else:
            status = repo.git.diff('--name-status', '--cached').splitlines()
            if not status:
                console.print("[yellow]No staged changes to unstage.[/yellow]")
                return

            console.print("[blue]Staged changes:[/blue]")
            for s in status:
                console.print(s)

            unstage_all = inquirer.confirm(message="Do you want to unstage all changes?", default=False).execute()
            if unstage_all:
                repo.git.reset()
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
            stash_list = repo.git.stash('list')
            if stash_list:
                console.print("[blue]Stash list:[/blue]")
                console.print(stash_list)
            else:
                console.print("[yellow]No stashes found.[/yellow]")
        elif show:
            stash_show = repo.git.stash('show', '-p', show)
            console.print(f"[blue]Changes in {show}:[/blue]")
            console.print(stash_show)
        elif drop:
            stash_info = repo.git.stash('list', show).strip()
            repo.git.stash('drop', drop)
            console.print(f"[green]Deleted stash: {stash_info}[/green]")
        elif clear:
            confirm = inquirer.confirm(message="Are you sure you want to clear all stashes?", default=False).execute()
            if confirm:
                repo.git.stash('clear')
                console.print("[green]Cleared all stashes.[/green]")
            else:
                console.print("[yellow]Stash clear operation cancelled.[/yellow]")
        else:  # push is the default action
            stash_args = ['push']
            if include_untracked:
                stash_args.append('--include-untracked')
            if message:
                split_message = split_message_body(message)
                stash_args.extend(['-m', split_message])
            
            repo.git.stash(*stash_args)
            
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
            stash_list = repo.git.stash('list').splitlines()
            if not stash_list:
                console.print("[yellow]No stashes found.[/yellow]")
                return
            
            selected_stash = inquirer.select(
                message="Select a stash:",
                choices=stash_list
            ).execute()
            stash_id = selected_stash.split(':')[0]

        if apply:
            repo.git.stash('apply', stash_id)
            console.print(f"[green]Applied stash {stash_id} without removing it.[/green]")
        else:
            repo.git.stash('pop', stash_id)
            console.print(f"[green]Popped stash {stash_id}.[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")

        

#
# Commit changes
#
@app.command()
def commit(
    message:     Optional[str] = typer.Option  (None,  "-m", "--message",     help="The commit message"),
    body:        Optional[str] = typer.Option  (None,  "-b", "--body",        help="The commit message body"),
    add_all:     bool          = typer.Option  (False, "-a", "--all",         help="Add all changes before committing"),
    interactive: bool          = typer.Option  (False, "-i", "--interactive", help="Use interactive mode for commit message"),
    files:       List[str]     = typer.Argument(None,                         help="Files or directories to commit")
):
    """
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
    """
    try:
        # Stage changes if files are specified
        if files:
            repo.git.add(files)
            console.print(f"[green]Added specified files to the staging area: {', '.join(files)}[/green]")
        elif add_all:
            repo.git.add('--all')
            console.print("[green]Added all changes to the staging area[/green]")
        elif repo.is_dirty(untracked_files=True):
            console.print("[yellow]You have unstaged changes.[/yellow]")
            add_all = inquirer.confirm(message="Do you want to stage all changes?", default=True).execute()
            if add_all:
                repo.git.add('--all')
                console.print("[green]Added all changes to the staging area[/green]")
            else:
                console.print("[yellow]Proceeding with only staged changes.[/yellow]")

        # Ensure there are changes to commit
        if not repo.index.diff("HEAD") and not repo.untracked_files:
            console.print("[yellow]No changes to commit.[/yellow]")
            return

        # Interactive mode or prompt for message if not provided
        if interactive or not message:
            message = inquirer.text(message="Enter commit message:").execute()
            body = inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()

        # Prepare the commit message
        full_commit_message = message
        if body:
            full_commit_message += "\n\n" + split_message_body(body)

        # Show the full commit message and ask for confirmation
        console.print(f"[blue]Full commit message:[/blue]\n{full_commit_message}")
        confirm = inquirer.confirm(message="Do you want to proceed with this commit?", default=True).execute()

        if not confirm:
            console.print("[yellow]Commit aborted.[/yellow]")
            return

        # Perform the commit
        repo.git.commit('-m', full_commit_message)
        console.print(f"[green]Committed changes with message:[/green]\n{full_commit_message}")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


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
    if not check_network_connection():
        console.print("[red]Error: No network connection. Unable to fetch.[/red]")
        return

    try:
        if all_remotes:
            console.print("[blue]Fetching changes from all remotes...[/blue]")
            if prune:
                repo.git.fetch('--all', '--prune')
            else:
                repo.git.fetch('--all')
            console.print("[green]Fetched changes from all remotes.[/green]")
        else:
            remote_name = remote or 'origin'
            if branch:
                console.print(f"[blue]Fetching branch {branch} from remote {remote_name}...[/blue]")
                repo.git.fetch(remote_name, branch)
                console.print(f"[green]Fetched branch {branch} from remote {remote_name}.[/green]")
            else:
                console.print(f"[blue]Fetching changes from remote {remote_name}...[/blue]")
                if prune:
                    repo.git.fetch('--prune', remote_name)
                else:
                    repo.git.fetch(remote_name)
                console.print(f"[green]Fetched changes from remote {remote_name}.[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error fetching changes: {e}[/red]")


#
# Merge
#
@app.command()
def merge(
    source: Optional[str] = typer.Argument(None,              help="The source branch to merge from"),
    target: Optional[str] = typer.Argument(None,              help="The target branch to merge into"),
    squash: bool          = typer.Option  (False, "--squash", help="Squash commits when merging"),
    no_ff:  bool          = typer.Option  (True,  "--no-ff",  help="Create a merge commit even when fast-forward is possible")
):
    """
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
    """
    original_branch = repo.active_branch.name
    try:
        # Check if we're in the middle of a merge
        if repo.git.status('--porcelain', '--untracked-files=no') and os.path.exists(repo.git_dir + '/MERGE_HEAD'):
            console.print("[yellow]Continuing previous merge...[/yellow]")
            return continue_merge()

        # Use the current branch if no source is provided
        if source is None:
            source = repo.active_branch.name

        # If no target is provided, use the current branch
        if target is None:
            target = repo.active_branch.name

        # Check for unstaged changes
        if repo.is_dirty(untracked_files=True):
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
                commit_message = inquirer.text(message="Enter commit message:").execute()
                commit_body = inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()
                full_commit_message = commit_message + "\n\n" + split_message_body(commit_body) if commit_body else commit_message
                repo.git.add('.')
                repo.git.commit('-m', full_commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Stash changes":
                repo.git.stash('save', f"Stashed changes before merging {source} into {target}")
                console.print("[green]Changes stashed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Merge operation aborted.[/yellow]")
                return

        # Check if the merge can be fast-forwarded
        merge_base = repo.git.merge_base(target, source).strip()
        target_head = repo.git.rev_parse(target).strip()
        source_head = repo.git.rev_parse(source).strip()

        if merge_base == target_head:
            console.print(f"[green]Fast-forwarding {target} to {source}[/green]")
            repo.git.checkout(target)
            repo.git.merge(source, '--ff-only')
            return

        # Check if there are differences between branches
        try:
            rev_list = repo.git.rev_list('--left-right', '--count', f'{target}...{source}')
            ahead, behind = map(int, rev_list.split())
            if ahead == 0 and behind == 0:
                console.print(f"[yellow]No differences found between {source} and {target}. No merge needed.[/yellow]")
                return
            else:
                console.print(f"[blue]Found differences: {source} is {behind} commit(s) behind and {ahead} commit(s) ahead of {target}.[/blue]")
        except GitCommandError:
            console.print(f"[yellow]Unable to determine differences between {source} and {target}. Proceeding with merge.[/yellow]")

        # Perform the merge
        repo.git.checkout(target)

        try:
            # Force conflict detection by using --no-commit
            if squash:
                repo.git.merge('--squash', '--no-commit', source)
            else:
                repo.git.merge('--no-commit', '--no-ff' if no_ff else None, source)

        except GitCommandError as e:
            console.print(f"[yellow]Merge conflicts detected. Please resolve the conflicts.[/yellow]")
            # Ensure the conflict markers are in place before proceeding
            status = repo.git.status('--porcelain')
            if any(line.startswith('UU') for line in status.split('\n')):
                return continue_merge()
            else:
                console.print("[red]Error: Merge conflicts detected, but no conflict markers found. Aborting merge.[/red]")
                repo.git.merge('--abort')
                return

        # Check for conflicts
        status = repo.git.status('--porcelain')
        if status:
            console.print(f"[yellow]Merge conflicts detected when merging {source} into {target}.[/yellow]")
            conflicting_files = [line.split()[1] for line in status.split('\n') if line.startswith('UU')]
            console.print("[yellow]Conflicting files:[/yellow]")
            for file in conflicting_files:
                console.print(f"[yellow]- {file}[/yellow]")

            action = inquirer.select(
                message="How would you like to proceed?",
                choices=[
                    "Open git mergetool",
                    "Abort merge",
                    "Continue (resolve manually later)"
                ]
            ).execute()

            if action == "Open git mergetool":
                try:
                    subprocess.run(['git', 'mergetool'], check=True)
                    status = repo.git.status('--porcelain')
                    if not any(line.startswith('UU') for line in status.split('\n')):
                        console.print("[green]Conflicts resolved. Continuing merge...[/green]")
                        repo.git.commit('-m', f"Merge branch '{source}' into {target}")
                        # Cleanup .orig files
                        for file in glob.glob('*.orig'):
                            os.remove(file)
                    else:
                        console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Error running git mergetool: {e}[/red]")
                return
            elif action == "Abort merge":
                repo.git.merge('--abort')
                console.print("[yellow]Merge aborted.[/yellow]")
            else:
                console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
            return
        else:
            # No conflicts, complete the merge
            if repo.is_dirty():  # Check if there are changes to commit
                repo.git.commit('-m', f"Merge branch '{source}' into {target}")
                console.print(f"[green]Successfully merged {source} into {target}.[/green]")
            else:
                console.print(f"[yellow]Merge completed but there were no changes to commit.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")

    finally:
        # Only checkout the original branch if there are no unresolved conflicts
        if 'original_branch' in locals() and not any(line.startswith('UU') for line in repo.git.status('--porcelain').split('\n')):
            repo.git.checkout(original_branch)
            console.print(f"[green]Returned to {original_branch}[/green]")

            # If changes were stashed, ask if the user wants to pop them
            if 'action' in locals() and action == "Stash changes":
                pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
                if pop_stash:
                    try:
                        repo.git.stash('pop')
                        console.print("[green]Stashed changes reapplied.[/green]")
                    except GitCommandError as e:
                        console.print(f"[red]Error reapplying stashed changes: {e}[/red]")
                        console.print("[yellow]Your changes are still in the stash. You may need to manually resolve conflicts.[/yellow]")


def continue_merge():
    try:
        # Check if there are still conflicts
        status = repo.git.status('--porcelain')
        conflicting_files = [line.split()[1] for line in status.split('\n') if line.startswith('UU')]
        
        if conflicting_files:
            console.print("[yellow]There are still conflicting files:[/yellow]")
            for file in conflicting_files:
                console.print(f"[yellow]- {file}[/yellow]")
            
            action = inquirer.select(
                message="How would you like to proceed?",
                choices=[
                    "Open git mergetool",
                    "Abort merge",
                    "Continue (resolve manually later)"
                ]
            ).execute()

            if action == "Open git mergetool":
                try:
                    subprocess.run(['git', 'mergetool'], check=True)
                    status = repo.git.status('--porcelain')
                    if not any(line.startswith('UU') for line in status.split('\n')):
                        console.print("[green]Conflicts resolved. Continuing merge...[/green]")
                        repo.git.commit('-m', "Merge conflicts resolved")
                        # Cleanup .orig files
                        for file in glob.glob('*.orig'):
                            os.remove(file)
                    else:
                        console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Error running git mergetool: {e}[/red]")
                return
            elif action == "Abort merge":
                repo.git.merge('--abort')
                console.print("[yellow]Merge aborted.[/yellow]")
            else:
                console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
        else:
            # Changes staged but not committed
            repo.git.commit('--no-edit')
            console.print(f"[green]Successfully completed the merge.[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error during merge continuation: {e}[/red]")


#
# Push changes
#
@app.command()
def push(
    branch:    Optional[str] = typer.Argument(None,                   help="The branch to push changes to"),
    force:     bool          = typer.Option  (False, "-f", "--force", help="Force push changes"),
    create_pr: bool          = typer.Option  (False, "-p", "--pr",    help="Create a pull request instead of pushing directly")
):
    """
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
    """
    try:
        # Use the current branch if no branch is provided
        if branch is None:
            branch = repo.active_branch.name

        current_branch = repo.active_branch.name

        # Check for unstaged changes
        if repo.is_dirty(untracked_files=True):
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
                commit_message = inquirer.text(message="Enter commit message:").execute()
                commit_body = inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()
                full_commit_message = commit_message
                if commit_body:
                    full_commit_message += "\n\n" + split_message_body(commit_body)
                repo.git.add('.')
                repo.git.commit('-m', full_commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Push aborted.[/yellow]")
                return

        offline = not check_network_connection()

        if not offline:
            # Use our custom fetch function
            fetch(remote="origin", branch=None, all_remotes=False, prune=False)

            # Check if there are differences between local and remote
            try:
                ahead_behind = repo.git.rev_list('--left-right', '--count', f'origin/{branch}...HEAD').split()
                behind = int(ahead_behind[0])
                ahead = int(ahead_behind[1])

                if ahead > 0:
                    console.print(f"[yellow]Your local branch is {ahead} commit(s) ahead of the remote branch.[/yellow]")
                    changes_made = True
                elif behind > 0:
                    console.print(f"[yellow]Your local branch is {behind} commit(s) behind the remote branch.[/yellow]")
                    if not force:
                        action = inquirer.select(
                            message="How would you like to proceed?",
                            choices=[
                                "Pull and rebase",
                                "Force push",
                                "Create pull request",
                                "Abort"
                            ]
                        ).execute()
                        if action == "Pull and rebase":
                            repo.git.pull('--rebase', 'origin', branch)
                        elif action == "Force push":
                            force = True
                        elif action == "Create pull request":
                            create_pr = True
                        else:
                            console.print("[yellow]Push aborted.[/yellow]")
                            return
                else:
                    console.print("[yellow]Your local branch is up to date with the remote branch. No push needed.[/yellow]")
                    return
            except GitCommandError:
                # If the remote branch doesn't exist, consider it as having differences
                changes_made = True
        else:
            console.print("[yellow]No network connection. Proceeding with local push.[/yellow]")
            changes_made = True

        if changes_made or create_pr:
            try:
                if create_pr:
                    if not offline:
                        console.print(f"[yellow]Creating pull request to merge {current_branch} into {branch}.[/yellow]")
                        result = subprocess.run(
                            ["gh", "pr", "create", "--base", branch, "--head", current_branch,
                             "--title", f"Merge {current_branch} into {branch}",
                             "--body", "Automated pull request from script"],
                            capture_output=True, text=True, check=True
                        )
                        console.print(f"[green]Created pull request to merge {current_branch} into {branch}[/green]")
                    else:
                        console.print("[yellow]No network connection. Unable to create pull request.[/yellow]")
                else:
                    if not offline:
                        if force:
                            repo.git.push('origin', branch, '--force')
                        else:
                            repo.git.push('origin', branch)
                        console.print(f"[green]Pushed changes to {branch}[/green]")
                    else:
                        console.print("[yellow]No network connection. Changes will be pushed when online.[/yellow]")
            except (GitCommandError, subprocess.CalledProcessError) as e:
                if "protected branch" in str(e):
                    console.print(f"[yellow]Protected branch {branch} detected. Creating a new branch for pull request.[/yellow]")
                    # Create a new branch for the pull request
                    new_branch_name = f"update-{branch}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    repo.git.checkout('-b', new_branch_name)
                    if not offline:
                        repo.git.push('origin', new_branch_name)
                        result = subprocess.run(
                            ["gh", "pr", "create", "--base", branch, "--head", new_branch_name,
                             "--title", f"Update {branch}", "--body", "Automated pull request from script"],
                            capture_output=True, text=True
                        )
                        if result.returncode != 0:
                            console.print(f"[red]Error creating pull request: {result.stderr}[/red]")
                        else:
                            console.print(f"[green]Created pull request to merge changes from {new_branch_name} into {branch}[/green]")
                    else:
                        console.print("[yellow]No network connection. New branch created locally. Push and create PR when online.[/yellow]")

                    # Switch back to the original branch
                    repo.git.checkout(current_branch)
                else:
                    console.print(f"[red]Error: {e}[/red]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


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
    """
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
    """
    if not check_network_connection():
        console.print("[red]Error: No network connection. Unable to pull.[/red]")
        return

    try:
        original_branch = repo.active_branch.name
        stashed_changes = False

        # Fetch changes first
        fetch_args = ['--all'] if all_branches else [remote]
        if prune:
            fetch_args.append('--prune')
        repo.git.fetch(*fetch_args)
        console.print("[green]Fetched changes from remote.[/green]")

        if all_branches:
            console.print("[blue]Pulling changes for all local branches...[/blue]")

            # Check for uncommitted changes before starting
            if repo.is_dirty(untracked_files=True):
                action = inquirer.select(
                    message="You have uncommitted changes. What would you like to do?",
                    choices=[
                        "Stash changes",
                        "Continue without stashing",
                        "Abort"
                    ]
                ).execute()

                if action == "Stash changes":
                    repo.git.stash('push')
                    console.print("[green]Changes stashed.[/green]")
                    stashed_changes = True
                elif action == "Abort":
                    console.print("[yellow]Operation aborted.[/yellow]")
                    return

            # Loop through each local branch and pull updates if there are changes
            for branch in repo.branches:
                local_commit = repo.git.rev_parse(branch.name)
                remote_commit = repo.git.rev_parse(f'{remote}/{branch.name}')

                if local_commit != remote_commit:
                    repo.git.checkout(branch.name)
                    console.print(f"[blue]Updating branch {branch.name}...[/blue]")
                    try:
                        if rebase:
                            result = subprocess.run(
                                ["git", "pull", "--rebase", remote, branch.name],
                                capture_output=True,
                                text=True
                            )
                        else:
                            result = subprocess.run(
                                ["git", "pull", remote, branch.name],
                                capture_output=True,
                                text=True
                            )
                        console.print(f"[green]Pulled changes for branch {branch.name}[/green]")
                        console.print(result.stdout)
                        if result.stderr:
                            console.print(result.stderr)
                    except subprocess.CalledProcessError as e:
                        console.print(f"[red]Error pulling changes for branch {branch.name}: {e}[/red]")
                else:
                    console.print(f"[yellow]Branch {branch.name} is up to date.[/yellow]")

            # Return to the original branch
            repo.git.checkout(original_branch)
            console.print(f"[green]Returned to branch {original_branch}[/green]")
        else:
            # Pull changes for the current branch
            current_branch = branch or repo.active_branch.name
            console.print(f"[blue]Pulling changes for branch {current_branch}...[/blue]")

            if repo.is_dirty(untracked_files=True):
                action = inquirer.select(
                    message="You have uncommitted changes. What would you like to do?",
                    choices=[
                        "Stash changes",
                        "Continue without stashing",
                        "Abort"
                    ]
                ).execute()

                if action == "Stash changes":
                    stash_message = inquirer.text(message="Enter a stash message (optional):").execute()
                    if stash_message:
                        repo.git.stash('push', '-m', stash_message)
                    else:
                        repo.git.stash('push')
                    console.print("[green]Changes stashed.[/green]")
                    stashed_changes = True
                elif action == "Abort":
                    console.print("[yellow]Pull aborted.[/yellow]")
                    return

            try:
                if rebase:
                    result = subprocess.run(
                        ["git", "pull", "--rebase", remote, current_branch],
                        capture_output=True,
                        text=True
                    )
                else:
                    result = subprocess.run(
                        ["git", "pull", remote, current_branch],
                        capture_output=True,
                        text=True
                    )
                console.print(f"[green]Pulled changes for branch {current_branch}[/green]")
                console.print(result.stdout)
                if result.stderr:
                    console.print(result.stderr)
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Error pulling changes for branch {current_branch}: {e}[/red]")

        # After successful pull, ask if user wants to pop the stash
        if stashed_changes:
            pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
            if pop_stash:
                try:
                    repo.git.stash('pop')
                    console.print("[green]Popped the stashed changes.[/green]")
                except GitCommandError as e:
                    console.print(f"[red]Error popping stash: {e}[/red]")
                    console.print("[yellow]You may need to resolve conflicts manually.[/yellow]")

        # Show the status after pulling
        status()

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
        if "Your local changes to the following files would be overwritten by merge" in str(e):
            console.print("[yellow]You have local changes that conflict with the changes you're pulling.[/yellow]")
            console.print("[yellow]Please commit, stash, or discard your local changes before pulling.[/yellow]")
        elif "Please commit your changes or stash them before you merge" in str(e):
            console.print("[yellow]You have uncommitted changes in your working directory.[/yellow]")
            console.print("[yellow]Please commit or stash your changes before pulling.[/yellow]")


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
        current_branch = repo.active_branch.name
        status_table.add_row("Current Branch", current_branch)

        # Get commit information
        last_commit = repo.head.commit
        commit_message = last_commit.message.strip()
        commit_author = last_commit.author.name
        commit_date = last_commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
        status_table.add_row("Last Commit", f"{commit_message[:50]}..." if len(commit_message) > 50 else commit_message)
        status_table.add_row("Commit Author", commit_author)
        status_table.add_row("Commit Date", commit_date)

        # Get ahead/behind info
        try:
            ahead_behind = repo.git.rev_list('--left-right', '--count', f'origin/{current_branch}...HEAD').split()
            behind = int(ahead_behind[0])
            ahead = int(ahead_behind[1])
            status_table.add_row("Commits Ahead/Behind", f"Ahead by {ahead}, Behind by {behind}")
        except GitCommandError:
            status_table.add_row("Commits Ahead/Behind", "Unable to determine")

        # Get status
        status = repo.git.status(porcelain=True)
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
        remotes = repo.remotes
        if remotes:
            remote_info = []
            for remote in remotes:
                remote_info.append(f"{remote.name}: {remote.url}")
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
        local_branches = [head.name for head in repo.heads]
        remote_branches = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs if ref.name != 'origin/HEAD']

        if branch1 is None:
            branches = local_branches + remote_branches
            branch1 = inquirer.select(message="Select the first branch:", choices=branches).execute()

        if branch2 is None:
            branches = local_branches + remote_branches
            branch2 = inquirer.select(message="Select the second branch:", choices=branches).execute()

        # Perform the diff
        diff = repo.git.diff(f'{branch1}:{file_path}', f'{branch2}:{file_path}')
        console.print(diff if diff else "[green]No differences found.[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Cherry-pick a file from the current branch into a target branch
#
@app.command()
def cp(
    file_path:     str           = typer.Argument(...,                 help="The path to the file to copy the latest commit for"),
    target_branch: Optional[str] = typer.Argument(None,                help="The target branch to copy into"),
    push:          bool          = typer.Option  (True, "--push",      help="Push the changes to the remote repository after copying"),
    create_pr:     bool          = typer.Option  (False, "-p", "--pr", help="Create a pull request instead of pushing directly")
):
    """
    Copy the latest commit of a specific file from the current branch into a target branch.

    Parameters:
    - file_path    : The path to the file to copy the latest commit for.
    - target_branch: The target branch to copy into.
    - push         : Push the changes to the remote repository after copying if the remote branch exists.
    - create_pr    : Create a pull request instead of pushing directly.

    Examples:
    - Copy the latest commit of gitflow.py into a feature branch:
        ./gitflow.py cp gitflow.py feature/new-feature --push
    - Copy and create a pull request:
        ./gitflow.py cp gitflow.py main --pr
    """
    try:
        offline = not check_network_connection()

        # Save the current branch
        original_branch = repo.active_branch.name

        # Read the file content in the current branch
        try:
            with open(file_path, 'r') as source_file:
                current_branch_file_content = source_file.read()
        except FileNotFoundError:
            console.print(f"[red]Error: {file_path} not found in the current branch[/red]")
            return

        # If target_branch is not provided, show a list of branches to select from
        if not target_branch:
            branches = [head.name for head in repo.heads if head.name != repo.active_branch.name]
            target_branch = inquirer.select(message="Select a branch to copy into:", choices=branches).execute()

        # Checkout the target branch
        repo.git.checkout(target_branch)
        console.print(f"[green]Switched to branch {target_branch}[/green]")

        # Read the file content in the target branch
        target_branch_file_content = ""
        try:
            with open(file_path, 'r') as target_file:
                target_branch_file_content = target_file.read()
        except FileNotFoundError:
            pass  # It's okay if the file does not exist in the target branch

        # Compare the file contents
        if current_branch_file_content == target_branch_file_content:
            console.print(f"[yellow]File {file_path} is identical in both branches. Skipping copy.[/yellow]")
        else:
            # Write the content from the current branch into the target branch
            with open(file_path, 'w') as target_file:
                target_file.write(current_branch_file_content)

            # Commit the change
            repo.git.add(file_path)
            commit_message = f"Copy latest changes for {file_path} from {original_branch} to {target_branch}"
            repo.git.commit('-m', commit_message)
            console.print(f"[green]Copied the latest changes for {file_path} into {target_branch}[/green]")

            # Push changes or create a pull request
            if push or create_pr:
                if not offline:
                    try:
                        if create_pr:
                            # Create a new branch for the pull request
                            pr_branch_name = f"cp-{file_path.replace('/', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            repo.git.checkout('-b', pr_branch_name)
                            repo.git.push('origin', pr_branch_name)

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
                            repo.git.push('origin', target_branch)
                            console.print(f"[green]Pushed changes to {target_branch}[/green]")
                    except GitCommandError as e:
                        if "protected branch" in str(e):
                            console.print(f"[yellow]Protected branch {target_branch} detected. Creating a pull request instead.[/yellow]")
                            # Create a new branch for the pull request
                            pr_branch_name = f"cp-{file_path.replace('/', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            repo.git.checkout('-b', pr_branch_name)
                            repo.git.push('origin', pr_branch_name)

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
                    console.print("[yellow]No network connection. Changes will be pushed when online.[/yellow]")

        # Return to the original branch
        repo.git.checkout(original_branch)
        console.print(f"[green]Returned to branch {original_branch}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")



#
# Command: Doc
#
@app.command()
def doc (
    ctx:        typer.Context,
    title:      str  = typer.Option(None,   help="The title of the document"),
    toc:        bool = typer.Option(False,  help="Whether to create a table of contents"),
) -> None:
    """
    Re-create the documentation and write it to the output file.
    """
    import importlib
    import importlib.util
    import sys
    import os
    import doc2md

    def import_path(path):
        module_name = os.path.basename(path).replace("-", "_")
        spec = importlib.util.spec_from_loader(
            module_name,
            importlib.machinery.SourceFileLoader(module_name, path),
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module

    mod_name = os.path.basename(__file__)
    if mod_name.endswith(".py"):
        mod_name = mod_name.rsplit(".py", 1)[0]
    atitle = title or mod_name.replace("_", "-")
    module = import_path(__file__)
    docstr = module.__doc__
    result = doc2md.doc2md(docstr, atitle, toc=toc, min_level=0)
    print(result)


#
# Main function
#
if __name__ == "__main__":
    if sys.gettrace() is not None:
        # For debugging purposes
        pass
    else:
        try:
            app()
        except SystemExit as e:
            if e.code != 0:
                raise
