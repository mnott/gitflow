"""
This module initializes the AI client package.

It provides easy access to the main classes of the package:
AIClient for interacting with AI providers, GitConfig for
managing configurations, and DocGenerator for generating documentation.
"""

from .client import AIClient
from .gitwrapper import GitWrapper
from .gitconfig import GitConfig
from .doc import DocGenerator
