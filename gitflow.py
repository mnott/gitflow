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
./gitflow.py delete
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
import subprocess
from datetime import datetime
from pathlib import Path
from rich import print
from rich import traceback
from rich import pretty
from rich.console import Console
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
try:
    repo = Repo(Path.cwd())
except GitCommandError:
    console.print("[red]Error: Not a valid Git repository[/red]")
    sys.exit(1)

def get_week_number(week: Optional[int] = None) -> str:
    """Get the current week number in the format YYYY-WW."""
    if week is None:
        week = datetime.now().isocalendar()[1]
    return f"{datetime.now().year}-{week:02}"

def get_current_week_tag(prefix: str = "cw-") -> str:
    """Generate a tag for the current week."""
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]
    current_tag = f"{prefix}{current_year}-{current_week:02}"
    return current_tag

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


#
# Start a branch
#
@app.command()
def start(
    name:        Optional[str] = typer.Option(None,     "-n", "--name",        help="Specify the feature, hotfix, release, or backup name"),
    branch_type: str           = typer.Option("hotfix", "-t", "--type",        help="Specify the branch type: hotfix, feature, release, or backup"),
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
    - branch_type: The type of branch to create ('hotfix', 'feature', or 'release').
    - week       : The calendar week for a weekly hotfix branch.
    - increment  : The version increment type for release branches ('major', 'minor', or 'patch').
    - message    : An optional commit message.
    - skip_switch: Whether to skip switching to the main or develop branch before creating the new branch. True is assumed for -t backup.

    Examples:
    - Start a weekly update hotfix branch (e.g. for some minor weekly updates):
        ./gitflow.py start
    - Start a new hotfix branch:
        ./gitflow.py start -t hotfix  -n "critical-bugfix" -m "Starting critical bugfix hotfix"
    - Start a new feature branch:
        ./gitflow.py start -t feature -n "new-feature"     -m "Starting new feature"
    - Start a new release branch:
        ./gitflow.py start -t release -m "Starting release" -i "patch"
    - Start a new backup branch off the current branch (-s is assumed if -t is backup):
        ./gitflow.py start -t backup -n "backup-branch" -m "Starting backup branch"

    The name is optional for a release (and for a weekly hotfix branch); if not given, those values will be auto-generated.
    """
    version_tag = None
    existing_tags = [tag.name for tag in repo.tags]
    if name and branch_type != "release":
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
            # Checkout base branch and pull the latest changes
            repo.git.checkout(base_branch)
            repo.git.pull('origin', base_branch)

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
            # Check if the tag already exists
            existing_tags = [tag.name for tag in repo.tags]
            if version_tag in existing_tags:
                console.print(f"[yellow]Tag {version_tag} already exists, skipping tagging[/yellow]")
            else:
                # Tag the release branch
                repo.git.tag('-a', version_tag, '-m', f"Release {name} {version_tag}")
                repo.git.push('origin', version_tag)
                console.print(f"[green]Tagged release branch with {version_tag}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Finish a branch
#
@app.command()
def finish(
    name: Optional[str] = typer.Option(None, "-n", "--name", help="Specify the feature, hotfix, or release name"),
    branch_type: str = typer.Option("hotfix", "-t", "--type", help="Specify the branch type: hotfix, feature, or release"),
    week: Optional[int] = typer.Option(None, "-w", "--week", help="Specify the calendar week"),
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Specify a commit message"),
    target_branch: Optional[str] = typer.Option("develop", "-tb", "--target-branch", help="Specify the branch to merge hotfix into"),
    delete: bool = typer.Option(True, "-d", "--delete", help="Delete the feature, hotfix, or release branch after creating PRs")
):
    """
    Finish the feature, hotfix, or release by creating pull requests for main and/or develop.

    Parameters:
    - name: The name of the feature, hotfix, or release branch.
    - branch_type: The type of branch to finish ('hotfix', feature, or 'release').
    - week: The calendar week for a weekly hotfix branch.
    - message: An optional commit message.
    - target_branch: The branch to merge hotfix into (default is 'develop').
    - delete: Whether to delete the feature, hotfix, or release branch after creating PRs.
    """
    if name and branch_type != "release":
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
        # Add and commit changes if a message is provided
        if message:
            repo.git.add('.')
            if repo.is_dirty(untracked_files=True):
                repo.git.commit('-m', message)
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")
        else:
            repo.git.add('.')
            if repo.is_dirty(untracked_files=True):
                default_message = f"Finish {branch_type}."
                repo.git.commit('-m', default_message)
                console.print(f"[green]Committed changes with default message: {default_message}[/green]")
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")

        # Push the branch to the remote
        try:
            repo.git.push('origin', branch_name)
        except GitCommandError as e:
            if "non-fast-forward" in str(e):
                console.print(f"[yellow]Branch already exists on remote. Pulling changes and pushing again.[/yellow]")
                repo.git.pull('origin', branch_name, '--rebase')
                repo.git.push('origin', branch_name)
            else:
                raise e

        # Create pull requests
        def create_pull_request(base_branch: str):
            result = subprocess.run(
                ["gh", "pr", "create", "--base", base_branch, "--head", branch_name,
                 "--title", f"Merge {branch_name} into {base_branch}", "--body", "Automated pull request from script"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                console.print(f"[red]Error creating pull request: {result.stderr}[/red]")
            else:
                console.print(f"[green]Created pull request to merge {branch_name} into {base_branch}[/green]")

        if branch_type == "hotfix" or branch_type == "release":
            create_pull_request("main")
        
        create_pull_request(target_branch)

        if delete:
            console.print(f"[yellow]Branch {branch_name} not deleted because pull requests were created.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")



#
# Weekly update hotfix branches
#
@app.command()
def weekly_update(
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Specify a commit message"),
):
    """
    Pull changes from the weekly-updates branch and merge them into develop and main branches.

    Parameters:
    - message: An optional commit message for the merge commits.

    Examples:
    - Pull changes and merge them:
        ./gitflow.py weekly_update -m "Merging weekly updates"
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

        # Merge changes into develop branch
        repo.git.checkout(develop_branch)
        repo.git.pull('origin', develop_branch)
        repo.git.merge(weekly_branch, '--no-ff', m=message or f"Merging changes from {weekly_branch} into {develop_branch}")
        repo.git.push('origin', develop_branch)
        console.print(f"[green]Merged changes from {weekly_branch} into {develop_branch}[/green]")

        # Merge changes into main branch
        repo.git.checkout(main_branch)
        repo.git.pull('origin', main_branch)
        repo.git.merge(develop_branch, '--no-ff', m=message or f"Merging changes from {develop_branch} into {main_branch}")
        repo.git.push('origin', main_branch)
        console.print(f"[green]Merged changes from {develop_branch} into {main_branch}[/green]")

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
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Specify a commit message")
):
    """
    Update the release branch by merging it back into develop.

    This command can be used to merge bug fixes from the release branch back into develop.

    Parameters:
    - name: The name of the release branch.
    - message: An optional commit message.

    Examples:
    - Update the release branch:
        ./gitflow.py update -n "1.2.0" -m "Merging bug fixes from release 1.2.0"
    """
    if not name:
        console.print("[red]Error: A release branch must have a name[/red]")
        return

    branch_name = f"release/{name}"

    try:
        # Checkout the release branch
        repo.git.checkout(branch_name)

        # Add and commit changes if a message is provided
        if message:
            repo.git.add('.')
            if repo.is_dirty(untracked_files=True):
                repo.git.commit('-m', message)
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")
        else:
            repo.git.add('.')
            if repo.is_dirty(untracked_files=True):
                default_message = "Update release branch."
                repo.git.commit('-m', default_message)
                console.print(f"[green]Committed changes with default message: {default_message}[/green]")
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")

        # Merge release branch into develop
        repo.git.checkout('develop')
        repo.git.pull('origin', 'develop')
        repo.git.merge(branch_name, '--no-ff')
        repo.git.push('origin', 'develop')

        console.print(f"[green]Merged {branch_name} into develop[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


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
def checkout(branch: Optional[str] = typer.Argument(None, help="The branch to switch to")):
    """
    Switch to a different branch using an interactive menu or directly if branch name is provided.

    Examples:
    - Switch to a different branch interactively:
        ./gitflow.py checkout
    - Switch to a specific branch:
        ./gitflow.py checkout develop
    """
    try:
        # List branches
        local_branches = [f"Local: {head.name}" for head in repo.heads]
        remote_branches = [f"Remote: {ref.name.replace('origin/', '')}" for ref in repo.remotes.origin.refs if ref.name != 'origin/HEAD']

        if branch is None:
            # Show menu if no branch is provided
            branches = local_branches + remote_branches
            selected = inquirer.select(message="Select a branch:", choices=branches).execute()
            branch_type, branch_name = selected.split(": ")
        else:
            # Check if branch is local or remote
            if branch in [head.name for head in repo.heads]:
                branch_type = "Local"
                branch_name = branch
            elif branch in [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs]:
                branch_type = "Remote"
                branch_name = branch
            else:
                console.print(f"[red]Error: Branch '{branch}' not found[/red]")
                return

        # Detect local or remote branch
        if branch_type == "Remote":
            remote_branch = f"origin/{branch_name}"
        else:
            remote_branch = None

        # Ensure working directory is clean before switching
        if repo.is_dirty(untracked_files=True):
            console.print(f"[red]Error: Working directory is not clean. Please commit or stash your changes before switching branches.[/red]")
            return

        # Switch to the branch
        try:
            if remote_branch:
                repo.git.checkout('-b', branch_name, remote_branch)
            else:
                repo.git.checkout(branch_name)
            console.print(f"[green]Switched to branch {branch_name}[/green]")
        except GitCommandError as e:
            console.print(f"[red]Error: {e}[/red]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")



#
# Delete a branch
#
@app.command()
def delete(
    branch_name: Optional[str] = typer.Argument(None, help="The branch name to delete"),
    force: bool = typer.Option(False, "-f", "--force", help="Force delete the branch, even if it's not fully merged or has open pull requests"),
    cleanup: bool = typer.Option(False, "-c", "--cleanup", help="Cleanup both local and remote branches")
):
    """
    Delete a branch using an interactive menu or by specifying the branch name.

    Parameters:
    - branch_name: The branch name to delete.
    - force: Force delete the branch, even if it's not fully merged or has open pull requests.
    - cleanup: Cleanup both local and remote branches after merging.

    Examples:
    - Delete a branch using a menu:
        ./gitflow.py delete
    - Delete a specific branch:
        ./gitflow.py delete feature/old-feature
    - Force delete a branch (local or remote):
        ./gitflow.py delete feature/old-feature -f
    - Cleanup a branch:
        ./gitflow.py delete -c
    """
    # Update local and remote references
    repo.git.fetch('--all')
    repo.git.remote('prune', 'origin')

    local_branches = [head.name for head in repo.heads]
    remote_branches = [ref.name.replace('origin/', '') for ref in repo.remote().refs if ref.name.startswith('origin/') and ref.name != 'origin/HEAD']

    if not branch_name:
        all_branches = [f"Local: {branch}" for branch in local_branches] + [f"Remote: {branch}" for branch in remote_branches]
        branch_name = inquirer.select(message="Select a branch to delete:", choices=all_branches).execute()

    if "Local: " in branch_name:
        branch_name = branch_name.replace("Local: ", "")
    elif "Remote: " in branch_name:
        branch_name = branch_name.replace("Remote: ", "")

    def check_prs(branch_name: str):
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

    try:
        if branch_name in local_branches:
            try:
                if cleanup:
                    for base_branch in ['main', 'develop']:
                        repo.git.checkout(base_branch)
                        repo.git.pull('origin', base_branch)
                        if repo.git.merge_base(branch_name, base_branch) != repo.git.rev_parse(branch_name):
                            console.print(f"[red]Error: {branch_name} is not fully merged into {base_branch}.[/red]")
                            return
                    console.print(f"[green]Branch {branch_name} is fully merged into main and develop.[/green]")
                
                repo.git.branch('-d' if not force else '-D', branch_name)
                console.print(f"[green]Deleted local branch {branch_name}[/green]")
            except GitCommandError as e:
                console.print(f"[red]Error: {e}[/red]")

        if branch_name in remote_branches:
            # Verify if the branch actually exists on the remote
            remote_branches_actual = [ref.name.replace('origin/', '') for ref in repo.remote().refs]
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
                    except GitCommandError as e:
                        console.print(f"[red]Error deleting remote branch {branch_name}: {e}[/red]")
            else:
                console.print(f"[red]Error: Remote branch {branch_name} does not exist[/red]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Add files to Git
#
@app.command()
def add(
    file_paths: List[str] = typer.Argument(..., help="The path(s) to the file(s) to add")
):
    """
    Add file changes to the staging area.

    Parameters:
    - file_paths: The path(s) to the file(s) to add.

    Examples:
    - Add a single file:
        ./gitflow.py add gitflow.py
    - Add multiple files:
        ./gitflow.py add gitflow.py README.md
    """
    try:
        repo.git.add(file_paths)
        console.print(f"[green]Added {file_paths} to the staging area[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Commit changes
#
@app.command()
def commit(
    message: str = typer.Option(..., "-m", "--message", help="The commit message"),
):
    """
    Commit the current changes with a specified message.

    Parameters:
    - message: The commit message.

    Examples:
    - Commit the current changes:
        ./gitflow.py commit -m "Updated gitflow script"
    """
    try:
        repo.git.add('.')
        if repo.index.diff("HEAD"):
            repo.git.commit('-m', message)
            console.print(f"[green]Committed changes with message: {message}[/green]")
        else:
            console.print(f"[yellow]No changes to commit.[/yellow]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Push changes
#
@app.command()
def push(
    branch: Optional[str] = typer.Argument(None, help="The branch to push changes to"),
    force: bool = typer.Option(False, "-f", "--force", help="Force push changes"),
    create_pr: bool = typer.Option(False, "-p", "--pr", help="Create a pull request instead of pushing directly")
):
    try:
        # Use the current branch if no branch is provided
        if branch is None:
            branch = repo.active_branch.name

        current_branch = repo.active_branch.name

        # Check for unstaged changes
        changes_made = repo.is_dirty(untracked_files=True)

        if changes_made:
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
                repo.git.add('.')
                repo.git.commit('-m', commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Push aborted.[/yellow]")
                return
            # If "Continue without committing" is selected, we just proceed

        # Fetch the latest changes from the remote
        repo.git.fetch('origin')

        # Check if there are differences between local and remote
        try:
            ahead_behind = repo.git.rev_list('--left-right', '--count', f'origin/{branch}...HEAD').split()
            behind = int(ahead_behind[0])
            ahead = int(ahead_behind[1])
            
            if ahead > 0:
                console.print(f"[yellow]Your local branch is {ahead} commit(s) ahead of the remote branch.[/yellow]")
                changes_made = True
            elif not changes_made:
                console.print("[yellow]Your local branch is up to date with the remote branch. No push needed.[/yellow]")
                return
        except GitCommandError:
            # If the remote branch doesn't exist, consider it as having differences
            changes_made = True

        if changes_made or create_pr:
            try:
                if force:
                    repo.git.push('origin', branch, '--force')
                else:
                    repo.git.push('origin', branch)
                console.print(f"[green]Pushed changes to {branch}[/green]")
            except GitCommandError as e:
                if "protected branch" in str(e):
                    console.print(f"[yellow]Protected branch {branch} detected. Creating a new branch for pull request.[/yellow]")
                    # Create a new branch for the pull request
                    new_branch_name = f"update-{branch}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    repo.git.checkout('-b', new_branch_name)
                    repo.git.push('origin', new_branch_name)
                    
                    # Create pull request from the new branch
                    result = subprocess.run(
                        ["gh", "pr", "create", "--base", branch, "--head", new_branch_name,
                         "--title", f"Update {branch}", "--body", "Automated pull request from script"],
                        capture_output=True, text=True
                    )
                    if result.returncode != 0:
                        console.print(f"[red]Error creating pull request: {result.stderr}[/red]")
                    else:
                        console.print(f"[green]Created pull request to merge changes from {new_branch_name} into {branch}[/green]")
                    
                    # Switch back to the original branch
                    repo.git.checkout(current_branch)
                elif "non-fast-forward" in str(e):
                    # Handle non-fast-forward error (code for this part remains the same)
                    pass
                else:
                    raise e

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")

#
# Pull changes
#
@app.command()
def pull(
    all_branches: bool = typer.Option(False, "-a", "--all", help="Pull changes for all local branches")
):
    """
    Pull the committed changes from the remote repository.

    Parameters:
    - all_branches: Pull changes for all local branches if set to True. Defaults to False.

    Examples:
    - Pull changes for the current branch:
        ./gitflow.py pull
    - Pull changes for all local branches:
        ./gitflow.py pull --all
    """
    try:
        original_branch = repo.active_branch.name

        if all_branches:
            console.print("[blue]Pulling changes for all local branches...[/blue]")
            # Fetch all branches from the remote
            repo.git.fetch('--all')

            # Loop through each local branch and pull updates if there are changes
            for branch in repo.branches:
                local_commit = repo.git.rev_parse(branch.name)
                remote_commit = repo.git.rev_parse(f'origin/{branch.name}')

                if local_commit != remote_commit:
                    repo.git.checkout(branch.name)
                    console.print(f"[blue]Updating branch {branch.name}...[/blue]")
                    try:
                        result = subprocess.run(
                            ["git", "pull", "origin", branch.name],
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
            current_branch = repo.active_branch.name
            console.print(f"[blue]Pulling changes for the current branch {current_branch}...[/blue]")
            try:
                result = subprocess.run(
                    ["git", "pull", "origin", current_branch],
                    capture_output=True,
                    text=True
                )
                console.print(f"[green]Pulled changes for branch {current_branch}[/green]")
                console.print(result.stdout)
                if result.stderr:
                    console.print(result.stderr)
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Error pulling changes for branch {current_branch}: {e}[/red]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Compare
#
@app.command()
def compare(
    file_path: str = typer.Argument(..., help="The path to the file to compare"),
    branch1: Optional[str] = typer.Argument(None, help="The first branch to compare"),
    branch2: Optional[str] = typer.Argument(None, help="The second branch to compare")
):
    """
    Compare the same file in two different branches.

    Parameters:
    - file_path: The path to the file to compare.
    - branch1: The first branch to compare.
    - branch2: The second branch to compare.

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
    file_path    : str           = typer.Argument(...,           help="The path to the file to copy the latest commit for"),
    target_branch: Optional[str] = typer.Argument(None,          help="The target branch to copy into"),
    push         : bool          = typer.Option(True,  "--push", help="Push the changes to the remote repository after copying")
):
    """
    Copy the latest commit of a specific file from the current branch into a target branch.

    Parameters:
    - file_path: The path to the file to copy the latest commit for.
    - target_branch: The target branch to copy into.
    - push: Push the changes to the remote repository after copying if the remote branch exists.

    Examples:
    - Copy the latest commit of gitflow.py into a feature branch:
        ./gitflow.py cp gitflow.py feature/new-feature --push
    """
    try:
        # Save the current branch
        original_branch = repo.active_branch.name

        # Find the latest commit hash for the specific file
        latest_commit = repo.git.log('-n', '1', '--pretty=format:%H', '--', file_path)

        if not latest_commit:
            console.print(f"[red]Error: No commits found for {file_path}[/red]")
            return

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
            # Cherry-pick the latest commit
            try:
                result = subprocess.run(["git", "cherry-pick", latest_commit], capture_output=True, text=True)
                if result.returncode != 0:
                    console.print(f"[red]Cherry-pick resulted in conflicts. Please resolve them and run 'git cherry-pick --continue' or 'git cherry-pick --abort'.[/red]")
                    console.print(result.stderr)
                    console.print("[yellow]To see the conflicts, run 'git status' and check the conflicted files.[/yellow]")
                    return
                else:
                    console.print(f"[green]Copied the latest commit for {file_path} into {target_branch}[/green]")

            except subprocess.CalledProcessError as e:
                console.print(f"[red]Cherry-pick resulted in conflicts. Please resolve them and run 'git cherry-pick --continue' or 'git cherry-pick --abort'.[/red]")
                return

            # Optionally push the changes if the --push flag is set and the remote branch exists
            if push:
                try:
                    remote_branches = [branch for branch in repo.git.branch('-r').split('\n') if 'origin/HEAD' not in branch]
                    remote_branch_exists = any(f'origin/{target_branch}' in branch for branch in remote_branches)

                    if remote_branch_exists:
                        repo.git.push('origin', target_branch)
                        console.print(f"[green]Pushed changes to {target_branch}[/green]")
                    else:
                        console.print(f"[yellow]Remote branch {target_branch} does not exist. Skipping push.[/yellow]")
                except GitCommandError as e:
                    console.print(f"[red]Error while pushing: {e}[/red]")

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
