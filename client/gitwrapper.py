from datetime import datetime
from git import Repo, GitCommandError
from InquirerPy import inquirer
from pathlib import Path
from rich.console import Console
from typing import Optional, Dict, List
import subprocess
import sys
import json

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

    def delete_branch(self, branch_name: str, delete_remote: bool = False, delete_local: bool = True, quiet: bool = False) -> None:
        """Delete a branch locally and/or remotely."""
        try:
            # Strip any "Local: " or "Remote: " prefix if present, but don't require it
            if branch_name.startswith("Local: "):
                branch_name = branch_name[7:]
            elif branch_name.startswith("Remote: "):
                branch_name = branch_name[8:]

            # Check if we're on the branch we're trying to delete
            current_branch = self.get_current_branch()
            if current_branch == branch_name:
                # Switch to a safe branch first
                if 'develop' in self.repo.heads:
                    self.repo.heads.develop.checkout()
                else:
                    self.repo.heads.main.checkout()
                if not quiet:
                    self.console.print(f"Switched to {self.get_current_branch()} before deleting {branch_name}")

            if delete_local:
                # Check if local branch exists before trying to delete
                if branch_name in [h.name for h in self.repo.heads]:
                    # Get branch status first
                    status = self.get_branch_status(branch_name)
                    if not quiet:
                        self.console.print(f"Branch status for {branch_name}:")
                        self.console.print(f"  Last commit: {status['last_commit']} - {status['last_commit_msg']}")
                        if status['has_upstream']:
                            self.console.print(f"  Ahead by {status['ahead_count']}, behind by {status['behind_count']} commits")
                        else:
                            self.console.print("  No upstream branch found")

                    try:
                        self.repo.delete_head(branch_name)
                    except GitCommandError as e:
                        if "not fully merged" in str(e):
                            if not quiet:
                                self.console.print("[yellow]Branch has unmerged changes. Use -f to force delete.[/yellow]")
                            # Try force delete
                            self.repo.git.branch('-D', branch_name)
                        else:
                            raise
                    if not quiet:
                        self.console.print(f"Deleted local branch {branch_name}")
                elif not quiet:
                    self.console.print(f"Local branch {branch_name} does not exist")

            if delete_remote:
                try:
                    self.repo.git.push('origin', '--delete', branch_name)
                    if not quiet:
                        self.console.print(f"Deleted remote branch {branch_name}")
                except GitCommandError as e:
                    if "remote ref does not exist" in str(e):
                        if not quiet:
                            self.console.print(f"Remote branch {branch_name} does not exist")
                    else:
                        raise

        except GitCommandError as e:
            if not quiet:
                self.console.print(f"Error deleting branch {branch_name}: {e}")
            raise

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

            # Don't delete the branch here - let the calling code handle deletion
            # after all merges are complete

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

    def list_worktrees(self) -> str:
        """List all worktrees in the repository.

        Returns a formatted string with worktree information.
        The main worktree is marked with '[main-worktree]' in the output.
        """
        try:
            # Get the porcelain output first to identify the main worktree
            porcelain_output = self.repo.git.worktree('list', '--porcelain')
            worktrees = []
            current_worktree = {}

            # Parse porcelain output to identify main worktree
            for line in porcelain_output.split('\n'):
                if line.startswith('worktree '):
                    if current_worktree:
                        worktrees.append(current_worktree)
                    current_worktree = {'path': line.split(' ', 1)[1]}
                elif line.startswith('bare'):
                    current_worktree['bare'] = True
                elif line.startswith('HEAD '):
                    current_worktree['head'] = line.split(' ', 1)[1]
                elif line.startswith('branch '):
                    current_worktree['branch'] = line.split('refs/heads/', 1)[1]
                elif line == '':
                    if current_worktree:
                        worktrees.append(current_worktree)
                        current_worktree = {}

            if current_worktree:
                worktrees.append(current_worktree)

            # The first worktree is always the main one
            main_worktree_path = worktrees[0]['path'] if worktrees else None

            # Now get the normal output and add the main-worktree marker
            output = []
            normal_list = self.repo.git.worktree('list')
            for line in normal_list.split('\n'):
                if line.strip():
                    parts = line.split()
                    path = parts[0]
                    if path == main_worktree_path:
                        line += ' [main-worktree]'
                    output.append(line)

            return '\n'.join(output)
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
                    # Convert path to use system-specific separators and normalize
                    current_worktree = str(Path(line.split(' ', 1)[1]).resolve())
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

    def get_branch_status(self, branch_name: str) -> dict:
        """Get detailed status of a branch compared to its upstream.

        Args:
            branch_name (str): Name of the branch to check

        Returns:
            dict: Status information including:
                - has_upstream: bool
                - ahead_count: int
                - behind_count: int
                - upstream_name: str or None
                - last_commit: str
                - last_commit_msg: str
        """
        try:
            branch = self.repo.heads[branch_name]
            status = {
                'has_upstream': False,
                'ahead_count': 0,
                'behind_count': 0,
                'upstream_name': None,
                'last_commit': str(branch.commit)[:8],
                'last_commit_msg': branch.commit.message.strip()
            }

            # Get upstream info if it exists
            try:
                upstream = branch.tracking_branch()
                if upstream:
                    status['has_upstream'] = True
                    status['upstream_name'] = upstream.name
                    ahead, behind = self.repo.git.rev_list('--left-right', '--count',
                        f'{upstream.name}...{branch_name}').split()
                    status['ahead_count'] = int(ahead)
                    status['behind_count'] = int(behind)
            except GitCommandError:
                pass

            return status

        except (IndexError, GitCommandError) as e:
            self.console.print(f"[red]Error getting branch status: {e}[/red]")
            raise

    def is_directory(self, path_spec: str) -> bool:
        """Check if a path in a specific revision is a directory."""
        try:
            # Use git ls-tree to check if it's a directory
            output = self.repo.git.ls_tree(path_spec.split(':')[0], path_spec.split(':')[1])
            return output.strip().startswith('040000')
        except GitCommandError:
            return False

    def get_tracked_files(self, branch: str, directory: str) -> List[str]:
        """Get list of tracked files in a directory on a branch."""
        try:
            # Use git ls-tree -r to recursively list tracked files
            output = self.repo.git.ls_tree('-r', '--name-only', branch, directory)
            return [f for f in output.split('\n') if f.strip()]
        except GitCommandError:
            return []

    def show(self, path_spec: str) -> str:
        """Show file/directory contents at a specific revision."""
        return self.repo.git.show(path_spec)

    def has_uncommitted_changes(self, path: str) -> bool:
        """Check if a file or directory has uncommitted changes.

        Args:
            path: File or directory path to check

        Returns:
            bool: True if there are uncommitted changes, False otherwise
        """
        try:
            # Use git status --porcelain to get a machine-readable status
            status = self.repo.git.status('--porcelain', path)
            return bool(status.strip())
        except GitCommandError:
            return False

    def get_file_hash(self, path_spec: str) -> str:
        """Get the hash of a file in a specific revision.

        Args:
            path_spec: Path spec like "branch:path/to/file"

        Returns:
            The Git hash of the file
        """
        try:
            # Use git ls-tree to get the file's hash
            output = self.repo.git.ls_tree('-r', path_spec.split(':')[0], path_spec.split(':')[1])
            if output.strip():
                # Output format: <mode> blob <hash>\t<path>
                return output.split()[2]
            return ""
        except GitCommandError:
            return ""

    # -----------------------------------
    # Issue and Label Operations
    # -----------------------------------

    def list_issues_by_label(self, labels: List[str], state: str = "open") -> List[dict]:
        """List issues with specified labels.

        Args:
            labels (List[str]): List of label names to filter by
            state (str): Issue state ('open', 'closed', or 'all')

        Returns:
            List[dict]: List of issues matching the criteria
        """
        try:
            cmd = ["gh", "issue", "list",
                  "--json", "number,title,labels,state,url",
                  "--state", state]

            for label in labels:
                cmd.extend(["--label", label])

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error listing issues: {e.stderr}[/red]")
            raise

    def get_repo_labels(self) -> List[dict]:
        """Get all labels defined in the repository.

        Returns:
            List[dict]: List of label objects with name, color, and description
        """
        try:
            result = subprocess.run(
                ["gh", "label", "list", "--json", "name,color,description"],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error getting labels: {e.stderr}[/red]")
            raise

    def create_label(self, name: str, color: str, description: str = "") -> None:
        """Create a new label in the repository.

        Args:
            name (str): Label name
            color (str): Color in hex format (e.g., 'ff0000')
            description (str, optional): Label description
        """
        try:
            cmd = ["gh", "label", "create", name,
                  "--color", color.lstrip('#')]
            if description:
                cmd.extend(["--description", description])

            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.console.print(f"[green]Created label '{name}'[/green]")
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr:
                self.console.print(f"[yellow]Label '{name}' already exists[/yellow]")
            else:
                self.console.print(f"[red]Error creating label: {e.stderr}[/red]")
                raise

    def add_labels_to_issue(self, issue_number: int, labels: List[str]) -> None:
        """Add labels to an issue.

        Args:
            issue_number (int): Issue number
            labels (List[str]): Labels to add
        """
        try:
            cmd = ["gh", "issue", "edit", str(issue_number)]
            for label in labels:
                cmd.extend(["--add-label", label])

            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.console.print(f"[green]Added labels to issue #{issue_number}[/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error adding labels: {e.stderr}[/red]")
            raise

    def remove_labels_from_issue(self, issue_number: int, labels: List[str]) -> None:
        """Remove labels from an issue.

        Args:
            issue_number (int): Issue number
            labels (List[str]): Labels to remove
        """
        try:
            cmd = ["gh", "issue", "edit", str(issue_number)]
            for label in labels:
                cmd.extend(["--remove-label", label])

            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.console.print(f"[green]Removed labels from issue #{issue_number}[/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error removing labels: {e.stderr}[/red]")
            raise
