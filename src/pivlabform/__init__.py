"""PivLabForm - GitLab configuration management tool."""

__version__ = "0.1.0"
__author__ = "Your Name"

from ._cli_logic import create_click_command
from .pivlabform import Pivlabform

__all__ = ["Pivlabform", "create_click_command"]
