from typing import Callable, Any, List, Type, TypeVar

from .option_metadata import Option
from ...constants import OPTION_DECORATOR_KEY

T = TypeVar('T')


def option(key: str, meta_type: Type[T] = None, default: T = None, required: bool = False,
           select: List[T] = None) -> Callable:
    """
    This option decorator
    """

    def decorator(cls):
        options = getattr(cls, OPTION_DECORATOR_KEY, {})
        if options.get(key.strip()) is None:
            options[key.strip()] = Option(key=key, meta_type=meta_type, required=required, default=default,
                                          select=select)
        else:
            raise Exception(f"The @option '{key}' is already defined in {cls.__name__}")
        setattr(cls, OPTION_DECORATOR_KEY, options)
        return cls

    return decorator
