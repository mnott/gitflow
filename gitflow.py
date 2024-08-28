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

# License

This script is released under the [WTFPL License](https://en.wikipedia.org/wiki/WTFPL).
"""

import os
import shutil
import glob
from datetime import datetime, timedelta
from collections import defaultdict
from rich import print
from rich import traceback
from rich import pretty
from rich.console import Console
from rich.table import Table
from rich import box
import typer
from typing import Optional, List
from InquirerPy import inquirer
from git import Repo, GitCommandError

import json
import re

import tempfile
import subprocess
import os

# Local imports
from client import AIClient, GitConfig, DocGenerator, GitWrapper

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
    name:         Optional[str] = typer.Argument(None,                         help="Specify the feature, local, hotfix, release, or backup name"),
    branch_type:            str = typer.Option("local", "-t", "--type",        help="Specify the branch type: local, hotfix, feature, release, or backup"),
    week:         Optional[int] = typer.Option(None,    "-w", "--week",        help="Specify the calendar week"),
    increment:              str = typer.Option("patch", "-i", "--increment",   help="Specify the version increment type: major, minor, patch"),
    message:      Optional[str] = typer.Option(None,    "-m", "--message",     help="Specify a commit message"),
    skip_switch:           bool = typer.Option(False,   "-s", "--skip-switch", help="Skip switching to main or develop branch before creating the new branch")
):
    """
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
    """
    offline = not git_wrapper.check_network_connection()
    if offline:
        console.print("[yellow]Network is unavailable. Operating in offline mode.[/yellow]")

    version_tag = None
    existing_tags = git_wrapper.get_tags()

    if branch_type == "hotfix" and name is None:
        week_number = git_wrapper.get_week_number(week)
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
            # Checkout base branch
            git_wrapper.checkout(base_branch)
            if not offline:
                # Pull the latest changes if online
                git_wrapper.pull('origin', base_branch)
            else:
                console.print(f"[yellow]Skipping pull from {base_branch} due to offline mode.[/yellow]")

        # Check if the branch already exists
        if branch_name in git_wrapper.get_branches():
            git_wrapper.checkout(branch_name)
            console.print(f"[yellow]Switched to existing branch {branch_name}[/yellow]")
        else:
            # Create and checkout the new branch
            git_wrapper.checkout(branch_name, create=True)
            console.print(f"[green]Created and switched to branch {branch_name}[/green]")

        if message:
            # Commit the initial changes if a message is provided
            git_wrapper.add('.')
            if git_wrapper.get_index_diff("HEAD"):
                git_wrapper.commit(message)
                console.print(f"[green]Initial commit with message: {message}[/green]")
            else:
                console.print(f"[yellow]No changes to commit.[/yellow]")

        if branch_type == "release" and version_tag:
            # Create the tag locally, but don't push it yet
            git_wrapper.create_tag(version_tag, message=f"Release {version_tag}")
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
    delete: bool = typer.Option(True, "-d", "--delete", help="Delete the branch after finishing"),
    keep_local: bool = typer.Option(False, "-k", "--keep-local", help="Keep the local branch after finishing")
):
    """
    Finish the current feature, hotfix, or release branch by creating pull requests for main and/or develop.
    Must be run from the branch that is being finished.
    """
    try:
        current_branch = git_wrapper.get_current_branch()

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

        if not handle_unstaged_changes(branch_type):
            return

        offline = not git_wrapper.check_network_connection()

        if offline:
            console.print("[yellow]Network is unavailable. Operating in offline mode.[/yellow]")
        else:
            fetch(remote="origin", branch=None, all_remotes=False, prune=False)

        push_changes = git_wrapper.push_to_remote(current_branch)

        if not push_changes:
            console.print("[yellow]No changes to push. Finishing operation.[/yellow]")
            return

        target_branches = ["main", "develop"] if branch_type in ["hotfix", "release"] else ["develop"]

        # For release branches, push the tag before merging
        if branch_type == 'release' and not offline:
            tag_name = current_branch.split('/')[-1]
            try:
                git_wrapper.push('origin', tag_name)
                console.print(f"[green]Pushed tag {tag_name} to remote[/green]")
            except GitCommandError as e:
                console.print(f"[yellow]Warning: Failed to push tag {tag_name}. Error: {e}[/yellow]")

        merge_successful = all(git_wrapper.merge_to_target(current_branch, target) for target in target_branches)

        if merge_successful:
            if delete and not keep_local:
                git_wrapper.delete_branch(current_branch)  # This will delete both local and remote
                git_wrapper.cleanup_temp_branches()  # This will only delete local temp branches
            elif keep_local:
                console.print(f"[yellow]Keeping local branch {current_branch} as requested.[/yellow]")
        else:
            console.print(f"[yellow]Branch {current_branch} not deleted due to merge issues.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")



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
):
    """
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
    """
    try:
        # Remember the current branch
        original_branch = git_wrapper.get_current_branch()

        # Determine the branch name from the local path
        branch_name = local.replace("/", "-")

        # Step 1: Clone or update remote tenantcleanup-cds repository
        temp_repo_path = os.path.join(git_wrapper.get_working_tree_dir(), "temp-tenantcleanup-cds")
        if os.path.exists(temp_repo_path):
            temp_repo = Repo(temp_repo_path)
            temp_repo.remotes.origin.pull()
            console.print("[green]Updated remote tenantcleanup-cds repository[/green]")
        else:
            Repo.clone_from(remote, temp_repo_path)
            console.print("[green]Cloned remote tenantcleanup-cds repository[/green]")

        # Step 2: Switch to the specified branch
        if branch_name in git_wrapper.get_branches():
            git_wrapper.checkout(branch_name)
        else:
            git_wrapper.checkout(branch_name, create=True)
        console.print(f"[green]Switched to {branch_name} branch[/green]")

        # Step 3: Copy contents
        local_path = os.path.join(git_wrapper.get_working_tree_dir(), local)
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        shutil.copytree(temp_repo_path, local_path)
        console.print(f"[green]Copied contents from remote repository to /{local}[/green]")

        # Step 4: Commit and push changes
        git_wrapper.add(local_path)
        if git_wrapper.is_dirty():
            # Get the commit message
            full_commit_message = get_commit_message(message or f"Sync changes from remote tenantcleanup-cds to {local}", body)

            git_wrapper.commit(full_commit_message)
            console.print("[green]Changes committed.[/green]")

            git_wrapper.push("origin", branch_name)
            console.print(f"[green]Pushed changes to {branch_name} branch[/green]")
        else:
            console.print("[yellow]No changes to commit.[/yellow]")

        # Step 5: Create pull requests for main and develop branches
        def create_cds_pr(base_branch: str):
            try:
                result = subprocess.run(
                    ["gh", "pr", "create", "--base", base_branch, "--head", branch_name,
                     "--title", f"Merge CDS view updates into {base_branch}",
                     "--body", full_commit_message if 'full_commit_message' in locals() else f"Syncing CDS views from {remote} to {local}"],
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

        prs_created_develop = create_cds_pr("develop")
        prs_created_main = create_cds_pr("main")

        if prs_created_develop or prs_created_main:
            console.print(f"[yellow]Pull requests created to merge {branch_name} into main and/or develop.[/yellow]")
        else:
            console.print(f"[yellow]No pull requests were created as there were no differences to merge.[/yellow]")

        # Return to the original branch
        git_wrapper.checkout(original_branch)
        console.print(f"[green]Returned to branch {original_branch}[/green]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        # Clean up: remove the temporary cloned repository
        if os.path.exists(temp_repo_path):
            shutil.rmtree(temp_repo_path)


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
def ls():
    """
    List all branches, including both local and remote.

    Examples:
    - List all branches:
        ./gitflow.py ls
    """
    git_wrapper.fetch('--all', '--prune')
    local_branches  = git_wrapper.get_local_branches()
    remote_branches = git_wrapper.get_remote_branches()

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
    offline = not git_wrapper.check_network_connection()

    try:
        if target is None:
            # Interactive branch selection
            local_branches = [f"Local : {head.name}" for head in git_wrapper.get_heads()]
            if not offline:
                remote_branches = [f"Remote: {ref.name.replace('origin/', '')}" for ref in git_wrapper.get_origin_refs() if ref.name != 'origin/HEAD']
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
        if target in git_wrapper.get_branches() or (not offline and target.startswith("origin/")):
            # Check if there are uncommitted changes
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

    # If changes were stashed, ask if the user wants to pop them
    if 'action' in locals() and action == "Stash changes":
        pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
        if pop_stash:
            try:
                git_wrapper.stash('pop')
                console.print("[green]Stashed changes reapplied.[/green]")
            except GitCommandError as e:
                console.print(f"[red]Error reapplying stashed changes: {e}[/red]")
                console.print("[yellow]Your changes are still in the stash. You may need to manually resolve conflicts.[/yellow]")


#
# Delete a branch
#
@app.command()
def rm(
    branch_names: Optional[List[str]] = typer.Argument(None, help="The branch name(s) to delete"),
    force: bool = typer.Option(False, "-f", "--force", help="Force delete the branch, even if it's not fully merged or has open pull requests"),
    all: bool = typer.Option(False, "-a", "--all", help="Delete both local and remote branches with the same name")
):
    """
    Delete one or more branches using an interactive menu or by specifying the branch names.
    """
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
        all_branches = [f"Local: {branch}" for branch in local_branches]
        if git_wrapper.check_network_connection():
            all_branches += [f"Remote: {branch}" for branch in remote_branches]

        selected_branches = inquirer.checkbox(
            message="Select branch(es) to delete:",
            choices=all_branches
        ).execute()

        if not selected_branches:
            console.print("[yellow]No branches selected. Operation aborted.[/yellow]")
            return
    else:
        selected_branches = branch_names

    for branch in selected_branches:
        if "Local: " in branch:
            branch_name = branch.replace("Local: ", "")
            delete_local = True
            delete_remote = False
        elif "Remote: " in branch:
            branch_name = branch.replace("Remote: ", "")
            delete_local = False
            delete_remote = True
        else:
            branch_name = branch
            delete_local = True
            delete_remote = all and git_wrapper.check_network_connection()

        if branch_name in ['develop', 'main']:
            console.print(f"[red]Error: You cannot delete the {branch_name} branch. Skipping.[/red]")
            continue

        if delete_remote and check_prs(branch_name) and not force:
            console.print(f"[yellow]There are open pull requests for the branch {branch_name}. Use -f to force delete the remote branch. Skipping.[/yellow]")
            continue

        git_wrapper.delete_branch(branch_name, delete_remote=delete_remote)

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
        if api_key and (interactive or not message):
            full_commit_message = get_commit_message(message, body)
        else:
            full_commit_message = get_manual_commit_message(message, body)

        # Show the full commit message and ask for confirmation
        confirm = True

        if interactive:
            console.print(f"[blue]Full commit message:[/blue]\n{full_commit_message}")
            confirm = inquirer.confirm(message="Do you want to proceed with this commit?", default=True).execute()

        if not confirm:
            console.print("[yellow]Commit aborted.[/yellow]")
            return

        # Perform the commit
        git_wrapper.commit(full_commit_message)
        console.print(f"[green]Committed changes with message:[/green]\n{full_commit_message}")

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

def get_manual_commit_message(message, body):
    if not message:
        message = inquirer.text(message="Enter commit message:").execute()
    if not body:
        body = inquirer.text(message="Enter commit body (optional, press enter to skip):", default="").execute()

    full_commit_message = message
    if body:
        full_commit_message += "\n\n" + split_message_body(body)

    return full_commit_message


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
        print(f"Generating a commit message using: {current_provider}")

        generated_message = ai_client.prompt(prompt)

        if as_command:
            # Function was called as a command
            console.print("[green]Generated explanation:[/green]")
            console.print(generated_message)
        else:
            # Function was called programmatically
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
    original_branch = git_wrapper.get_current_branch()
    try:
        # Check if we're in the middle of a merge
        if git_wrapper.status('--porcelain', '--untracked-files=no') and os.path.exists(git_wrapper.get_git_dir() + '/MERGE_HEAD'):
            console.print("[yellow]Continuing previous merge...[/yellow]")
            return continue_merge()

        # Use the current branch if no source is provided
        if source is None:
            source = git_wrapper.get_current_branch()

        # If no target is provided, use the current branch
        if target is None:
            target = git_wrapper.get_current_branch()

        # Check for unstaged changes
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
                api_key = git_wrapper.get_git_metadata("openai.apikey")
                if api_key:
                    use_ai = inquirer.confirm(message="Do you want to use AI to generate a commit message?", default=True).execute()
                    if use_ai:
                        generated_message = explain(files=None, commit=None, start=None, end=None, as_command=False, days=None, daily_summary=False, summary=False, improve=False, custom_prompt=None, examples=False)
                        if generated_message:
                            console.print("[green]AI-generated commit message:[/green]")
                            console.print(generated_message)

                            edit_message = inquirer.confirm(message="Do you want to edit this message?", default=True).execute()
                            if edit_message:
                                full_commit_message = edit_in_editor(generated_message)
                            else:
                                full_commit_message = generated_message
                        else:
                            console.print("[yellow]Failed to generate AI message. Falling back to manual entry.[/yellow]")
                            full_commit_message = git_wrapper.get_manual_commit_message()
                    else:
                        full_commit_message = git_wrapper.get_manual_commit_message()
                else:
                    full_commit_message = git_wrapper.get_manual_commit_message()

                git_wrapper.add('.')
                git_wrapper.commit(full_commit_message)
                console.print("[green]Changes committed.[/green]")
            elif action == "Stash changes":
                git_wrapper.stash('save', f"Stashed changes before merging {source} into {target}")
                console.print("[green]Changes stashed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Merge operation aborted.[/yellow]")
                return

        # Check if the merge can be fast-forwarded
        merge_base = git_wrapper.merge_base(target, source).strip()
        target_head = git_wrapper.rev_parse(target).strip()
        source_head = git_wrapper.rev_parse(source).strip()

        if merge_base == target_head:
            console.print(f"[green]Fast-forwarding {target} to {source}[/green]")
            git_wrapper.checkout(target)
            git_wrapper.merge(source, ff_only=True)
            return

        # Check if there are differences between branches
        try:
            rev_list = git_wrapper.rev_list('--left-right', '--count', f'{target}...{source}')
            ahead, behind = map(int, rev_list.split())
            if ahead == 0 and behind == 0:
                console.print(f"[yellow]No differences found between {source} and {target}. No merge needed.[/yellow]")
                return
            else:
                console.print(f"[blue]Found differences: {source} is {behind} commit(s) behind and {ahead} commit(s) ahead of {target}.[/blue]")
        except GitCommandError:
            console.print(f"[yellow]Unable to determine differences between {source} and {target}. Proceeding with merge.[/yellow]")

        # Perform the merge
        git_wrapper.checkout(target)

        try:
            # Force conflict detection by using --no-commit
            if squash:
                git_wrapper.merge(source, squash=True, commit=False)
            else:
                git_wrapper.merge(source, no_ff=no_ff, commit=False)

        except GitCommandError as e:
            console.print(f"[yellow]Merge conflicts detected. Please resolve the conflicts.[/yellow]")
            # Ensure the conflict markers are in place before proceeding
            status = git_wrapper.status('--porcelain')
            if any(line.startswith('UU') for line in status.split('\n')):
                return continue_merge()
            else:
                console.print("[red]Error: Merge conflicts detected, but no conflict markers found. Aborting merge.[/red]")
                git_wrapper.merge(abort=True)
                return

        # Check for conflicts
        status = git_wrapper.status('--porcelain')
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
                    status = git_wrapper.status('--porcelain')
                    if not any(line.startswith('UU') for line in status.split('\n')):
                        console.print("[green]Conflicts resolved. Continuing merge...[/green]")
                        git_wrapper.commit(f"Merge branch '{source}' into {target}")
                        # Cleanup .orig files
                        for file in glob.glob('*.orig'):
                            os.remove(file)
                    else:
                        console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Error running git mergetool: {e}[/red]")
                return
            elif action == "Abort merge":
                git_wrapper.merge(abort=True)
                console.print("[yellow]Merge aborted.[/yellow]")
            else:
                console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
            return
        else:
            # No conflicts, complete the merge
            if git_wrapper.is_dirty():  # Check if there are changes to commit
                git_wrapper.commit(f"Merge branch '{source}' into {target}")
                console.print(f"[green]Successfully merged {source} into {target}.[/green]")
            else:
                console.print(f"[yellow]Merge completed but there were no changes to commit.[/yellow]")

    except GitCommandError as e:
        console.print(f"[red]Error: {e}[/red]")

    finally:
        # Only checkout the original branch if there are no unresolved conflicts
        if 'original_branch' in locals() and not any(line.startswith('UU') for line in git_wrapper.status('--porcelain').split('\n')):
            git_wrapper.checkout(original_branch)
            console.print(f"[green]Returned to {original_branch}[/green]")

            # If changes were stashed, ask if the user wants to pop them
            if 'action' in locals() and action == "Stash changes":
                pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
                if pop_stash:
                    try:
                        git_wrapper.stash('pop')
                        console.print("[green]Stashed changes reapplied.[/green]")
                    except GitCommandError as e:
                        console.print(f"[red]Error reapplying stashed changes: {e}[/red]")
                        console.print("[yellow]Your changes are still in the stash. You may need to manually resolve conflicts.[/yellow]")


def continue_merge():
    try:
        # Check if there are still conflicts
        status = git_wrapper.status('--porcelain')
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
                    status = git_wrapper.status('--porcelain')
                    if not any(line.startswith('UU') for line in status.split('\n')):
                        console.print("[green]Conflicts resolved. Continuing merge...[/green]")
                        git_wrapper.commit("Merge conflicts resolved")
                        # Cleanup .orig files
                        for file in glob.glob('*.orig'):
                            os.remove(file)
                    else:
                        console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Error running git mergetool: {e}[/red]")
                return
            elif action == "Abort merge":
                git_wrapper.merge(abort=True)
                console.print("[yellow]Merge aborted.[/yellow]")
            else:
                console.print("[yellow]Please resolve conflicts, stage the changes, and run the merge command again to continue.[/yellow]")
        else:
            # Changes staged but not committed
            git_wrapper.commit('--no-edit')
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
            branch = git_wrapper.get_current_branch()

        current_branch = git_wrapper.get_current_branch()

        # Check for unstaged changes
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
                git_wrapper.stash('save', f"Stashed changes before finishing {branch}")
                console.print("[green]Changes stashed.[/green]")
            elif action == "Abort":
                console.print("[yellow]Push aborted.[/yellow]")
                return

        offline = not git_wrapper.check_network_connection()

        if not offline:
            # Use our custom fetch function
            fetch(remote="origin", branch=None, all_remotes=False, prune=False)

            # Check if there are differences between local and remote
            changes_made = False
            try:
                print(f"[blue]Checking differences between {branch} and origin/{branch}[/blue]")
                ahead_behind = git_wrapper.rev_list('--left-right', '--count', f'origin/{branch}...HEAD').split()
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
                            git_wrapper.pull('--rebase', 'origin', branch)
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
                            git_wrapper.push('origin', branch, '--force')
                        else:
                            git_wrapper.push('origin', branch)
                        console.print(f"[green]Pushed changes to {branch}[/green]")
                    else:
                        console.print("[yellow]No network connection. Changes will be pushed when online.[/yellow]")
            except (GitCommandError, subprocess.CalledProcessError) as e:
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
    if not git_wrapper.check_network_connection():
        console.print("[red]Error: No network connection. Unable to pull.[/red]")
        return

    try:
        original_branch = git_wrapper.get_current_branch()
        stashed_changes = False

        # Fetch changes first
        fetch_args = ['--all'] if all_branches else [remote]
        if prune:
            fetch_args.append('--prune')
        git_wrapper.fetch(*fetch_args)
        console.print("[green]Fetched changes from remote.[/green]")

        if all_branches:
            console.print("[blue]Pulling changes for all local branches...[/blue]")

            # Check for uncommitted changes before starting
            if git_wrapper.is_dirty(untracked_files=True):
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
                    stashed_changes = True
                elif action == "Abort":
                    console.print("[yellow]Operation aborted.[/yellow]")
                    return

            # Loop through each local branch and pull updates if there are changes
            for branch in git_wrapper.get_branches():
                local_commit = git_wrapper.rev_parse(branch.name)
                remote_commit = git_wrapper.rev_parse(f'{remote}/{branch.name}')

                if local_commit != remote_commit:
                    git_wrapper.checkout(branch.name)
                    console.print(f"[blue]Updating branch {branch.name}...[/blue]")
                    try:
                        result = git_wrapper.pull(remote, branch.name, rebase=rebase)
                        console.print(f"[green]Pulled changes for branch {branch.name}[/green]")
                        console.print(result)
                    except GitCommandError as e:
                        console.print(f"[red]Error pulling changes for branch {branch.name}: {e}[/red]")
                else:
                    console.print(f"[yellow]Branch {branch.name} is up to date.[/yellow]")

            # Return to the original branch
            git_wrapper.checkout(original_branch)
            console.print(f"[green]Returned to branch {original_branch}[/green]")
        else:
            # Pull changes for the current branch
            current_branch = branch or git_wrapper.get_current_branch()
            console.print(f"[blue]Pulling changes for branch {current_branch}...[/blue]")

            if git_wrapper.is_dirty(untracked_files=True):
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
                        git_wrapper.stash('push', message=stash_message)
                    else:
                        git_wrapper.stash('push')
                    console.print("[green]Changes stashed.[/green]")
                    stashed_changes = True
                elif action == "Abort":
                    console.print("[yellow]Pull aborted.[/yellow]")
                    return

            try:
                result = git_wrapper.pull(remote, current_branch, rebase=rebase)
                console.print(f"[green]Pulled changes for branch {current_branch}[/green]")
                console.print(result)
            except GitCommandError as e:
                console.print(f"[red]Error pulling changes for branch {current_branch}: {e}[/red]")

        # After successful pull, ask if user wants to pop the stash
        if stashed_changes:
            pop_stash = inquirer.confirm(message="Do you want to pop the stashed changes?", default=True).execute()
            if pop_stash:
                try:
                    git_wrapper.stash('pop')
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
    file_path:      str           = typer.Argument(...,                 help="The path to the file to copy the latest commit for"),
    target_branches: List[str]    = typer.Argument(None,                help="The target branch(es) to copy into"),
    push:           bool          = typer.Option  (True, "--push",      help="Push the changes to the remote repository after copying"),
    create_pr:      bool          = typer.Option  (False, "-p", "--pr", help="Create a pull request instead of pushing directly")
):
    """
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
    """
    try:
        offline = not git_wrapper.check_network_connection()

        # Save the current branch
        original_branch = git_wrapper.get_current_branch()

        # Read the file content in the current branch
        try:
            with open(file_path, 'r') as source_file:
                current_branch_file_content = source_file.read()
        except FileNotFoundError:
            console.print(f"[red]Error: {file_path} not found in the current branch[/red]")
            return

        # If target_branches is not provided, show a list of branches to select from
        if not target_branches:
            branches = [head.name for head in git_wrapper.get_heads() if head.name != git_wrapper.get_current_branch()]
            target_branches = inquirer.checkbox(
                message="Select branch(es) to copy into:",
                choices=branches
            ).execute()

        for target_branch in target_branches:
            # Checkout the target branch
            git_wrapper.checkout(target_branch)
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
                console.print(f"[yellow]File {file_path} is identical in {target_branch}. Skipping copy.[/yellow]")
            else:
                # Write the content from the current branch into the target branch
                with open(file_path, 'w') as target_file:
                    target_file.write(current_branch_file_content)

                # Commit the change
                git_wrapper.add(file_path)
                commit_message = f"Copy latest changes for {file_path} from {original_branch} to {target_branch}"
                git_wrapper.commit(commit_message)
                console.print(f"[green]Copied the latest changes for {file_path} into {target_branch}[/green]")

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
# Clone an existing issue
#
@app.command()
def clone_issue(
    issue_number:       int = typer.Argument(..., help="The number of the issue to clone"),
    empty_checkboxes: bool  = typer.Option  (True, "--empty-checkboxes/--keep-checkboxes", help="Empty checkboxes in the description"),
    replace: Optional[str]  = typer.Option  (None, "--replace", help="String or regex pattern to replace in the title"),
    with_str: Optional[str] = typer.Option  (None, "--with", help="String to replace with in the title"),
    regex:             bool = typer.Option  (False, "--regex", help="Use regex for string replacement in title")
):
    """
    Clone an existing issue, creating a new issue with the same metadata and comments.

    Parameters:
    - issue_number: The number of the issue to clone.
    - empty_checkboxes: Whether to empty checkboxes in the description (default: True).
    - replace: String or regex pattern to replace in the title.
    - with_str: String to replace with in the title.
    - regex: Use regex for string replacement in title.

    Examples:
    - Clone issue #245 and empty checkboxes:
        ./gitflow.py clone_issue 245
    - Clone issue #245, keep checkboxes, and replace 'CW35' with 'CW36' in the title:
        ./gitflow.py clone_issue 245 --keep-checkboxes --replace "CW35" --with "CW36"
    - Use regex to replace 'CW' followed by any digits with 'CW36' in the title:
        ./gitflow.py clone_issue 245 --replace "CW[0-9]+" --with "CW36" --regex
    """
    try:
        # Fetch the original issue details
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number), "--json", "title,body,labels,assignees"],
            capture_output=True, text=True, check=True
        )
        issue_data = json.loads(result.stdout)

        # Modify the body to empty checkboxes if requested
        if empty_checkboxes:
            issue_data['body'] = re.sub(r'\[x\]', '[ ]', issue_data['body'])

        # Replace string in title if requested
        if replace and with_str:
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
            create_cmd.extend(["--label", label['name']])

        # Add assignees
        for assignee in issue_data['assignees']:
            create_cmd.extend(["--assignee", assignee['login']])

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
        console.print(f"[red]Error: {e.stderr}[/red]")
        console.print(f"[red]Command that failed: {' '.join(e.cmd)}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print(f"[red]Error type: {type(e).__name__}[/red]")
        import traceback
        console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")


#
# Command: Doc
#
@app.command()
def doc(
    ctx: typer.Context,
    title: str = typer.Option(None,  help="The title of the document"),
    toc:  bool = typer.Option(False, help="Whether to create a table of contents"),
) -> None:
    """
    Re-create the documentation and write it to the output file.

    This command generates documentation for the script, including an optional
    table of contents and custom title.
    """
    result = DocGenerator.generate_doc(__file__, title, toc)
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










