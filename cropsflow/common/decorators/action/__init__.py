from typing import Callable

from ...constants import *
from .metadata import *


def action(selector: str, auto_next: bool = True) -> Callable:
    """
    This Action decorator
    Parameters:
    selector (str): The selector of the action.
    """

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if ACTION_WATERMARK not in watermarks:
            watermarks.append(ACTION_WATERMARK)
        else:
            raise Exception("Duplicated Action decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)
        setattr(cls, ACTION_DECORATOR_SELECTOR_KEY, selector)
        setattr(cls, ACTION_DECORATOR_AUTO_NEXT_KEY, auto_next)
        return cls

    return decorator
