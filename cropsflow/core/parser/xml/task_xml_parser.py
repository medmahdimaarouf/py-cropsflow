import inspect
from typing import Callable, Dict, List

from lxml.etree import Element, XMLSyntaxError, parse

from cropsflow.core.exceptions import TaskBuildException
from cropsflow.core.parser.task_parse_tree import TaskParseTree, PlaybookParseNode


class XMLTaskTemplateParser:

    def __init__(self, template_file_name: str):
        self.template_file_name: str = template_file_name

    def read_line(self, line: int):
        with open(self.template_file_name, "r") as file:
            lines = file.readlines()
            return lines[line].strip() if line < len(lines) else None

    def parse_playbook_item(self, playbook_element: Element, error_callback: Callable) -> PlaybookParseNode:
        options: Dict[str, str] = {}
        for key, attr in playbook_element.attrib.items():
            options[key.strip()] = attr.strip()
        items: List[PlaybookParseNode] = []

        for child in playbook_element:
            items.append(self.parse_playbook_item(playbook_element=child, error_callback=error_callback))

        return PlaybookParseNode(selector=playbook_element.tag.strip(),
                                 options=options,
                                 line=playbook_element.sourceline,
                                 column=0,
                                 template_file_name=self.template_file_name,
                                 source=self.read_line(playbook_element.sourceline),
                                 children=items)

    def parse_metadata(self, meta_element: Element, error_callback: Callable) -> Dict[str, str]:
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

    '''
        bad behavior
        @todo: parse returns and child could bbe null , 
    '''

    def parse(self, template_path: str, error_callback: Callable) -> TaskParseTree:
        def handle_error(error, res: any = None) -> any:
            if error_callback is not None:
                error_callback(error)
                return res
            else:
                raise e

        try:
            root = parse(source=template_path).getroot()
            parsed_metadata: Dict[str, str] = {}
            parsed_playbook: PlaybookParseNode = None
            for child in root:
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
                    parsed_playbook = PlaybookParseNode(line=child.sourceline,
                                                        column=0,
                                                        template_file_name=template_path,
                                                        selector='playbook',
                                                        source=self.read_line(child.sourceline),
                                                        children=[]
                                                        )
                    for playbook_element in child:
                        parsed_playbook.children.append(
                            self.parse_playbook_item(playbook_element=playbook_element, error_callback=error_callback))
                else:
                    handle_error(TaskBuildException(message=f"Unknown tag '{child.tag}' found in <task>.",
                                                    template_file_path=template_path, line=1))

            return TaskParseTree(metadata=parsed_metadata, playbook=parsed_playbook)

        except FileNotFoundError:
            return handle_error(
                Exception(f"Error: template file '{template_path}' was not found.")
            )

        except XMLSyntaxError as e:
            return handle_error(
                ValueError(f"XML parsing template {template_path} error: {e.position[0], e.position[1]}"))
