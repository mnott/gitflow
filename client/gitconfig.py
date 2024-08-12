"""
This module provides the GitConfig class for managing AI provider configurations using Git config.

The GitConfig class implements the ConfigProvider interface, using Git config
as the backend for storing and retrieving configuration data.
"""

import os
import subprocess
from typing import Optional, List, Dict
from rich.console import Console
from InquirerPy import inquirer
from .config_provider import ConfigProvider

console = Console()

class GitConfig(ConfigProvider):
    """
    A configuration provider that uses Git config for storage.

    This class implements the ConfigProvider interface, using Git config
    commands to store and retrieve configuration data for AI providers.
    """
    def __init__(self):
        self.git_dir = self._find_git_dir()

    def _find_git_dir(self):
        """Find the .git directory relative to the scocr.py file."""
        # Get the directory of the scocr.py file
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Traverse up the directory tree from the script location
        current_dir = script_dir
        while current_dir != '/':
            git_dir = os.path.join(current_dir, '.git')
            if os.path.exists(git_dir):
                return git_dir
            current_dir = os.path.dirname(current_dir)

        raise ValueError("No .git directory found in the parent directories of scocr.py")

    def _run_git_command(self, args):
        work_tree = os.path.dirname(self.git_dir)
        full_args = ["git", f"--git-dir={self.git_dir}", f"--work-tree={work_tree}"]
        full_args.extend(args)
        # print(" ".join(full_args))
        result = subprocess.run(full_args, capture_output=True, text=True)
        return result


    def get_metadata(self, key: str) -> Optional[str]:
        """
        Retrieve a metadata value from Git config.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[str]: The value associated with the key, or None if not found.
        """
        try:
            result = self._run_git_command(["config", "--get", key])
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None


    def set_metadata(self, key: str, value: str):
        """
        Set a metadata value in local Git config.

        Args:
            key   (str): The key to set.
            value (str): The value to associate with the key.
        """
        try:
            self._run_git_command(["config", key, value])
            console.print(f"[green]{key} saved successfully to local config.[/green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Failed to save {key} to local config: {e}[/red]")
            console.print(f"[red]Command attempted: git config --local {key} {value}[/red]")


    def get_available_providers(self) -> List[str]:
        """
        Get a list of available AI providers from Git config.

        Returns:
            List[str]: A list of provider names.
        """
        try:
            result = self._run_git_command(["config", "--get-regexp", "^[^.]+\\.aiprovider$"])
            providers = [line.split('.')[0] for line in result.stdout.splitlines() if line.endswith('true')]
            #print(f"Available providers: {providers}")  # Debug print
            return providers
        except subprocess.CalledProcessError as e:
            #print(f"Error getting available providers: {e}")  # Debug print
            if e.returncode == 1:
                # No matching configuration found, which is not an error
                return []
            raise  # Re-raise the exception for other error codes


    def create_provider(self, provider: str):
            """
            Create a new provider entry.

            Args:
                provider (str): The name of the new provider.
            """
            self.set_metadata(f"{provider}.aiprovider", "true")


    def get_provider_metadata(self, provider: str) -> Dict[str, str]:
        """
        Get all metadata for a specific provider from Git config.

        Args:
            provider (str): The name of the provider.

        Returns:
            Dict[str, str]: A dictionary of metadata key-value pairs.
        """
        metadata = {}
        keys = ['name', 'url', 'apikey', 'model', 'header', 'response']
        for key in keys:
            value = self.get_metadata(f"{provider}.{key}")
            if value:
                metadata[key] = value
        return metadata


    def set_provider_metadata(self, provider: str, metadata: Dict[str, str]):
        """
        Set all metadata for a specific provider in Git config.

        Args:
            provider            (str): The name of the provider.
            metadata (Dict[str, str]): A dictionary of metadata key-value pairs.
        """
        for key, value in metadata.items():
            self.set_metadata(f"{provider}.{key}", value)


    def delete_provider(self, provider: str):
        """
        Delete all metadata for a specific provider from Git config.

        Args:
            provider (str): The name of the provider to delete.
        """
        keys = ['aiprovider', 'name', 'url', 'apikey', 'model', 'header', 'response']
        for key in keys:
            try:
                self._run_git_command(["config", "--local", "--unset", f"{provider}.{key}"])
            except subprocess.CalledProcessError:
                pass  # Ignore if the key doesn't exist
        #console.print(f"[green]Provider {provider} deleted successfully.[/green]")


    def get_default_provider(self) -> Optional[str]:
        return self.get_metadata("ai.default")


    def set_default_provider(self, provider: str):
        if provider not in self.get_available_providers():
            raise ValueError(f"Provider '{provider}' not found in git config.")
        self.set_metadata("ai.default", provider)


    def select_provider(self, message: str = "Select an AI provider:") -> str:
        available_providers = self.get_available_providers()
        if not available_providers:
            raise ValueError("No AI providers found in git config.")

        provider_names = {p: self.get_metadata(f"{p}.name") for p in available_providers}
        choices = list(provider_names.values())

        selected_name = inquirer.select(
            message=message,
            choices=choices
        ).execute()

        return next(key for key, value in provider_names.items() if value == selected_name)


    def set_default_provider_interactive(self):
        provider = self.select_provider("Select an AI provider to set as default:")
        self.set_default_provider(provider)
        friendly_name = self.get_metadata(f"{provider}.name")
        console.print(f"[green]Default AI provider set to: {friendly_name} ({provider})[/green]")

