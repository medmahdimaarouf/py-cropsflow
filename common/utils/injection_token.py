from __future__ import annotations
from typing import Union, Type, Any

InjectionToken = Union[str, Type[Any]]


def stringify_injection_token(token: InjectionToken) -> str:
    return token.__name__ if isinstance(token, Type) else token
