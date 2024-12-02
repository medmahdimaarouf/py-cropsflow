from typing import Callable, Union, Type, Any

from .metadata import *
from common.constants import *


def Service(provide_in: Union[str, Type[Any]]) -> Callable:
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
        setattr(cls, INJECTABLE_DECORATOR_PROVIDER_HOST_KEY, provide_in)
        return cls

    return decorator
