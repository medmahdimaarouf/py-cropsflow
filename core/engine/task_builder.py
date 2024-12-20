import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable
from common.decorators import OptionMetaData
from ..injector import Container, Task
from ..parser import TaskPlaybookParseNode, parse_task_template, TaskParseTree
from ..scanner.metadata_scanner import scan_class_options

task_playbook_item_core_keys = ['pipe', 'pipe_accessor']


@dataclass
class TaskPlaybookItem:
    parent: "TaskPlaybookItem"
    action_or_pipe: Container
    id: str = field(default_factory=str)
    bindings: Dict[str, Any] = field(default_factory=dict)
    children: List["TaskPlaybookItem"] = field(default_factory=list)

    def __int__(self, action_or_pipe: Container, parent: "TaskPlaybookItem" = None):
        self.id = uuid.uuid4()
        self.action_or_pipe = action_or_pipe
        self.parent = parent


TaskPlaybook = List[TaskPlaybookItem]


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


def build_playbook(task: Task, parse_node: TaskPlaybookParseNode,
                   handleError: Callable, parent: TaskPlaybookItem = None) -> TaskPlaybookItem:
    action_or_pipe: Container = task.get_action(selector=parse_node.selector)
    if action_or_pipe is None:
        action_or_pipe = task.get_pipe(selector=parse_node.selector)
    if action_or_pipe is None:
        raise Exception(
            f"No action or pipe found by selector '{parse_node.selector}' in @task {task.get_name()} at line : {parse_node.line}")
    bindings: Dict[str, Any] = {}
    action_or_pipe_options: Dict[str, OptionMetaData] = scan_class_options(action_or_pipe.metadata.target)
    for name, value in parse_node.options.items():
        option = action_or_pipe_options.get(name.strip(), None)
        if option is not None:
            # todo: parse value from field annotation type
            bindings[name] = value
            action_or_pipe_options.pop(name.strip())
        else:
            handleError(Exception(
                f"Unknown @option '{name}' for {action_or_pipe.get_name()} selected by '{parse_node.selector}' at line : {parse_node.line}"))
    if len(action_or_pipe_options):
        for key, action_or_pipe_option in action_or_pipe_options.items():
            # Todo :  replace required with optional default value check
            if not action_or_pipe_option.required:
                continue
            handleError(Exception(
                f"Required option '{key}' binding for action '{action_or_pipe.get_name()}' selected by '{parse_node.selector}' at line : {parse_node.line}"))
    for child in parse_node.children:
        build_playbook(child)
    return TaskPlaybookItem(action_or_pipe=action_or_pipe, parent=parent, bindings=bindings)


def build_task(task: Task, error_callback: Callable = None) -> bool:
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
        playbook_item: TaskPlaybookItem = build_playbook(playbook_item_node)
        task_playbook.append(playbook_item)
    template: TaskTemplate = TaskTemplate(meta_data=task_parse_tree.meta_data, dataset=task_parse_tree.dataset,
                                          bucket=task_parse_tree.bucket, playbook=task_playbook)
    return not has_error
