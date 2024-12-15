from typing import Callable, Any, List

from .option_metadata import OptionMetaData
from ...constants import OPTION_DECORATOR_KEY


def option(name: str, required: bool = False, default: Any = None, select: List[Any] = None) -> Callable:
    """
    This option decorator
    """

    def decorator(func):
        setattr(func, OPTION_DECORATOR_KEY,
                OptionMetaData(setter_name=func.__name__, name=name, required=required, default=default, select=select))
        return func

    return decorator
