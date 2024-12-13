from ..injector import Container
from .task_parser import parse_task_xml


def build_task(task: Container):
    try:
        template = parse_task_xml(task)
    except Exception as e:
        print(str(e))
