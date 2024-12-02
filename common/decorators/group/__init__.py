from functools import wraps
from typing import List, Callable

from common.constants import *


def Group(name: str, route: List[str]) -> Callable:
    """
    This Action decorator
    Parameters:
    selector (str): The selector of the action.
    """

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if GROUP_WATERMARK not in watermarks:
            watermarks.append(GROUP_WATERMARK)
        else:
            raise Exception("Duplicated Module decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)

        setattr(cls, GROUP_DECORATOR_NAME_KEY, name)
        setattr(cls, GROUP_DECORATOR_ROUTE_KEY, route)

        return cls

    return decorator
