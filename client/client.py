"""
This module provides the AIClient class for interacting with various AI providers.

The AIClient class allows users to configure and use different AI providers
(such as OpenAI or Claude) through a unified interface. It handles provider
selection, configuration management, and API interactions.
"""

from InquirerPy import inquirer
from rich.console import Console
from typing import Optional, Dict
import re
import requests
import sys
from .gitconfig import GitConfig
from .gitwrapper import GitWrapper

console = Console()

class AIClient:
    """
    A client for interacting with various AI providers.

    This class manages the configuration and interaction with different AI providers.
    It allows for dynamic provider selection, configuration loading, and API requests.

    Attributes:
        config_provider       (GitConfig): The configuration provider used to store and retrieve settings.
        available_providers   (List[str]): A list of available AI providers.
        provider_names   (Dict[str, str]): A mapping of provider keys to their friendly names.
        name_to_provider (Dict[str, str]): A mapping of friendly names to provider keys.
        ai                          (str): The currently selected AI provider.
        name                        (str): The friendly name of the current provider.
        url                         (str): The API URL for the current provider.
        api_key                     (str): The API key for the current provider.
        model                       (str): The default model for the current provider.
        header_template             (str): The header template for API requests.
        response_template           (str): The response template for parsing API responses.
    """

    def __init__(self, ai: Optional[str] = None, config_provider: Optional[GitConfig] = None):
        """
        Initialize the AIClient with a specified provider and configuration.

        Args:
            ai                    (str): The AI provider to use. If None or invalid, user will be prompted to select.
            config_provider (GitConfig): The configuration provider to use for storing/retrieving settings.
        """
        self.config_provider = config_provider or GitConfig()
        self.available_providers = self.config_provider.get_available_providers()

        if not self.available_providers:
            console.print("[yellow]No AI providers found in git config. Let's create one.[/yellow]")
            self.create_new_provider()
            return

        self.provider_names = {p: self.config_provider.get_metadata(f"{p}.name") for p in self.available_providers}
        self.name_to_provider = {v: k for k, v in self.provider_names.items()}

        if ai is None:
            ai = self.config_provider.get_default_provider()

        if ai is None or (ai not in self.available_providers and ai not in self.name_to_provider):
            if ai:
                console.print(f"[yellow]Provider '{ai}' not found in git config.[/yellow]")

            selected_name = self.config_provider.select_provider(
                message="Select an AI provider or set a default:",
                choices=list(self.provider_names.values()) + ["Set new default"]
            )

            if selected_name == "Set new default":
                self.ai = self.config_provider.set_default_provider_interactive()
            else:
                self.ai = self.name_to_provider[selected_name]
        else:
            self.ai = ai if ai in self.available_providers else self.name_to_provider[ai]

        self.load_provider_metadata()


    def get_current_provider_name(self) -> str:
        """
        Get the name of the currently selected AI provider.

        Returns:
            str: The friendly name of the current AI provider.
        """
        return self.name


    def load_provider_metadata(self):
        """
        Load the metadata for the current AI provider from the configuration.

        This method retrieves and sets various attributes like name, URL, API key, etc.,
        for the currently selected AI provider.
        """
        metadata = self.config_provider.get_provider_metadata(self.ai)
        self.name = metadata.get('name', '')
        self.url = metadata.get('url', '')
        self.api_key = metadata.get('apikey', '')
        self.model = metadata.get('model', '')
        self.header_template = metadata.get('header', '')
        self.response_template = metadata.get('response', '')


    def parse_headers(self, headers_str):
        """
        Parse a header string and format the values with the API key.

        Args:
            headers_str (str): A string representation of the headers.

        Returns:
            dict: A dictionary of parsed headers with the API key inserted.
        """
        if headers_str is None:
            return {}

        # Remove the outer curly braces
        headers_str = headers_str.strip().strip('{}')

        # Use regex to split the string into key-value pairs
        pairs = re.findall(r'([\w-]+):\s*([^,}]+)', headers_str)

        headers_dict = {}
        for key, value in pairs:
            # Remove any surrounding whitespace or quotes
            key = key.strip()
            value = value.strip().strip('"')
            # Replace {api_key} with self.api_key, handling cases where the closing brace might be missing
            value = re.sub(r'\{api_key\}?', self.api_key, value)
            headers_dict[key] = value

        return headers_dict


    def prompt(self, prompt: str, model: Optional[str] = None, tokens: int = 1000, verbose: bool = False):
        """
        Send a prompt to the AI provider and get a response.

        Args:
            prompt          (str): The prompt to send to the AI model.
            model (Optional[str]): The specific model to use. If None, uses the default model.
            tokens          (int): The maximum number of tokens to generate in the response.
            verbose        (bool): If True, print the API URL and request details.

        Returns:
            str: The generated response from the AI model.

        Raises:
            requests.RequestException: If there's an error in making the API request.
        """
        # Prepare the API request
        headers = {
            "content-type": "application/json"
        }

        if model:
            self.model = model

        api_headers = self.parse_headers(self.header_template)

        headers.update(api_headers)

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": tokens
        }

        # Print verbose information if requested
        if verbose:
            console.print(f"[cyan]API URL:[/cyan] {self.url}")
            console.print(f"[cyan]Model:[/cyan] {self.model}")
            console.print(f"[cyan]Max Tokens:[/cyan] {tokens}")
            # Print headers but mask sensitive information
            safe_headers = {k: "***" if "key" in k.lower() or "authorization" in k.lower() else v
                           for k, v in headers.items()}
            console.print(f"[cyan]Headers:[/cyan] {safe_headers}")
            console.print(f"[cyan]Request Body:[/cyan]")
            safe_data = data.copy()
            if 'messages' in safe_data and safe_data['messages']:
                prompt_preview = safe_data['messages'][0]['content'][:200] + "..." if len(safe_data['messages'][0]['content']) > 200 else safe_data['messages'][0]['content']
                safe_data['messages'][0]['content'] = prompt_preview
            console.print(safe_data)

        # Make the API request
        response = requests.post(self.url, headers=headers, json=data)

        if verbose:
            console.print(f"[cyan]Response Status:[/cyan] {response.status_code}")
            console.print(f"[cyan]Response Headers:[/cyan] {dict(response.headers)}")
            console.print(f"[cyan]Response Body:[/cyan] {response.text[:500]}")

        response.raise_for_status()

        # Parse and return the result
        return eval(self.response_template)

    @classmethod
    def set_default_provider(cls, provider: Optional[str] = None):
        config = GitConfig()
        if provider:
            config.set_default_provider(provider)
        else:
            config.set_default_provider_interactive()

    def create_new_provider(self):
        provider_name = inquirer.text(message="Enter a name for the new provider:").execute()
        self.config_provider.create_provider(provider_name)
        self.config_provider.configure_provider(provider_name)
        self.ai = provider_name
        self.load_provider_metadata()

    def set_branch_comment(self, branch: str, comment: str):
        """Set a comment for a specific branch.

        Args:
            branch  (str): The name of the branch to comment on
            comment (str): The comment to associate with the branch
        """
        git = GitWrapper()
        git.set_branch_comment(branch, comment)

    def get_branch_comment(self, branch: str) -> Optional[str]:
        """Get the comment associated with a specific branch.

        Args:
            branch (str): The name of the branch to get the comment for

        Returns:
            Optional[str]: The comment if it exists, None otherwise
        """
        git = GitWrapper()
        return git.get_branch_comment(branch)

    def get_all_branch_comments(self) -> Dict[str, str]:
        """Get all branch comments.

        Returns:
            Dict[str, str]: A dictionary mapping branch names to their comments
        """
        git = GitWrapper()
        return git.get_all_branch_comments()
