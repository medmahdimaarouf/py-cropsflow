from typing import Callable, Union, Type, Any

from .metadata import *
from common.constants import *
from ..inject import InjectionScope


def Service(scope: InjectionScope) -> Callable:
    """
    This Action decorator
    Parameters:
    selector (str): The selector of the action.
    """

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if INJECTABLE_WATERMARK not in watermarks:
            watermarks.append(INJECTABLE_WATERMARK)
        else:
            raise Exception("Duplicated Injectable decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)
        setattr(cls, INJECTABLE_DECORATOR_INJECTION_SCOPE_KEY, scope)
        return cls

    return decorator
