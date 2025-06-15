import uuid
from enum import Enum
from typing import Dict, List

from cropsflow.common import DecoratorMetaDataType
from cropsflow.common.constants import PLAYBOOK_TRANSFORMER_PIPE_ID_OPTION_KEY, \
    PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY, \
    PLAYBOOK_IS_ASYNC_OPTION_KEY, \
    PLAYBOOK_IS_SKIPPABLE_OPTION_KEY
from ..injector import Container
from ..parser import ParseNode, PlaybookParseNode

PLAYBOOK_NODES_CORE_OPTIONS_KEYS = [
    PLAYBOOK_TRANSFORMER_PIPE_ID_OPTION_KEY,
    PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY,
    PLAYBOOK_IS_ASYNC_OPTION_KEY,
    PLAYBOOK_IS_SKIPPABLE_OPTION_KEY
]


class EPlaybookNodeType(Enum):
    ROOT = 'ROOT',
    ACTION = 'ACTION',
    PIPE = 'PIPE'


class PlaybookNode:

    @property
    def skippable(self) -> bool:
        return self.options.get(PLAYBOOK_IS_SKIPPABLE_OPTION_KEY, None) is True

    @property
    def is_async(self) -> bool:
        return self.options.get(PLAYBOOK_IS_ASYNC_OPTION_KEY, None) is True

    @property
    def transformer_pipe_id(self) -> str | None:
        return self.options.get(PLAYBOOK_TRANSFORMER_PIPE_ID_OPTION_KEY, None)

    @property
    def accumulator_accessor(self) -> str | None:
        return self.options.get(PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY, None)

    def __init__(self, parse_node: ParseNode, container: Container, options: Dict[str, any] = {},
                 parent: 'PlaybookNode' = None):
        self.id = uuid.uuid4()
        self.parent: 'PlaybookNode' = parent
        self.container: Container = container
        self.options: Dict[str, any] = options
        self.parse_node: PlaybookParseNode = parse_node
        self.children: List['PlaybookNode'] = []
        if self.container.metadata.type == DecoratorMetaDataType.ACTION:
            self.type: EPlaybookNodeType = EPlaybookNodeType.ACTION
        elif self.container.metadata.type == DecoratorMetaDataType.DATAPIPE:
            self.type: EPlaybookNodeType = EPlaybookNodeType.PIPE
        elif self.container.metadata.type == DecoratorMetaDataType.TASK:
            self.type: EPlaybookNodeType = EPlaybookNodeType.ROOT
        else:
            raise Exception(f'RunnerQueueException: {self.container.get_name()} is not a runnable dependency')

    def append(self, parse_node: ParseNode, container: Container, options: Dict[str, any]) -> 'PlaybookNode':
        child_node: PlaybookNode = PlaybookNode(parse_node=parse_node, container=container, options=options,
                                                parent=self)
        self.children.append(child_node)
        return child_node

    def remove(self, container: Container) -> 'PlaybookNode':
        self.children = [child for child in self.children if child.container.id != container.id]
        return self
