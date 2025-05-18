from typing import Callable, Dict, List

from lxml.etree import Element, XMLSyntaxError, parse

from .task_parse_tree import TaskParseTree, TaskPlaybookParseNode


def parse_playbook_item(playbook_element: Element, error_callback: Callable) -> TaskPlaybookParseNode:
    options: Dict[str, str] = {}
    for key, attr in playbook_element.attrib.items():
        options[key.strip()] = attr.strip()
    items: List[TaskPlaybookParseNode] = []

    for child in playbook_element:
        items.append(parse_playbook_item(child, error_callback))

    return TaskPlaybookParseNode(selector=playbook_element.tag.strip(),
                                 options=options,
                                 line=playbook_element.sourceline,
                                 children=items)


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


def parse_task_xml(template_path: str, error_callback: Callable) -> TaskParseTree:
    def handle_error(error, res: any = None) -> any:
        if error_callback is not None:
            error_callback(error)
            return res
        else:
            raise e

    try:
        tree = parse(source=template_path).getroot()
        parsed_metadata: Dict[str, str] = {}
        parsed_playbook: List[TaskPlaybookParseNode] = []

        for child in tree:
            if child.tag == "title":
                parsed_metadata['title'] = child.text.strip() if child.text else None
            elif child.tag == "version":
                parsed_metadata['version'] = child.text.strip() if child.text else None
            elif child.tag == "description":
                parsed_metadata['description'] = child.text.strip() if child.text else None
            elif child.tag == "tags":
                parsed_metadata['tags'] = str(child.text).strip().split(',') if child.text else []
            elif child.tag == "readme" and "src" in child.attrib:
                parsed_metadata['readme'] = child.attrib["src"]
            elif child.tag == "playbook":
                for playbook_item in child:
                    parsed_playbook.append(parse_playbook_item(playbook_item, error_callback))
            else:
                handle_error(ValueError(f"Unknown tag '{child.tag}' found in <task>."))

        return TaskParseTree(meta_data=parsed_metadata, playbook=parsed_playbook)

    except FileNotFoundError:
        return handle_error(
            Exception(f"Error: template file '{template_path}' was not found.")
        )

    except XMLSyntaxError as e:
        return handle_error(ValueError(f"XML parsing template {template_path} error: {e.position[0], e.position[1]}"))
