from typing import Callable

from ..injector import Container
from common.decorators import TaskDecoratorMetaData
from lxml import etree


def parse_task(task: Container, error_callback: Callable):
    metadata: TaskDecoratorMetaData = task.metadata
    task_template_path: str = metadata.template
    try:
        tree = etree.parse(task_template_path)
        root = tree.getroot()

        for element in root.iter():
            print(
                f"Tag: {element.tag}, Attributes: {element.attrib}, Text: {element.text.strip() if element.text else ''}")
        return True
    except FileNotFoundError as e:
        exception = Exception(
            f"Error: Task '{metadata.target.__name__}' template file '{task_template_path}' was not found.")
        if error_callback is not None:
            error_callback(exception)
        else:
            raise exception
        return None
    except etree.XMLSyntaxError as e:
        exception = Exception(
            f"Error: Task '{metadata.target.__name__}' parse error at line {e.position[0]}, column {e.position[1]}")
        if error_callback is not None:
            error_callback(exception)
        else:
            raise exception
        return None


def build_task(task: Container, error_callback: Callable = None):
    try:
        task_parse = parse_task(task)
    except Exception as e:
        if error_callback is not None:
            error_callback(e)
        else:
            raise e
