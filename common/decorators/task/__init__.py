from functools import wraps
from typing import Callable
import inspect
from os import path

from common.decorators.task.metadata import TaskDecoratorMetaData
from common.constants import *


def PrxTask(template: str = '', template_url: str = '') -> Callable:
    """
    This Action decorator

    Parameters:
    selector (str): The selector of the action.
    """
    # Get the frame object for the caller of the current function
    frame = inspect.currentframe()
    caller_frame = frame.f_back

    # Get the file path of the caller
    caller_file_path = caller_frame.f_code.co_filename
    call_path: str = path.abspath(caller_file_path)
    template_uri = '' if template_url == '' else path.join(call_path, template_url)

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if TASK_WATERMARK not in watermarks:
            watermarks.append(TASK_WATERMARK)
        else:
            raise Exception("Duplicated Task decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)
        setattr(cls, TASK_DECORATOR_TEMPLATE_URI_KEY, template_uri)
        return cls

    return decorator
