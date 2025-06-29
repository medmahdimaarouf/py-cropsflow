from typing import Type, Callable
from ...constants import *


def exports(*args: list[Type[any] | str]) -> Callable:
    def decorator(cls):
        setattr(cls, MODULE_DECORATOR_EXPORTS_KEY, [_ for _ in args if _ is not None])
        return cls

    return decorator
