from functools import wraps
from typing import Callable, Any

from common.constants import *
from .metadata import *
from .option_metadata import *


def PrxAction(selector: str) -> Callable:
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
        return cls

    return decorator

    return decorator


def Option(required: bool = False, label: str = None, default: Any = Any) -> Callable:
    """
    This Action option decorator
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        # Attach metadata to the function
        wrapper._metadata = {
            'required': required,
            'label': label,
            'default': default
        }
        return wrapper

    return decorator
