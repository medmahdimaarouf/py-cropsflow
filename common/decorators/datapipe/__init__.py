from functools import wraps
from typing import Callable

from .metadata import DataPipeDecoratorMetaData
from common.constants import *


def PrxPipe(selector: str) -> Callable:
    """
    This Action decorator
    Parameters:
    selector (str): The selector of the action.
    """

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if PIPE_WATERMARK not in watermarks:
            watermarks.append(PIPE_WATERMARK)
        else:
            raise Exception("Duplicated Pipe decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)
        setattr(cls, DATAPIPE_DECORATOR_SELECTOR_KEY, selector)
        return cls

    return decorator
