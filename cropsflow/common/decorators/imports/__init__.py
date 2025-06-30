from typing import Type, Callable

from ...constants import *


def imports(**args: list[Type[any]]) -> Callable:
    def decorator(cls):
        setattr(cls, MODULE_DECORATOR_IMPORTS_KEY, [_ for _ in args if _ is not None])
        return cls

    return decorator
