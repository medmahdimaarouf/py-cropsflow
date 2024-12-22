import sys
import uuid
from abc import abstractmethod, ABC
from dataclasses import field
from copy import copy
from typing import Generic, List, TypeVar, Dict, Any
from ..injector import Container
from common.decorators import InjectionScope, ActionDecoratorMetaData, DataPipeDecoratorMetaData
from common.abstracts import Action, Pipe, TaskContext

T = TypeVar('T')


class PlaybookNode(Generic[T], ABC):
    id: str
    parent: "PlaybookNode"
    action_or_pipe: Container
    bindings: Dict[str, Any]
    nodes: List["PlaybookNode"]

    def __init__(self, action_or_pipe: Container, bindings: Dict[str, Any] = {}, parent: "PlaybookNode" = None):
        self.id = str(uuid.uuid4())
        self.parent = parent
        self.action_or_pipe = action_or_pipe
        self.bindings = bindings
        self.nodes = []

    @abstractmethod
    def run(self, context: TaskContext) -> TaskContext:
        pass

    def instantiate(self) -> T:
        return self.action_or_pipe.injector.resolve(scope=InjectionScope.TRANSIENT, optional=False)

    @staticmethod
    def create(action_or_pipe: Container, bindings: Dict[str, Any], parent: "PlaybookNode" = None):
        from .task_playbook import PipePlaybookNode, ActionPlaybookNode
        if isinstance(action_or_pipe.metadata, ActionDecoratorMetaData):
            return ActionPlaybookNode(action_or_pipe=action_or_pipe, bindings=bindings, parent=parent)
        elif isinstance(action_or_pipe.metadata, DataPipeDecoratorMetaData):
            return PipePlaybookNode(action_or_pipe=action_or_pipe, bindings=bindings, parent=parent)

    def add_node(self, action_or_pipe: Container, bindings: Dict[str, Any]):
        self.nodes.append(PlaybookNode.create(action_or_pipe=action_or_pipe, bindings=bindings, parent=self))


class PipePlaybookNode(PlaybookNode[Pipe]):

    async def run(self, context: TaskContext) -> TaskContext:
        context = copy(context)
        sys.stdout.write(f"running Pipe {self.action_or_pipe.metadata.target.__name__} ...")
        try:
            instance: Pipe = self.instantiate()
            instance.options(options=self.bindings)
            for node in self.nodes:
                await node.run(context=context)
            instance.accumulate()
            return context
        except Exception as e:
            print(f"error running Pipe {self.action_or_pipe.metadata.target.__name__}")


class ActionPlaybookNode(PlaybookNode[Action]):

    async def run(self, context: TaskContext) -> TaskContext:
        context = copy(context)
        print(f"running action {self.action_or_pipe.metadata.target.__name__} ...")
        instance: Action = self.instantiate()

        await instance.run(context=context, options=self.bindings)

        for node in self.nodes:
            await node.run(context=context)
        print(f"completed action {self.action_or_pipe.metadata.target.__name__}")

        return context


TaskPlaybook = List[PlaybookNode]
