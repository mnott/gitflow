from datetime import datetime
from git import Repo, GitCommandError
from InquirerPy import inquirer
from pathlib import Path
from rich.console import Console
from typing import Optional, Dict
import subprocess
import sys

class GitWrapper:
    def __init__(self):
        path = Path.cwd()
        self.repo = Repo(path, search_parent_directories=True)
        self.console = Console()

        if self.repo is None:
            self.console.print("[red]Error: Not in a valid Git repository[/red]")
            sys.exit(1)
        self.temp_branches = []

    # -----------------------------------
    # Repository Information and Metadata
    # -----------------------------------

    def get_repo_root(self):
        """Get the root directory of the current Git repository."""
        repo_root = Path(self.repo.git.rev_parse("--show-toplevel"))
        return repo_root

    def get_git_dir(self):
        """Get the .git directory path."""
        return self.repo.git_dir

    def get_working_tree_dir(self):
        """Get the working tree directory of the repository."""
        return self.repo.working_tree_dir

    def get_heads(self):
        return self.repo.heads

    def get_repo_heads(self):
        """Retrieves the list of all local branch heads."""
        return self.repo.heads

    def get_current_branch(self):
        """Get the name of the currently active branch."""
        return self.repo.active_branch.name

    def get_branches(self):
        """Get a list of all branches in the repository."""
        return self.repo.branches

    def get_local_branches(self):
        """Get a list of all local branches."""
        return [head.name for head in self.repo.heads]

    def get_remote_branches(self, remote='origin'):
        """Get a list of all branches from the specified remote."""
        return [ref.name for ref in self.repo.remote().refs if ref.name != 'origin/HEAD']

    def get_remotes(self):
        """Get a list of all remotes with their names and URLs."""
        return [(remote.name, remote.url) for remote in self.repo.remotes]

    def get_remote_url(self, remote='origin'):
        """Get the URL of the specified remote."""
        return self.repo.remotes[remote].url

    # -----------------------------------
    # Git Metadata Management
    # -----------------------------------

    def get_git_metadata(self, key: str) -> Optional[str]:
        """Get a specific configuration value from the .git/config file."""
        try:
            value = subprocess.check_output(["git", "config", "--get", key], universal_newlines=True).strip()
            return value
        except subprocess.CalledProcessError:
            return None

    def set_git_metadata(self, key: str, value: str):
        """Set a specific configuration value in the .git/config file."""
        try:
            subprocess.run(["git", "config", "--local", key, value], check=True)
            self.console.print(f"[green]{key} saved successfully.[/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Failed to save {key}: {e}[/red]")

    # -----------------------------------
    # Commit and Tag Operations
    # -----------------------------------

    def get_last_commit(self):
        """Get the last commit in the current branch."""
        return self.repo.head.commit

    def get_commit_author(self, commit='HEAD'):
        """Get the author of a specific commit."""
        return self.repo.commit(commit).author.name

    def get_commit_date(self, commit='HEAD'):
        """Get the date of a specific commit."""
        return self.repo.commit(commit).committed_datetime

    def commit(self, message):
        """Commit changes with the specified message."""
        if message == "--no-edit":
            self.repo.git.commit('--no-edit')
        else:
            self.repo.git.commit('-m', message)

    def create_tag(self, tag_name, message=None):
        """Create a tag with an optional message."""
        self.repo.create_tag(tag_name, message=message)

    def get_tags(self):
        """Get a list of all tags in the repository."""
        return [tag.name for tag in self.repo.tags]

    def push_tag(self, tag_name):
        """Push a tag to the remote repository."""
        self.repo.git.push('origin', tag_name)

    # -----------------------------------
    # Branch Operations
    # -----------------------------------

    def create_branch(self, branch_name):
        """Create a new branch from current HEAD."""
        try:
            self.repo.git.branch(branch_name)
        except GitCommandError as e:
            raise GitCommandError(f"Failed to create branch: {e}")

    def rename_branch(self, old_name, new_name):
        """Rename an existing branch."""
        self.repo.git.branch('-m', old_name, new_name)

    def delete_branch(self, branch, delete_remote=True, delete_local=True):
        """Delete a branch locally and/or remotely.

        Args:
            branch (str): Name of the branch to delete
            delete_remote (bool): Whether to delete the remote branch
            delete_local (bool): Whether to delete the local branch
        """
        try:
            # Check what actually exists before announcing actions
            local_exists = branch in [b.name for b in self.repo.branches]
            remote_exists = False
            if self.check_network_connection():
                try:
                    self.repo.git.ls_remote('--exit-code', 'origin', f'refs/heads/{branch}')
                    remote_exists = True
                except GitCommandError:
                    pass

            # Print what we're actually going to do
            actions = []
            if delete_remote and remote_exists:
                actions.append("remote")
            if delete_local and local_exists:
                actions.append("local")
            if actions:
                self.console.print(f"[blue]Deleting {' and '.join(actions)} branch{'es' if len(actions) > 1 else ''} '{branch}'...[/blue]")

            # Handle remote deletion
            if delete_remote and self.check_network_connection():
                try:
                    self.repo.git.push('origin', '--delete', branch)
                    self.console.print(f"[green]Deleted remote branch {branch}[/green]")
                except GitCommandError as e:
                    if "remote ref does not exist" in str(e):
                        pass
                    else:
                        raise

            # Handle local deletion
            if delete_local and local_exists:
                # Only switch to develop if we're deleting the current branch locally
                current_branch = self.repo.active_branch.name
                if current_branch == branch:
                    self.repo.git.checkout('develop')

                self.repo.git.branch('-D', branch)
                self.console.print(f"[green]Deleted local branch {branch}[/green]")

        except GitCommandError as e:
            self.console.print(f"[yellow]Could not delete branch {branch}: {e}[/yellow]")

    def checkout(self, branch, start_point=None, create=False, force=False):
        """Checkout a branch, optionally creating it or forcing the operation."""
        args = []

        if branch == "--":
            args.append('--')
            args.append(start_point)
        else:
            if create:
                args.extend(['-b', branch])
            else:
                args.append(branch)

            if start_point:
                args.append(start_point)

        # Prepare keyword arguments
        kwargs = {}

        if force:
            kwargs['force'] = True

        # Execute the git checkout command
        self.repo.git.checkout(*args, **kwargs)

    def determine_branch_name(self, name, branch_type, week):
        """Determine the full branch name based on the type and name."""
        if name and branch_type != "release":
            return f"{branch_type}/{name}" if branch_type != "local" else name
        elif branch_type == "hotfix":
            week_number = self.get_week_number(week)
            return f"hotfix/week-{week_number}"
        elif branch_type == "release" and name:
            return f"release/{name}"
        else:
            self.console.print("[red]Error: Invalid branch configuration[/red]")
            return None

    def set_branch_comment(self, branch: str, comment: str):
        """Set a comment for a specific branch.

        Args:
            branch  (str): The name of the branch to comment on
            comment (str): The comment to associate with the branch
        """
        config_key = f"branch.{branch}.comment"
        try:
            self.repo.git.config('--local', config_key, comment)
            self.console.print(f"[green]Comment saved for branch '{branch}'[/green]")
        except GitCommandError as e:
            self.console.print(f"[red]Failed to save comment for branch '{branch}': {e}[/red]")

    def get_branch_comment(self, branch: str) -> Optional[str]:
        """Get the comment associated with a specific branch.

        Args:
            branch (str): The name of the branch to get the comment for

        Returns:
            Optional[str]: The comment if it exists, None otherwise
        """
        config_key = f"branch.{branch}.comment"
        try:
            return self.repo.git.config('--get', config_key)
        except GitCommandError:
            return None

    def get_all_branch_comments(self) -> Dict[str, str]:
        """Get all branch comments.

        Returns:
            Dict[str, str]: A dictionary mapping branch names to their comments
        """
        try:
            # Get all branch.*.comment configurations
            config_output = self.repo.git.config('--get-regexp', r'^branch\..*\.comment$')
            comments = {}
            for line in config_output.splitlines():
                key, comment = line.split(' ', 1)
                branch = key.split('.')[1]  # Extract branch name from branch.<name>.comment
                comments[branch] = comment
            return comments
        except GitCommandError:
            return {}

    # -----------------------------------
    # Add, Pull, Push, Fetch, and Remote Operations
    # -----------------------------------

    def add(self, *file_paths, all=False, force=False):
        args = []

        if all:
            args.append('--all')
        else:
            args.extend(file_paths)

        if force:
            args.append('--force')

        self.repo.git.add(*args)

    def push(self, remote='origin', branch='develop', *args, **kwargs):
        """Push changes to the specified remote and branch, with fallback for protected branches."""
        offline = not self.check_network_connection()
        new_branch_name = None

        try:
            self.repo.git.push(remote, branch, *args, **kwargs)
            return None  # No new branch created
        except (GitCommandError, subprocess.CalledProcessError) as e:
            if "protected branch" in str(e):
                self.console.print(f"[yellow]Protected branch {branch} detected. Creating a new branch for pull request.[/yellow]")
                new_branch_name = f"update-{branch}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.repo.git.checkout('-b', new_branch_name)
                if not offline:
                    self.repo.git.push('origin', new_branch_name)
                    result = subprocess.run(
                        ["gh", "pr", "create", "--base", branch, "--head", new_branch_name,
                            "--title", f"Update {branch}", "--body", "Automated pull request from script"],
                        capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        self.console.print(f"[green]Created pull request to merge changes from {new_branch_name} into {branch}[/green]")
                        self.temp_branches.append(new_branch_name)
                    else:
                        self.console.print(f"[red]Error creating pull request: {result.stderr}[/red]")
                else:
                    self.console.print("[yellow]No network connection. New branch created locally. Push and create PR when online.[/yellow]")
                    self.temp_branches.append(new_branch_name)

                self.repo.git.checkout(branch)
            else:
                self.console.print(f"[red]Error: {e}[/red]")
                raise e

        return new_branch_name

    def push_to_remote(self, branch):
        """Push changes to the remote repository, with offline mode handling."""
        offline = not self.check_network_connection()
        if offline:
            self.console.print("[yellow]Offline mode. Changes will be pushed when online.[/yellow]")
            return True

        try:
            self.push('origin', branch)
            self.console.print(f"[green]Pushed changes to {branch}[/green]")
            return True
        except GitCommandError as e:
            if "up-to-date" in str(e):
                return False
            self.console.print(f"[red]Error pushing to remote: {e}[/red]")
            return False

    def pull(self, remote='origin', branch=None, rebase=False):
        """
        Pull changes from a remote repository.

        :param remote: The remote to pull from (default: 'origin')
        :param branch: The branch to pull (default: current branch)
        :param rebase: Whether to rebase the current branch on top of the upstream branch after fetching
        :return: The output of the pull command.
        """
        pull_args = ['git', 'pull', remote]
        if branch:
            pull_args.append(branch)
        if rebase:
            pull_args.insert(2, '--rebase')

        try:
            return self.repo.git.execute(pull_args)
        except GitCommandError as e:
            self.console.print(f"[red]Error: {e}[/red]")
            raise e

    def fetch(self, remote='origin', branch=None, all_remotes=False, prune=False):
        """Fetch updates from the remote repository."""
        args = []
        if all_remotes:
            args.append('--all')
        if prune:
            args.append('--prune')
        if branch:
            self.repo.git.fetch(remote, branch, *args)
        else:
            self.repo.git.fetch(remote, *args)

    def remote(self, command, *args):
        """Execute git remote commands like 'prune', 'add', or 'remove'."""
        cmd_args = [command] + list(args)
        return self.repo.git.remote(*cmd_args)


    # -----------------------------------
    # Merge, Rebase, and Reset Operations
    # -----------------------------------

    def merge(self, branch=None, squash=False, no_ff=True, ff_only=False, commit=True, abort=False):
        """Merge a branch into the current branch with various options."""
        args = []

        if abort:
            args.append('--abort')
        else:
            if squash:
                args.append('--squash')
            if not commit:
                args.append('--no-commit')
            if ff_only:
                args.append('--ff-only')
            elif no_ff:
                args.append('--no-ff')
            if branch:
                args.append(branch)

        self.repo.git.merge(*args)

    def merge_base(self, base_branch, compare_branch):
        """Find the common ancestor of two branches."""
        return self.repo.git.merge_base(base_branch, compare_branch)

    def merge_to_target(self, source, target, no_ff=True):
        """Merge the source branch into the target branch and push the changes."""
        self.console.print(f"[blue]Merging {source} into {target}...[/blue]")
        try:
            self.repo.git.checkout(target)
            merge_args = [source]
            if no_ff:
                merge_args.append('--no-ff')
            self.repo.git.merge(*merge_args)
            new_branch = self.push('origin', target)
            if new_branch:
                self.console.print(f"[green]Pull request created to merge {source} into {target}[/green]")
            else:
                self.console.print(f"[green]Merged and pushed {source} into {target}[/green]")
            return True
        except GitCommandError as e:
            self.console.print(f"[red]Unexpected error merging {source} into {target}: {e}[/red]")
            return False

    def reset(self, mode='mixed', commit='HEAD'):
        """Reset the current HEAD to the specified state."""
        self.repo.git.reset(mode, commit)

    def abort_merge(self):
        """Abort the current merge process."""
        self.repo.git.merge('--abort')

    def rebase(self, upstream, branch=None):
        """Rebase the current branch onto the specified upstream branch."""
        args = ['rebase', upstream]
        if branch:
            args.append(branch)
        self.repo.git.execute(args)


    # -----------------------------------
    # Stashing Operations
    # -----------------------------------

    def stash(self, command='push', *args, message=None, include_untracked=False):
        """Stash changes with options for message and including untracked files."""
        cmd_args = [command]

        if command in ['push', 'save']:
            if include_untracked:
                cmd_args.append('--include-untracked')
            if message:
                cmd_args.extend(['-m', message])

        cmd_args.extend(args)  # Add any additional arguments

        if command in ['list', 'show']:
            return self.repo.git.stash(*cmd_args)
        else:
            self.repo.git.stash(*cmd_args)

    def get_stashed_changes(self):
        """Get a list of stashed changes."""
        return self.repo.git.stash('list')

    # -----------------------------------
    # Status and Diff Operations
    # -----------------------------------

    def status(self, *args, **kwargs):
        """Get the status of the working directory."""
        return self.repo.git.status(*args, **kwargs)

    def get_diff(self, start=None, end=None):
        """Get the diff between two commits or for the working directory."""
        if start is None:
            # Get diff of unstaged changes
            return self.repo.git.diff()
        elif end is None:
            if '..' in start:
                # Handle the case where the range is passed as a single argument
                return self.repo.git.diff(start)
            else:
                # Handle the case where only one argument is provided (e.g., '--cached')
                return self.repo.git.diff(start)
        else:
            return self.repo.git.diff(start, end)

    def is_dirty(self, untracked_files=True):
        """Check if the working directory has uncommitted changes."""
        return self.repo.is_dirty(untracked_files=untracked_files)

    def get_untracked_files(self):
        """Get a list of untracked files."""
        return self.repo.untracked_files

    def get_modified_files(self):
        """Get a list of modified but unstaged files."""
        return [item.a_path for item in self.repo.index.diff(None)]

    def get_staged_files(self):
        """Get a list of files that are staged for commit."""
        return [item.a_path for item in self.repo.index.diff('HEAD')]

    def get_commits(self, start=None, end='HEAD', max_count=None, since=None):
        """Get a list of commits in the specified range."""
        args = []
        if max_count:
            args.extend(['-n', str(max_count)])
        if since:
            args.extend(['--since', since])
        if start:
            args.append(f"{start}..{end}")
        else:
            args.append(end)
        return list(self.repo.iter_commits(*args))

    def get_diff(self, start=None, end=None):
        """Get the diff between two commits or the current working directory."""
        if start is None:
            return self.repo.git.diff()
        elif end is None:
            if '..' in start:
                return self.repo.git.diff(start)
            else:
                return self.repo.git.diff(start)
        else:
            return self.repo.git.diff(start, end)

    def get_index_diff(self, branch):
        """Get the diff between the index and the specified branch."""
        return self.repo.index.diff(branch)

    def rev_parse(self, rev):
        """Return the SHA-1 hash of the given revision."""
        try:
            return self.repo.git.rev_parse(rev).strip()
        except GitCommandError as e:
            self.console.print(f"[red]Error: {e}[/red]")
            return None

    def rev_list(self, *args):
        """List commit objects in reverse chronological order."""
        return self.repo.git.rev_list(*args)

    # -----------------------------------
    # Cleanup Operations
    # -----------------------------------

    def cleanup_temp_branches(self):
        """Cleanup temporary branches created during operations."""
        for branch in self.temp_branches:
            self.delete_branch(branch, delete_remote=False)
        self.temp_branches = []

    # -----------------------------------
    # Utility Methods
    # -----------------------------------

    def check_network_connection(self):
        """Check if there is a network connection by trying to reach the remote."""
        try:
            self.repo.git.ls_remote('--exit-code', '--quiet', 'origin')
            return True
        except GitCommandError:
            return False

    def get_week_number(self, week: Optional[int] = None) -> str:
        """Get the current week number in the format YYYY-WW."""
        if week is None:
            week = datetime.now().isocalendar()[1]
        return f"{datetime.now().year}-{week:02}"

    def get_origin_refs(self):
        """Get references to all branches and tags from the origin remote."""
        return self.repo.remotes.origin.refs

    def cherry_pick(self, commit):
        """Cherry-pick a specific commit onto the current branch."""
        self.repo.git.cherry_pick(commit)

    def revert(self, commit):
        """Revert a specific commit."""
        self.repo.git.revert(commit)

    def execute_git_command(self, cmd):
        """Execute a git command and return its output."""
        try:
            return self.repo.git.execute(['git'] + cmd)
        except GitCommandError as e:
            raise GitCommandError(f"Git command failed: {e}")

    def log(self, *args):
        """Execute git log command with the given arguments and return the output."""
        try:
            return self.repo.git.log(*args)
        except GitCommandError as e:
            self.console.print(f"[red]Error executing git log: {e}[/red]")
            raise

    def show(self, *args):
        """Show various git objects (commits, files at specific revisions, etc).

        Args:
            *args: Variable arguments to pass to git show command

        Returns:
            The output of the git show command as a string

        Example:
            show('HEAD:file.txt') - Shows contents of file.txt at HEAD
            show('abc123') - Shows commit abc123
        """
        try:
            return self.repo.git.show(*args)
        except GitCommandError as e:
            self.console.print(f"[red]Error executing git show: {e}[/red]")
            raise

    # -----------------------------------
    # Worktree Operations
    # -----------------------------------

    def list_worktrees(self):
        """List all worktrees in the repository."""
        try:
            return self.repo.git.worktree('list')
        except GitCommandError as e:
            self.console.print(f"[red]Error listing worktrees: {e}[/red]")
            raise

    def add_worktree(self, path, branch=None, new_branch=None):
        """Add a new worktree.

        Args:
            path (str): Path where to create the worktree
            branch (str, optional): Existing branch to checkout
            new_branch (str, optional): Create and checkout new branch
        """
        args = []
        if new_branch:
            args.extend(['-b', new_branch])
        args.append(path)
        if branch:
            args.append(branch)

        try:
            return self.repo.git.worktree('add', *args)
        except GitCommandError as e:
            self.console.print(f"[red]Error adding worktree: {e}[/red]")
            raise

    def remove_worktree(self, path, force=False):
        """Remove a worktree.

        Args:
            path (str): Path of the worktree to remove
            force (bool): Force removal even with uncommitted changes
        """
        args = ['remove']
        if force:
            args.append('--force')
        args.append(path)

        try:
            return self.repo.git.worktree(*args)
        except GitCommandError as e:
            self.console.print(f"[red]Error removing worktree: {e}[/red]")
            raise

    def is_worktree(self, branch):
        """Check if a branch is currently used in a worktree.

        Args:
            branch (str): Branch name to check

        Returns:
            tuple: (bool, str) - (is_worktree, worktree_path) or (False, None)
        """
        try:
            worktree_list = self.repo.git.worktree('list', '--porcelain').split('\n')
            current_worktree = None
            current_branch = None

            for line in worktree_list:
                if line.startswith('worktree '):
                    current_worktree = line.split(' ', 1)[1]
                elif line.startswith('branch '):
                    current_branch = line.split('refs/heads/', 1)[1]
                    if current_branch == branch:
                        return True, current_worktree
                elif line == '':
                    current_worktree = None
                    current_branch = None

            return False, None
        except GitCommandError:
            return False, None

    def prune_refs(self):
        """Update branch list by pruning stale refs."""
        try:
            self.repo.git.fetch('--prune')  # Prune remote branches
            self.repo.git.remote('prune', 'origin')  # Prune remote tracking branches
            self.repo.git.gc('--prune=now')  # Clean up any loose objects
        except GitCommandError as e:
            raise GitCommandError(f"Failed to prune refs: {e}")
