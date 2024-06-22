"""Module to store core configurations and settings."""

from .config import adapter_configuration, configuration
from .exceptions import RequestFailedError

__all__ = ["adapter_configuration", "configuration", "RequestFailedError"]
