"""
Module providing InjectionToken type and utility to stringify it.
"""

from __future__ import annotations
from typing import Union, Type, Any

InjectionToken = Union[str, Type[Any]]


def stringify_injection_token(token: InjectionToken) -> str:
    """
    Convert an InjectionToken to its string representation.

    Args:
        token (InjectionToken): The injection token, either a string or a type.

    Returns:
        str: The name of the type if token is a type, otherwise the string itself.
    """
    # Use getattr for safe attribute access
    return getattr(token, '__name__', str(token)) if not isinstance(token, str) else token
