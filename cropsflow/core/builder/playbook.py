import inspect
from enum import Enum
from typing import Dict, List

from cropsflow.common import DecoratorMetaDataType, DecoratorMetaData
from cropsflow.common.constants import PLAYBOOK_ACCUMULATOR_ID_OPTION_KEY, PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY, PLAYBOOK_IS_ASYNC_OPTION_KEY, \
    PLAYBOOK_IS_SKIPPABLE_OPTION_KEY
from ..injector import Container
from ..parser import ParseNode, PlaybookParseNode

PLAYBOOK_NODES_CORE_OPTIONS_KEYS = [
    PLAYBOOK_ACCUMULATOR_ID_OPTION_KEY,
    PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY,
    PLAYBOOK_IS_ASYNC_OPTION_KEY,
    PLAYBOOK_IS_SKIPPABLE_OPTION_KEY
]


class EPlaybookNodeType(Enum):
    ROOT = 'ROOT',
    ACTION = 'ACTION',
    PIPE = 'PIPE'


class PlaybookNode:
    parent: 'PlaybookNode' = None
    container: Container
    options: Dict[str, any]
    type: EPlaybookNodeType
    children: List['PlaybookNode'] = []
    parse_node: PlaybookParseNode

    @property
    def skippable(self) -> bool:
        return self.options.get(PLAYBOOK_IS_SKIPPABLE_OPTION_KEY, None) is True

    @property
    def is_async(self) -> bool:
        return self.options.get(PLAYBOOK_IS_ASYNC_OPTION_KEY, None) is True

    @property
    def accumulator_id(self) -> str | None:
        return self.options.get(PLAYBOOK_ACCUMULATOR_ID_OPTION_KEY, None)

    @property
    def accumulator_accessor(self) -> str | None:
        return self.options.get(PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY, None)

    def __init__(self, parse_node: ParseNode, container: Container, options: Dict[str, any] = {}, parent: 'PlaybookNode' = None):
        self.container = container
        self.options = options
        self.parse_node = parse_node
        self.parent = parent
        self.children = []
        if self.container.metadata.type == DecoratorMetaDataType.ACTION:
            self.type = EPlaybookNodeType.ACTION
        elif self.container.metadata.type == DecoratorMetaDataType.DATAPIPE:
            self.type = EPlaybookNodeType.PIPE
        elif self.container.metadata.type == DecoratorMetaDataType.TASK:
            self.type = EPlaybookNodeType.ROOT
        else:
            raise Exception(f'RunnerQueueException: {self.container.get_name()} is not a runnable dependency')

    def append(self, parse_node: ParseNode, container: Container, options: Dict[str, any]) -> 'PlaybookNode':
        child_node: PlaybookNode = PlaybookNode(parse_node=parse_node, container=container, options=options, parent=self)
        self.children.append(child_node)
        return child_node

    def remove(self, container: Container) -> 'PlaybookNode':
        self.children = [child for child in self.children if child.container.id != container.id]
        return self
