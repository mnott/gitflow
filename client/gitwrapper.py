from datetime import datetime
from git import Repo, GitCommandError
from InquirerPy import inquirer
from pathlib import Path
from rich.console import Console
from typing import Optional
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

    def get_repo_root(self):
        repo_root = Path(self.repo.git.rev_parse("--show-toplevel"))
        return repo_root

    def get_git_dir(self):
        return self.repo.git_dir

    def get_working_tree_dir(self):
        return self.repo.working_tree_dir

    # Get the current week number
    def get_week_number(self, week: Optional[int] = None) -> str:
        """Get the current week number in the format YYYY-WW."""
        if week is None:
            week = datetime.now().isocalendar()[1]
        return f"{datetime.now().year}-{week:02}"

    def get_branches(self):
        return self.repo.branches

    def check_network_connection(self):
        try:
            self.repo.git.ls_remote('--exit-code', '--quiet', 'origin')
            return True
        except GitCommandError:
            return False

    def push(self, remote='origin', branch='develop', *args, **kwargs):
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

    def determine_branch_name(self, name, branch_type, week):
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


    def push_to_remote(self, branch):
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


    def merge_base(self, base_branch, compare_branch):
        return self.repo.git.merge_base(base_branch, compare_branch)

    def merge_to_target(self, source, target):
        self.console.print(f"[blue]Merging {source} into {target}...[/blue]")
        try:
            self.repo.git.checkout(target)
            self.repo.git.merge(source, '--no-ff')
            new_branch = self.push('origin', target)
            if new_branch:
                self.console.print(f"[green]Pull request created to merge {source} into {target}[/green]")
            else:
                self.console.print(f"[green]Merged and pushed {source} into {target}[/green]")
            return True
        except GitCommandError as e:
            self.console.print(f"[red]Unexpected error merging {source} into {target}: {e}[/red]")
            return False

    def delete_branch(self, branch, delete_remote=True):
        try:
            current_branch = self.repo.active_branch.name
            if current_branch == branch:
                self.repo.git.checkout('develop')

            # Check if local branch exists before trying to delete it
            if branch in [b.name for b in self.repo.branches]:
                self.repo.git.branch('-D', branch)
                self.console.print(f"[green]Deleted local branch {branch}[/green]")
            else:
                pass
                # This error might just mean we've already deleted the branch
                # e.g. when multi selecting branches to delete
                # console.print(f"[yellow]Local branch {branch} not found. Skipping local deletion.[/yellow]")

            if delete_remote and self.check_network_connection():
                try:
                    self.repo.git.push('origin', '--delete', branch)
                    self.console.print(f"[green]Deleted remote branch {branch}[/green]")
                except GitCommandError as e:
                    if "remote ref does not exist" in str(e):
                        pass
                        # This error might just mean we've already deleted the branch
                        # e.g. when multi selecting branches to delete
                        # console.print(f"[yellow]Remote branch {branch} not found. Skipping remote deletion.[/yellow]")
                    else:
                        raise
        except GitCommandError as e:
            self.console.print(f"[yellow]Could not delete branch {branch}: {e}[/yellow]")

    def cleanup_temp_branches(self):
        for branch in self.temp_branches:
            self.delete_branch(branch, delete_remote=False)
        self.temp_branches = []

    def checkout(self, branch, start_point=None, create=False, force=False):
        # Check if the branch is actually "--"
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

    def create_tag(self, tag_name, message=None):
        self.repo.create_tag(tag_name, message=message)

    def pull(self, remote='origin', branch=None):
        if branch:
            self.repo.git.pull(remote, branch)
        else:
            self.repo.git.pull()

    def fetch(self, remote='origin', branch=None, all_remotes=False, prune=False):
        args = []
        if all_remotes:
            args.append('--all')
        if prune:
            args.append('--prune')
        if branch:
            self.repo.git.fetch(remote, branch, *args)
        else:
            self.repo.git.fetch(remote, *args)

    def add(self, *file_paths, all=False, force=False):
        args = []

        if all:
            args.append('--all')
        else:
            args.extend(file_paths)

        if force:
            args.append('--force')

        self.repo.git.add(*args)

    def commit(self, message):
        if message == "--no-edit":
            self.repo.git.commit('--no-edit')
        else:
            self.repo.git.commit('-m', message)

    def get_repo_heads(self):
            """
            Retrieves the list of all local branch heads.

            :return: A list of branch head objects.
            """
            return self.repo.heads

    def remote(self, command, *args):
            """
            Executes git remote commands.

            :param command: The remote subcommand to execute (e.g., 'prune', 'add', 'remove').
            :param args: Additional arguments for the subcommand.
            :return: The output of the git remote command, if any.
            """
            cmd_args = [command] + list(args)
            return self.repo.git.remote(*cmd_args)

    def stash(self, command='push', *args, message=None, include_untracked=False):
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

    def reset(self, mode='mixed', commit='HEAD'):
        self.repo.git.reset(mode, commit)

    def merge(self, branch=None, squash=False, no_ff=True, commit=True, abort=False):
        args = []

        if abort:
            args.append('--abort')
        else:
            if squash:
                args.append('--squash')
            if not commit:
                args.append('--no-commit')
            if no_ff:
                args.append('--no-ff')
            if branch:
                args.append(branch)

        self.repo.git.merge(*args)

    def abort_merge(self):
        self.repo.git.merge('--abort')

    def get_current_branch(self):
        return self.repo.active_branch.name

    def get_local_branches(self):
        local_branches = [head.name for head in self.repo.heads]
        return local_branches

    def get_remote_branches(self, remote='origin'):
        remote_branches = [ref.name for ref in self.repo.remote().refs if ref.name != 'origin/HEAD']
        return remote_branches

    def get_last_commit(self):
        return self.repo.head.commit

    def get_heads(self):
        return self.repo.heads

    def get_origin_refs(self):
        return self.repo.remotes.origin.refs

    def get_commits(self, start=None, end='HEAD', max_count=None, since=None):
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

    def get_index_diff(self, branch):
        return self.repo.index.diff(branch)

    def status(self, *args, **kwargs):
        return self.repo.git.status(*args, **kwargs)

    def get_remote_url(self, remote='origin'):
        return self.repo.remotes[remote].url

    def create_branch(self, branch_name):
        self.repo.git.branch(branch_name)

    def rename_branch(self, old_name, new_name):
        self.repo.git.branch('-m', old_name, new_name)

    def get_tags(self):
        return [tag.name for tag in self.repo.tags]

    def push_tag(self, tag_name):
        self.repo.git.push('origin', tag_name)

    def get_remotes(self):
        return [(remote.name, remote.url) for remote in self.repo.remotes]

    def get_remote_url(self, remote='origin'):
        return self.repo.remotes[remote].url

    def is_dirty(self, untracked_files=True):
        return self.repo.is_dirty(untracked_files=untracked_files)

    def get_untracked_files(self):
        return self.repo.untracked_files

    def get_modified_files(self):
        return [item.a_path for item in self.repo.index.diff(None)]

    def get_staged_files(self):
        return [item.a_path for item in self.repo.index.diff('HEAD')]

    def cherry_pick(self, commit):
        self.repo.git.cherry_pick(commit)

    def revert(self, commit):
        self.repo.git.revert(commit)



    def get_commit_author(self, commit='HEAD'):
        return self.repo.commit(commit).author.name

    def get_commit_date(self, commit='HEAD'):
        return self.repo.commit(commit).committed_datetime

    def rev_list(self, *args):
        return self.repo.git.rev_list(*args)


    #
    # Set some metadata in the .git/config file.
    #
    def set_git_metadata(self, key: str, value: str):
        try:
            subprocess.run(["git", "config", "--local", key, value], check=True)
            self.console.print(f"[green]{key} saved successfully.[/green]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Failed to save {key}: {e}[/red]")
