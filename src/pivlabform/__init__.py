"""PivLabForm - GitLab as Code"""

__version__ = "0.1.1"
__author__ = "Arsenii Nikulin"

from ._cli_logic import create_click_command
from .pivlabform import Pivlabform

__all__ = ["Pivlabform", "create_click_command"]
