import ast
from copy import copy
from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable
from cropsflow.common.decorators import Option
from cropsflow.core.exceptions.builder import *
from cropsflow.core.builder.task_playbook import TaskPlaybook, PlaybookNode
from cropsflow.core.injector import Container, Task
from cropsflow.core.parser import TaskPlaybookParseNode, parse_task_template, TaskParseTree
from cropsflow.core.inspector.metadata_inspector import scan_class_options
from cropsflow.core.utils import parse_value

task_playbook_item_core_keys = ['pipe', 'pipe_accessor']


@dataclass
class TaskTemplate:
    dataset: str
    bucket: str
    meta_data: Dict[str, str] = field(default_factory=dict)
    playbook: TaskPlaybook = field(default_factory=list)

    def __init__(self, meta_data: Dict[str, str], playbook: List[dict], bucket: str = None, dataset: str = None):
        self.meta_data = meta_data
        self.playbook = playbook
        self.dataset = dataset
        self.bucket = bucket


def build_playbook_node(task: Task, parse_node: TaskPlaybookParseNode, error_handler: Callable) -> PlaybookNode:
    action_or_pipe: Container = task.get_action(selector=parse_node.selector) or task.get_pipe(selector=parse_node.selector)
    if action_or_pipe is None:
        error_handler(UnknownNodeSelectorException(template_file_path=task.metadata.template, node_name=parse_node.selector, line=parse_node.line, column=0))
        return

    action_or_pipe_options: Dict[str, Option] = copy(scan_class_options(action_or_pipe.metadata.target))
    parsed_node_options: Dict[str, str] = parse_node.options.items()
    bindings: Dict[str, Any] = {}

    for key, value in parsed_node_options:
        if action_or_pipe_options.keys().__contains__(key.strip()) is not None or task_playbook_item_core_keys.__contains__(key.strip()):
            bindings[key] = parse_value(val_str=value)
        else:
            error_handler(UnknownOptionException(template_file_path=task.metadata.template, name=key,
                                                 node_name=parse_node.selector, line=parse_node.line))

    for key, action_or_pipe_option in action_or_pipe_options.items():
        # Todo :  replace required with optional default value check
        if not bindings.keys().__contains__(key.strip()) and action_or_pipe_option.required is True:
            error_handler(
                MissedRequiredOptionException(template_file_path=task.metadata.template, name=key, node_name=parse_node.selector, line=parse_node.line))
        else:
            bindings.setdefault(key.strip(), action_or_pipe_option.default)

    node = PlaybookNode.create(action_or_pipe=action_or_pipe, bindings=bindings)
    for child in parse_node.children:
        node.nodes.append(build_playbook_node(task=task, parse_node=child, error_handler=error_handler))
    return node


def build_task(task: Task, error_callback: Callable = None) -> TaskTemplate:
    has_error: bool = False

    def handle_error(e):
        nonlocal has_error
        has_error = True
        if error_callback:
            error_callback(e)
        else:
            raise e

    task_parse_tree: TaskParseTree = parse_task_template(task.metadata.template, handle_error)
    task_playbook: TaskPlaybook = []

    for playbook_item_node in task_parse_tree.playbook:
        playbook_item: PlaybookNode = build_playbook_node(task=task, parse_node=playbook_item_node, error_handler=handle_error)
        task_playbook.append(playbook_item)
    return TaskTemplate(meta_data=task_parse_tree.meta_data, dataset=task_parse_tree.dataset, bucket=task_parse_tree.bucket, playbook=task_playbook)
