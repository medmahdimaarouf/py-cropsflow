from typing import Callable

from ..injector import Container
from .task_parser import parse_task
from .task_template import TaskTemplate


def build_task(task: Container, error_callback: Callable) -> TaskTemplate:
    template = parse_task(task, error_callback)
    return template
