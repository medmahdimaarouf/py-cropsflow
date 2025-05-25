import inspect
from copy import copy
from dataclasses import dataclass, field
from typing import Dict, Any, Callable, List

from cropsflow.common.decorators import Option
from .playbook import PlaybookNode, PLAYBOOK_NODES_CORE_OPTIONS_KEYS
from cropsflow.core.abstracts import Builder
from cropsflow.core.exceptions.builder import *
from cropsflow.core.injector import Container, Task
from cropsflow.core.parser import TaskPlaybookParseNode, parse_task_template, TaskParseTree
from cropsflow.core.scanner.metadata_scanner import scan_class_options
from cropsflow.core.utils import parse_value


@dataclass
class TaskTemplateMetaData:
    title: str = field(default_factory=str)
    version: str = field(default_factory=str)
    description: str = field(default_factory=str)
    readme: str = field(default_factory=str)
    keywords: List[str] = field(default_factory=list[str])


@dataclass
class TaskTemplateInputSchema:
    pass


@dataclass
class TaskTemplate:
    template_file_path: str = field(default=str)
    metadata: TaskTemplateMetaData = field(default_factory=TaskTemplateMetaData)
    input_schema: TaskTemplateInputSchema = field(default_factory=TaskTemplateInputSchema)
    playbook: PlaybookNode = None


class TaskTemplateBuilder(Builder[TaskTemplate]):
    task: Task
    parse_tree: TaskParseTree = None

    def __init__(self, task: Task):
        self.task = task

    def build(self, error_callback: Callable[[Exception], None] = None) -> TaskTemplate:
        self.parse_tree = parse_task_template(template_path=self.template_file_path(), error_callback=error_callback)
        task_template: TaskTemplate = TaskTemplate(template_file_path=self.template_file_path())
        task_template.metadata = self.build_metadata(error_callback=error_callback)
        task_template.input_schema = self.build_input_schema(error_callback=error_callback)
        task_template.playbook = self.__build_template_playbook(error_callback=error_callback)
        return task_template

    def template_file_path(self) -> str:
        return self.task.metadata.template.strip()

    def class_file(self) -> str:
        return inspect.getfile(self.task.metadata.target).strip()

    def build_metadata(self, error_callback: Callable[[Exception], None]) -> TaskTemplateMetaData:
        return TaskTemplateMetaData(title=self.parse_tree.metadata.get('title'), description=self.parse_tree.metadata.get('description'),
                                    readme=self.parse_tree.metadata.get('readme'), keywords=self.parse_tree.metadata.get('keywords') or [])

    def build_input_schema(self, error_callback: Callable[[Exception], None]) -> TaskTemplateInputSchema:
        return TaskTemplateInputSchema()

    def __build_template_playbook(self, error_callback: Callable[[Exception], None]) -> PlaybookNode:
        runner_node: PlaybookNode = PlaybookNode(container=self.task)
        for parse_node in self.parse_tree.playbook:
            self.__build_playbook_node(parse_node=parse_node, error_handler=error_callback, parent=runner_node)
        return runner_node

    def __build_playbook_node(self, parse_node: TaskPlaybookParseNode, error_handler: Callable[[Exception], None],
                              parent: PlaybookNode) -> None:
        # initialize runner container
        action_or_pipe: Container = self.task.get_action(selector=parse_node.selector) or self.task.get_pipe(selector=parse_node.selector)
        if action_or_pipe is None:
            error_handler(
                UnknownNodeSelectorException(template_file_path=self.template_file_path(), node_name=parse_node.selector, line=parse_node.line, column=0))
            return

        # building runner options
        action_or_pipe_options: Dict[str, Option] = copy(scan_class_options(action_or_pipe.metadata.target))
        parsed_node_options: Dict[str, str] = parse_node.options.items()
        options: Dict[str, Any] = {}

        for key, value in parsed_node_options:
            if action_or_pipe_options.keys().__contains__(key.strip()) is not None or key.strip() in PLAYBOOK_NODES_CORE_OPTIONS_KEYS:
                options[key] = parse_value(val_str=value)
            else:
                error_handler(
                    UnknownOptionException(template_file_path=self.template_file_path(), name=key, node_name=parse_node.selector, line=parse_node.line)
                )

        for key, action_or_pipe_option in action_or_pipe_options.items():
            if key.strip() not in options and action_or_pipe_option.required is True:
                error_handler(
                    MissedRequiredOptionException(template_file_path=self.template_file_path(), name=key, node_name=parse_node.selector, line=parse_node.line))
            else:
                options.setdefault(key.strip(), action_or_pipe_option.default)
        # append the node to parent
        node: PlaybookNode = parent.append(container=action_or_pipe, options=options)
        # assign file line from parse node to track template code
        node.file_line = parse_node.line
        # build its children
        for child_parse_node in parse_node.children:
            self.__build_playbook_node(parent=node, parse_node=child_parse_node, error_handler=error_handler)


def build_task(task: Task, error_callback: Callable = None) -> TaskTemplate:
    has_error: bool = False

    def handle_error(e):
        nonlocal has_error
        has_error = True
        if error_callback:
            error_callback(e)
        else:
            raise e

    return TaskTemplateBuilder(task=task).build(error_callback=handle_error)
