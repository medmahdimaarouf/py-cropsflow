import os
from functools import wraps
from typing import Callable
import inspect
from os import path

from common.decorators.task.metadata import TaskDecoratorMetaData
from common.constants import *


def task(template_path: str = '') -> Callable:
    """
        This Action decorator marks a class as a task and assigns a template URI.

        Parameters:
        template_path (str): Relative path to the task's template file.

        Raises:
        Exception: If the decorator is applied multiple times to the same class.
    """
    # Get the frame object for the caller of the current function
    frame = inspect.currentframe()
    caller_frame = frame.f_back

    # Get the directory of the caller file
    caller_file_path = caller_frame.f_code.co_filename
    caller_directory = os.path.dirname(os.path.abspath(caller_file_path))

    # Resolve the template path relative to the caller's directory
    template_uri = os.path.normpath(os.path.join(caller_directory, template_path))

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if TASK_WATERMARK not in watermarks:
            watermarks.append(TASK_WATERMARK)
        else:
            raise Exception("Duplicated @Task decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)
        setattr(cls, TASK_DECORATOR_TEMPLATE_URI_KEY, template_uri)
        return cls

    return decorator
