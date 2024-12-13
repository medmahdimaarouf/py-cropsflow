from lxml.etree import ElementTree, Element, XMLSyntaxError, parse
from typing import Callable, Dict, List

from common.decorators import TaskDecoratorMetaData
from .task_parse_tree import TaskParseTree, TaskPlaybookParseTree
from ..injector.task import Task


def parse_playbook(playbook_element: Element, error_callback: Callable) -> TaskPlaybookParseTree:
    options: Dict[str, str] = {}
    for key, attr in playbook_element.attrib.items():
        options[key.strip()] = attr.strip()
    playbook_parse_tree: TaskPlaybookParseTree = TaskPlaybookParseTree(selector=playbook_element.tag.strip(),
                                                                       options=options,
                                                                       line=playbook_element.sourceline)

    for child in playbook_element:
        playbook_parse_tree.children.append(parse_playbook(child, error_callback))
    return playbook_parse_tree


def parse_meta(meta_element: Element, error_callback: Callable) -> Dict[str, str]:
    task_template_metadata = {}
    for element in meta_element:
        if element.tag == "title":
            task_template_metadata['title'] = element.text.strip() if element.text else None
        elif element.tag == "version":
            task_template_metadata['version'] = element.text.strip() if element.text else None
        elif element.tag == "description":
            task_template_metadata['description'] = element.text.strip() if element.text else None
        elif element.tag == "tags":
            task_template_metadata['tags'] = str(element.text).strip().split(',') if element.text else []
        elif element.tag == "readme" and "src" in element.attrib:
            task_template_metadata['readme'] = element.attrib["src"]
        else:
            error_callback(ValueError(f"Unknown tag '{element.tag}' found in <meta>. line {element.sourceline}"))
    return task_template_metadata


def parse_task_xml(task: Task, error_callback: Callable) -> TaskParseTree:
    def handle_error(error, res: any = None) -> any:
        if error_callback is not None:
            error_callback(error)
            return res
        else:
            raise e

    try:
        metadata: TaskDecoratorMetaData = task.metadata
        tree = parse(source=metadata.template).getroot()
        parsed_metadata: Dict[str, str] = {}
        parsed_playbook: List[TaskPlaybookParseTree] = []

        for child in tree:
            if child.tag == "meta":
                parsed_metadata = parse_meta(child, error_callback)
            elif child.tag == "playbook":
                parsed_playbook = parse_playbook(child, error_callback)
            else:
                handle_error(ValueError(f"Unknown tag '{child.tag}' found in <task>."))

        return TaskParseTree(meta_data=parsed_metadata, playbook=parsed_playbook)

    except FileNotFoundError:
        return handle_error(
            Exception(f"Error: Task '{metadata.target.__name__}' template file '{metadata.template}' was not found.")
        )

    except XMLSyntaxError as e:
        return handle_error(ValueError(f"XML parsing error: {e.position[0], e.position[1]}"))


def parse_task_yaml(task: Task, error_callback: Callable) -> TaskParseTree:
    return None


def parse_task(task: Task, error_callback: Callable) -> TaskParseTree:
    if task.metadata.template.endswith('.xml'):
        return parse_task_xml(task, error_callback)
    else:
        return parse_task_yaml(task, error_callback)
