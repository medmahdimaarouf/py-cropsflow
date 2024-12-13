import xml.etree.ElementTree as ET
from typing import Callable

from common.decorators import TaskDecoratorMetaData
from .task_template import TaskTemplate, TaskTemplateMetaData
from ..injector import Container


def parse_task_xml(task: Container, error_callback: Callable) -> TaskTemplate:
    def handle_error(error, res: any = None) -> any:
        if error_callback is not None:
            error_callback(error)
            return res
        else:
            raise e

    def parse_meta(meta_element) -> TaskTemplateMetaData:
        task_template_metadata = TaskTemplateMetaData()
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
                handle_error(ValueError(f"Unknown tag '{element.tag}' found in <meta>."))
        return task_template_metadata

    def parse_playbook(playbook_element):
        playbook = []
        for action in playbook_element:
            if action.tag not in {"axios-get", "axios-dom-response", "dom-select-all", "key-value",
                                  "dom-attribute-value", "dom-first-child-element", "dom-text-content"}:
                raise ValueError(f"Unknown tag '{action.tag}' found in <playbook>.")

            action_data = {
                "tag": action.tag,
                "attributes": action.attrib,
                "children": parse_playbook(action) if len(action) > 0 else []
            }
            playbook.append(action_data)
        return playbook

    try:
        metadata: TaskDecoratorMetaData = task.metadata
        tree = ET.parse(metadata.template)
        root = tree.getroot()
        task = TaskTemplate()
        task.dataset = root.attrib.get("dataset")

        for child in root:
            if child.tag == "meta":
                task.meta = parse_meta(child)
            elif child.tag == "playbook":
                task.playbook = parse_playbook(child)
            else:
                raise ValueError(f"Unknown tag '{child.tag}' found in <task>.")

        return task
    except FileNotFoundError:
        return handle_error(
            Exception(f"Error: Task '{metadata.target.__name__}' template file '{metadata.template}' was not found."))

        return None
    except ET.ParseError as e:
        return handle_error(ValueError(f"XML parsing error: {e.position[0], e.position[1]}"))
