from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable
from common.decorators import OptionMetaData
from .task_playbook import TaskPlaybook, PlaybookNode
from ..injector import Container, Task
from ..parser import TaskPlaybookParseNode, parse_task_template, TaskParseTree
from ..scanner.metadata_scanner import scan_class_options

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
    action_or_pipe: Container = task.get_action(selector=parse_node.selector)
    if action_or_pipe is None:
        action_or_pipe = task.get_pipe(selector=parse_node.selector)
    if action_or_pipe is None:
        raise error_handler(Exception(
            f"No action or pipe found by selector '{parse_node.selector}' in @task {task.get_name()} at line : {parse_node.line}"))
    bindings: Dict[str, Any] = {}
    action_or_pipe_options: Dict[str, OptionMetaData] = scan_class_options(action_or_pipe.metadata.target)
    for name, value in parse_node.options.items():
        option = action_or_pipe_options.get(name.strip(), None)
        if option is not None:
            # todo: parse value from field annotation type
            bindings[name] = value
            action_or_pipe_options.pop(name.strip())
        else:
            error_handler(Exception(
                f"Unknown @option '{name}' for {action_or_pipe.get_name()} selected by '{parse_node.selector}' at line : {parse_node.line}"))

    if len(action_or_pipe_options):
        for key, action_or_pipe_option in action_or_pipe_options.items():
            # Todo :  replace required with optional default value check
            if not action_or_pipe_option.required:
                continue
            error_handler(Exception(
                f"Required option '{key}' binding for action '{action_or_pipe.get_name()}' selected by '{parse_node.selector}' at line : {parse_node.line}"))
    node = PlaybookNode.create(action_or_pipe=action_or_pipe, bindings=bindings)
    for child in parse_node.children:
        node.add_node(build_playbook_node(task=task, parse_node=child, error_handler=error_handler))
    return node


def build_task(task: Task, error_callback: Callable = None) -> TaskTemplate:
    has_error: bool = False

    def handleError(e):
        nonlocal has_error
        has_error = True
        if error_callback:
            error_callback(e)
        else:
            raise e

    task_parse_tree: TaskParseTree = parse_task_template(task.metadata.template, error_callback)
    task_playbook: TaskPlaybook = []

    for playbook_item_node in task_parse_tree.playbook:
        playbook_item: PlaybookNode = build_playbook_node(task=task, parse_node=playbook_item_node,
                                                          error_handler=error_callback)
        task_playbook.append(playbook_item)
    return TaskTemplate(meta_data=task_parse_tree.meta_data, dataset=task_parse_tree.dataset,
                        bucket=task_parse_tree.bucket, playbook=task_playbook)
