from typing import Type, Callable, Any

from ...constants import *


def deps(*args: Type[Any]) -> Callable:
    def decorator(cls):
        setattr(cls, MODULE_DECORATOR_DECLARATIONS_KEY, [_ for _ in args if _ is not None])
        return cls

    return decorator
