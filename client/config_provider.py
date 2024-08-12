"""
This module defines the ConfigProvider abstract base class.

The ConfigProvider class serves as a template for implementing
configuration management systems. It provides a standard interface
for storing, retrieving, and managing AI provider configurations.
"""

from abc import ABC, abstractmethod
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table
from typing import List, Dict, Optional

console = Console()

class ConfigProvider(ABC):
    """
    An abstract base class for configuration providers.

    This class defines the interface for configuration management systems.
    Concrete implementations should provide specific mechanisms for
    storing and retrieving configuration data.
    """

    @abstractmethod
    def get_metadata(self, key: str) -> Optional[str]:
        """
        Retrieve a metadata value for a given key.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[str]: The value associated with the key, or None if not found.
        """
        pass


    @abstractmethod
    def set_metadata(self, key: str, value: str):
        """
        Set a metadata value for a given key.

        Args:
            key (str): The key to set.
            value (str): The value to associate with the key.
        """
        pass


    @abstractmethod
    def get_available_providers(self) -> List[str]:
        """
        Get a list of available AI providers.

        Returns:
            List[str]: A list of provider names.
        """
        pass


    @abstractmethod
    def get_provider_metadata(self, provider: str) -> Dict[str, str]:
        """
        Get all metadata for a specific provider.

        Args:
            provider (str): The name of the provider.

        Returns:
            Dict[str, str]: A dictionary of metadata key-value pairs.
        """
        pass


    @abstractmethod
    def set_provider_metadata(self, provider: str, metadata: Dict[str, str]):
        """
        Set all metadata for a specific provider.

        Args:
            provider            (str): The name of the provider.
            metadata (Dict[str, str]): A dictionary of metadata key-value pairs.
        """
        pass


    @abstractmethod
    def delete_provider(self, provider: str):
        """
        Delete all metadata for a specific provider.

        Args:
            provider (str): The name of the provider to delete.
        """
        pass


    def create_provider(self, provider: str):
        """
        Create a new provider entry.

        Args:
            provider (str): The name of the new provider.
        """
        self.set_metadata(f"{provider}.aiprovider", "true")


    def provider_exists(self, provider: str) -> bool:
        """
        Check if a provider exists.

        Args:
            provider (str): The name of the provider to check.

        Returns:
            bool: True if the provider exists, False otherwise.
        """
        return provider in self.get_available_providers()


    def display_config(self, title: str, metadata: Dict[str, str]):
        """
        Display configuration in a formatted table.

        Args:
            title               (str): The title for the configuration display.
            metadata (Dict[str, str]): The configuration metadata to display.
        """
        table = Table(title=title)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="magenta")

        for key, value in metadata.items():
            if key == 'apikey':
                table.add_row(key, "[hidden]" if value else "[not set]")
            else:
                table.add_row(key, value if value else "[not set]")

        console.print(table)


    def clone_provider(self, source_provider: str, target_provider: str):
        """
        Clone an existing provider configuration to a new provider.

        Args:
            source_provider (str): The name of the provider to clone from.
            target_provider (str): The name of the new provider to create.

        Returns:
            bool: True if cloning was successful, False otherwise.
        """
        if not self.provider_exists(source_provider):
            console.print(f"[red]Source provider '{source_provider}' does not exist.[/red]")
            return False

        if self.provider_exists(target_provider):
            console.print(f"[red]Target provider '{target_provider}' already exists.[/red]")
            return False

        source_metadata = self.get_provider_metadata(source_provider)

        # Ask for a new friendly name
        new_friendly_name = inquirer.text(
            message=f"Enter a friendly name for the new provider '{target_provider}' (current: {source_metadata.get('name', 'Not set')}):"
        ).execute()

        if new_friendly_name:
            source_metadata['name'] = new_friendly_name

        self.create_provider(target_provider)
        self.set_provider_metadata(target_provider, source_metadata)
        console.print(f"[green]Provider '{source_provider}' cloned to '{target_provider}' successfully.[/green]")
        return True


    def configure_provider(self, provider: str):
        """
        Interactively configure a provider.

        This method guides the user through the process of creating,
        updating, or deleting a provider configuration.

        Args:
            provider (str): The name of the provider to configure.
        """
        if self.provider_exists(provider):
            action = inquirer.select(
                message=f"Provider '{provider}' already exists. What would you like to do?",
                choices=["Update", "Delete", "Clone", "Cancel"]
            ).execute()

            if action == "Delete":
                if inquirer.confirm(message=f"Are you sure you want to delete the provider '{provider}'?", default=False).execute():
                    self.delete_provider(provider)
                    console.print(f"[green]Provider '{provider}' has been deleted.[/green]")
                return
            elif action == "Clone":
                new_provider = inquirer.text(message="Enter the name for the cloned provider:").execute()
                if self.clone_provider(provider, new_provider):
                    provider = new_provider  # Continue configuring the new cloned provider
                else:
                    return
            elif action == "Cancel":
                console.print("[yellow]Operation cancelled.[/yellow]")
                return
        else:
            if inquirer.confirm(message=f"Provider '{provider}' does not exist. Do you want to create it?", default=True).execute():
                self.create_provider(provider)
            else:
                console.print("[yellow]Operation cancelled.[/yellow]")
                return

        existing_metadata = self.get_provider_metadata(provider)

        # Display current configuration
        if existing_metadata:
            self.display_config(f"Current Configuration for {provider}", existing_metadata)

        new_metadata = {}

        # Helper function to update or prompt for a value
        def update_value(key, prompt_message):
            existing_value = existing_metadata.get(key, '')
            if key == 'apikey':
                prompt = f"{prompt_message} [current: {'[hidden]' if existing_value else '[not set]'}]"
            else:
                prompt = f"{prompt_message} [current: {existing_value or '[not set]'}]"

            new_value = inquirer.text(message=prompt).execute()
            return existing_value if new_value == '' else new_value

        new_metadata['name']     = update_value('name', f"Enter a friendly name for {provider}:")
        new_metadata['apikey']   = update_value('apikey', f"Enter the API key for {provider}:")
        new_metadata['model']    = update_value('model', f"Enter the default model for {provider}:")
        new_metadata['url']      = update_value('url', f"Enter the API URL for {provider}:")
        new_metadata['header']   = update_value('header', f"Enter the header template for {provider}:")
        new_metadata['response'] = update_value('response', f"Enter the response template for {provider}:")

        # Display new configuration
        self.display_config("New configuration", new_metadata)

        if inquirer.confirm(message="Do you want to save these changes?", default=True).execute():
            self.set_provider_metadata(provider, new_metadata)
            console.print(f"[green]Provider {provider} configured successfully.[/green]")
        else:
            console.print("[yellow]Configuration cancelled. No changes were saved.[/yellow]")



