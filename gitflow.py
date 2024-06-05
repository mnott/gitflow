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

### Cherry-pick a File

To cherry-pick the latest commit of a specific file from the current branch into a target branch, run:

```bash
./gitflow.py pick gitflow.py feature/new-feature
```

# License

This script is released under the WTFP License.

"""


import sys
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

def get_next_semver(increment: str) -> str:
    """Generate the next Semantic Versioning (SemVer) tag."""
    tags = [tag.name for tag in repo.tags if tag.name.startswith("v")]
    if not tags:
        return "v1.0.0"

    tags.sort()
    latest_tag = tags[-1]
    major, minor, patch = map(int, latest_tag[1:].split('.'))

    if increment == "major":
        major += 1
        minor = 0
        patch = 0
    elif increment == "minor":
        minor += 1
        patch = 0
    elif increment == "patch":
        patch += 1

    return f"v{major}.{minor}.{patch}"


#
# Start a branch
#
@app.command()
def start(
    name:        Optional[str] = typer.Option(None,     "-n", "--name",      help="Specify the feature, hotfix, or release name"),
    branch_type: str           = typer.Option("hotfix", "-t", "--type",      help="Specify the branch type: hotfix, feature, or release"),
    week:        Optional[int] = typer.Option(None,     "-w", "--week",      help="Specify the calendar week"),
    increment:   str           = typer.Option("patch",  "-i", "--increment", help="Specify the version increment type: major, minor, patch"),
    message:     Optional[str] = typer.Option(None,     "-m", "--message",   help="Specify a commit message")
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

    Examples:
    - Start a weekly update hotfix branch (e.g. for some minor weekly updates):
        ./gitflow.py start
    - Start a new hotfix branch:
        ./gitflow.py start -t hotfix  -n "critical-bugfix" -m "Starting critical bugfix hotfix"
    - Start a new feature branch:
        ./gitflow.py start -t feature -n "new-feature"     -m "Starting new feature"
    - Start a new release branch:
        ./gitflow.py start -t release -m "Starting release" -i "patch"

    The name is optional for a release (and for a weekly hotfix branch); if not given, those values will be auto-generated.
    """
    version_tag = None
    if name and branch_type != "release":
        branch_name = f"{branch_type}/{name}"
    elif branch_type == "hotfix":
        week_number = get_week_number(week)
        branch_name = f"hotfix/week-{week_number}"
    elif branch_type == "release":
        version_tag = get_next_semver(increment)
        if name is None:
            name = version_tag
        branch_name = f"release/{name}"
    else:
        console.print("[red]Error: A feature or release branch must have a name[/red]")
        return

    base_branch = 'main' if branch_type == 'hotfix' else 'develop'

    try:
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
    name:          Optional[str] = typer.Option(None,      "-n",  "--name",          help="Specify the feature, hotfix, or release name"),
    branch_type:   str           = typer.Option("hotfix",  "-t",  "--type",          help="Specify the branch type: hotfix, feature, or release"),
    week:          Optional[int] = typer.Option(None,      "-w",  "--week",          help="Specify the calendar week"),
    message:       Optional[str] = typer.Option(None,      "-m",  "--message",       help="Specify a commit message"),
    target_branch: Optional[str] = typer.Option("develop", "-tb", "--target-branch", help="Specify the branch to merge hotfix into"),
    delete:        bool          = typer.Option(True,      "-d",  "--delete",        help="Delete the feature, hotfix, or release branch after merging")
):
    """
    Finish the feature, hotfix, or release by merging into main and/or develop, then tagging the update.

    Parameters:
    - name         : The name of the feature, hotfix, or release branch.
    - branch_type  : The type of branch to finish ('hotfix', feature, or 'release').
    - week         : The calendar week for a weekly hotfix branch.
    - message      : An optional commit message.
    - target_branch: The branch to merge hotfix into (default is 'develop').
    - delete       : Whether to delete the feature, hotfix, or release branch after merging.

    Examples:
    - Finish a weekly update hotfix branch:
        ./gitflow.py finish
    - Finish a hotfix branch:
        ./gitflow.py finish -t hotfix  -n "critical-bugfix" -m "Finishing critical bugfix hotfix"
    - Finish a feature branch:
        ./gitflow.py finish -t feature -n "new-feature"     -m "Finishing new feature"
    - Finish a release branch:
        ./gitflow.py finish -t release -n "v1.4.5"          -m "Finishing release."

    You must always give the name of the feature, hotfix, or release branch to finish, except if you
    are finishing a weekly hotfix branch in which case the name will be auto-generated.
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
                default_message = "Finish feature, hotfix, or release."
                repo.git.commit('-m', default_message)
                console.print(f"[green]Committed changes with default message: {default_message}[/green]")
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")

        # Ensure the branch is checked out before merging
        repo.git.checkout(branch_name)

        if branch_type == "hotfix" or branch_type == "release":
            # Merge hotfix or release branch into main
            repo.git.checkout('main')
            repo.git.pull('origin', 'main')
            repo.git.merge(branch_name, '--no-ff')
            repo.git.push('origin', 'main')

        # Determine the target branch for merging
        merge_target_branch = 'develop'
        if branch_type == "hotfix" and target_branch:
            merge_target_branch = target_branch

        # Merge feature, hotfix, or release branch into develop
        repo.git.checkout(merge_target_branch)
        repo.git.pull('origin', merge_target_branch)
        repo.git.merge(branch_name, '--no-ff')
        repo.git.push('origin', merge_target_branch)

        console.print(f"[green]Merged {branch_name} into {'main and ' if branch_type in ['hotfix', 'release'] else ''}develop[/green]")

        # Delete the feature, hotfix, or release branch if specified and if it exists remotely
        if delete:
            repo.git.branch('-d', branch_name)
            try:
                repo.git.push('origin', '--delete', branch_name)
                console.print(f"[green]Deleted branch {branch_name}[/green]")
            except GitCommandError:
                console.print(f"[yellow]Branch {branch_name} does not exist on the remote and cannot be deleted there[/yellow]")
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
    List all branches.

    Examples:
    - List all branches:
        ./gitflow.py ls
    """
    branches = [head.name for head in repo.heads]
    branches.sort()  # Sort the branches list
    for branch in branches:
        console.print(f"[cyan]{branch}[/cyan]")


