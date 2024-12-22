from typing import Callable
from .task_parse_tree import TaskParseTree
from .task_xml_parser import parse_task_xml
from .task_yaml_parser import parse_task_yaml


def parse_task_template(template_path: str, error_callback: Callable) -> TaskParseTree:
    if template_path.endswith('.xml'):
        return parse_task_xml(template_path, error_callback)
    else:
        return parse_task_yaml(template_path, error_callback)
