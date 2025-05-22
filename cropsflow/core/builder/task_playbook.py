import sys
import uuid
from abc import abstractmethod, ABC
from copy import copy
from typing import Generic, List, TypeVar, Dict, Any, Optional

from cropsflow import Init, Destroy
from cropsflow.core.injector import Container
from cropsflow.common.decorators import InjectionScope, ActionDecoratorMetaData, DataPipeDecoratorMetaData
from cropsflow.common.abstracts import Action, Pipe, TaskContext

T = TypeVar('T')


class PlaybookNode(Generic[T], ABC):
    id: str
    parent: "PlaybookNode"
    action_or_pipe: Container
    bindings: Dict[str, Any]
    nodes: List["PlaybookNode"]
    instance: T = None

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
        self.instance = self.action_or_pipe.injector.resolve(scope=InjectionScope.TRANSIENT, optional=False)
        return self.instance

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
    accumulator_pipe: "PipePlaybookNode" = None

    def __init__(self, action_or_pipe: Container, bindings: Dict[str, Any] = {}, parent: "PlaybookNode" = None):
        super().__init__(action_or_pipe=action_or_pipe, bindings=bindings, parent=parent)
        self.accumulator_pipe = self.find_parent_pipe(id=bindings.get('pipe'))
        if bindings.get('pipe') is not None and self.accumulator_pipe is None:
            raise Exception(f'Could not locate target accumulator pipe with id {bindings.get("pipe")}')

    def find_parent_pipe(self, id: str = None) -> Optional["PlaybookNode"]:
        parent: PlaybookNode = self.parent
        while parent:
            parent = parent.parent
            if isinstance(parent, PipePlaybookNode) and (True if id is None else parent.bindings.get("id") == id):
                return parent
        return None

    async def run(self, context: TaskContext) -> TaskContext:
        context = copy(context)
        sys.stdout.write(f"running Pipe {self.action_or_pipe.metadata.target.__name__} ...")
        try:
            self.instance: Pipe = self.instantiate()
            if isinstance(self.instance, Init):
                self.instance.init()
            for node in self.nodes:
                await node.run(context=context)
            if self.accumulator_pipe is not None:
                self.accumulator_pipe.instance.accumulate(data=self.instance.data, accessor=self.bindings.get('pipe_accessor'), options=self.bindings)

            if isinstance(self.instance, Destroy):
                self.instance.destroy()
            del self.instance
            return context
        except Exception as e:
            print(f"error running Pipe {self.action_or_pipe.metadata.target.__name__}")


class ActionPlaybookNode(PlaybookNode[Action]):
    async def run(self, context: TaskContext) -> TaskContext:
        context = copy(context)
        print(f"running action {self.action_or_pipe.metadata.target.__name__} ...")
        self.instance = self.instantiate()

        if isinstance(self.instance, Init):
            self.instance.init()
        await self.instance.run(context=context, options=self.bindings)

        for node in self.nodes:
            await node.run(context=context)
        print(f"completed action {self.action_or_pipe.metadata.target.__name__}")

        if isinstance(self.instance, Destroy):
            self.instance.destroy()
        del self.instance
        return context


TaskPlaybook = List[PlaybookNode]