#
# Checkout a branch
#
@app.command()
def checkout():
    """
    Switch to a different branch using an interactive menu.

    Examples:
    - Switch to a different branch:
        ./gitflow.py checkout
    """
    branches = [head.name for head in repo.heads]
    branch = inquirer.select(message="Select a branch:", choices=branches).execute()
    try:
        repo.git.checkout(branch)
        console.print(f"[green]Switched to branch {branch}[/green]")
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
    branch: str = typer.Argument(..., help="The branch to push changes to")
):
    """
    Push the committed changes to the remote repository.

    Parameters:
    - branch: The branch to push changes to.

    Examples:
    - Push changes to the current branch:
        ./gitflow.py push
    - Push changes to a specific branch:
        ./gitflow.py push feature/new-feature
    """
    try:
        repo.git.push('origin', branch)
        console.print(f"[green]Pushed changes to {branch}[/green]")
    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")


#
# Cherry-pick a file from the current branch into a target branch
#
@app.command()
def pick(
    file_path    : str           = typer.Argument(...,  help="The path to the file to cherry-pick the latest commit for"),
    target_branch: Optional[str] = typer.Argument(None, help="The target branch to cherry-pick into")
):
    """
    Cherry-pick the latest commit of a specific file from the current branch into a target branch.

    Parameters:
    - file_path: The path to the file to cherry-pick the latest commit for.
    - target_branch: The target branch to cherry-pick into.

    Examples:
    - Cherry-pick the latest commit of gitflow.py into a feature branch:
        ./gitflow.py pick gitflow.py feature/new-feature
    """
    try:
        # Find the latest commit hash for the specific file
        latest_commit = repo.git.log('-n', '1', '--pretty=format:%H', '--', file_path)

        if not latest_commit:
            console.print(f"[red]Error: No commits found for {file_path}[/red]")
            return

        # Read the file content before switching branches
        try:
            with open(file_path, 'r') as source_file:
                file_content = source_file.read()
        except FileNotFoundError:
            console.print(f"[red]Error: {file_path} not found in the current branch[/red]")
            return

        # If target_branch is not provided, show a list of branches to select from
        if not target_branch:
            branches = [head.name for head in repo.heads if head.name != repo.active_branch.name]
            target_branch = inquirer.select(message="Select a branch to cherry-pick into:", choices=branches).execute()

        # Checkout the target branch
        repo.git.checkout(target_branch)
        console.print(f"[green]Switched to branch {target_branch}[/green]")

        # Check if the file exists in the target branch
        file_exists = Path(file_path).exists()

        if not file_exists:
            # If the file does not exist, add it manually from the current branch content
            with open(file_path, 'w') as target_file:
                target_file.write(file_content)
            repo.git.add(file_path)
            repo.git.commit('-m', f"Add {file_path} to enable cherry-pick")
            console.print(f"[green]Added {file_path} to {target_branch} manually[/green]")

        # Cherry-pick the latest commit
        try:
            repo.git.cherry_pick(latest_commit)

            # Handle conflicts
            if repo.index.unmerged_blobs():
                console.print(f"[red]Cherry-pick resulted in conflicts. Please resolve them and run 'git cherry-pick --continue' or 'git cherry-pick --abort'.[/red]")
            else:
                console.print(f"[green]Cherry-picked the latest commit for {file_path} into {target_branch}[/green]")

                # Push the changes to the remote repository
                repo.git.push('origin', target_branch)
                console.print(f"[green]Pushed changes to {target_branch}[/green]")
        except GitCommandError as e:
            console.print(f"[red]Cherry-pick resulted in conflicts. Please resolve them and run 'git cherry-pick --continue' or 'git cherry-pick --abort'.[/red]")
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
