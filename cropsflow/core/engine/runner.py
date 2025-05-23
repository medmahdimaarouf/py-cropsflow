import gc
from abc import abstractmethod, ABC
from asyncio import sleep
from collections import deque
from copy import copy
from enum import Enum
from typing import Dict, List, TypeVar, Generic, Callable, Optional, cast

from cropsflow.common import TaskContext, DecoratorMetaDataType, ActionDecoratorMetaData, InjectionScope, Action, Init, Destroy, Pipe, DataModel
from ..injector import Container
from ..utils import BehaviorSubject
from cropsflow.common.constants import PLAYBOOK_ACCUMULATOR_ID_OPTION_KEY, PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY, PLAYBOOK_IS_ASYNC_OPTION_KEY, \
    PLAYBOOK_IS_SKIPPABLE_OPTION_KEY

I = TypeVar('I')
PLAYBOOK_NODES_CORE_OPTIONS_KEYS = [
    PLAYBOOK_ACCUMULATOR_ID_OPTION_KEY,
    PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY,
    PLAYBOOK_IS_ASYNC_OPTION_KEY,
    PLAYBOOK_IS_SKIPPABLE_OPTION_KEY
]


class ERunnerStatus(Enum):
    READY = 'READY',
    RUNNING = 'RUNNING',
    STOPPED = 'STOPPED',
    COMPLETED = 'COMPLETED'


class ERunnerNodeType(Enum):
    ROOT = 'ROOT',
    ACTION = 'ACTION',
    PIPE = 'PIPE'


class RunnerNode:
    parent: 'RunnerNode' = None
    container: Container
    options: Dict[str, any]
    type: ERunnerNodeType
    children: List['RunnerNode'] = []
    file_line: int = 0

    @property
    def shippable(self) -> bool:
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

    def __init__(self, container: Container, options: Dict[str, any] = {}, parent: 'RunnerNode' = None):
        self.container = container
        self.options = options

        if self.container.metadata.type == DecoratorMetaDataType.ACTION:
            self.type = ERunnerNodeType.ACTION
        elif self.container.metadata.type == DecoratorMetaDataType.DATAPIPE:
            self.type = ERunnerNodeType.PIPE
        elif self.container.metadata.type == DecoratorMetaDataType.TASK:
            self.type = ERunnerNodeType.ROOT
        else:
            raise Exception(f'RunnerQueueException: {self.container.get_name()} is not a runnable dependency')

    def append(self, container: Container, options: Dict[str, any] = {}) -> 'RunnerNode':
        node: RunnerNode = RunnerNode(container=container, options=options, parent=self)
        self.children.append(node)
        return node

    def remove(self, container: Container) -> 'RunnerNode':
        self.children = [child for child in self.children if child.container.id != container.id]
        return self


class Runner(Generic[I], ABC):
    parent: 'Runner' = None
    node: RunnerNode
    async_runners: List["Runner"] = []
    sync_runners: deque["Runner"] = deque()
    status: BehaviorSubject[ERunnerStatus] = BehaviorSubject(ERunnerStatus.READY)
    instance: I = None
    context: TaskContext = None
    stopped: bool = False

    def __init__(self, node: RunnerNode, parent: 'Runner' = None):
        self.node = node
        self.parent = parent

    @abstractmethod
    async def run(self, context: TaskContext) -> None:
        pass

    def stop(self):
        self.stopped = True
        for runner in self.sync_runners:
            runner.stop()

    def resume(self):
        self.stopped = False
        for runner in self.sync_runners:
            runner.resume()

    @classmethod
    async def run_queue(self, context: TaskContext) -> None:
        while len(self.sync_runners):
            while self.stopped:
                await sleep(500)
            runner = self.sync_runners.popleft()
            if runner.node.is_async:
                self.async_runners.append(runner)
                runner.run(context=copy(context))
            else:
                await runner.run(context=copy(context))
        gc.collect()

    def init(self, context: TaskContext = None, **args) -> None:
        self.instance = self.node.container.injector.resolve(scope=InjectionScope.DEFAULT, optional=False)
        self.context = context
        if isinstance(self.instance, Init):
            self.instance.init(args)
        for child_node in self.node.children:
            if child_node.type == ERunnerNodeType.ACTION:
                self.sync_runners.append(ActionRunner(node=child_node, parent=self))
            if child_node.type == ERunnerNodeType.PIPE:
                self.sync_runners.append(PipeRunner(node=child_node, parent=self))
        gc.collect()

    def destroy(self, **args) -> None:
        if self.instance is not None and isinstance(self.instance, Destroy) and not self.is_async:
            self.instance.destroy(args)
            del self.instance


class ActionRunner(Runner[Action]):
    async def run(self, context: TaskContext) -> None:
        async def next_callback(ctx: TaskContext) -> None:
            await self.run_queue(context=ctx)

        print(f"running action {self.node.container.get_name()} ...")
        self.init(context=context)
        is_auto_next: bool = cast(ActionDecoratorMetaData, self.node.container.metadata).auto_next
        if not is_auto_next:
            self.instance.next_callback: Callable[[TaskContext], None] = next_callback
        next_context = await self.instance.run(context=copy(context), options=self.node.options)
        if is_auto_next:
            await self.run_queue(context=next_context)
        print(f"completed action {self.node.container.get_name()}")
        self.destroy()


class PipeRunner(Runner[Pipe]):
    accumulator_pipe: 'PipeRunner' = None

    def __init__(self, node: RunnerNode, parent: 'Runner' = None):
        super().__init__(node=node, parent=parent)
        self.accumulator_pipe = self.find_parent_pipe(id=self.node.accumulator_id)
        if self.node.accumulator_id and not self.accumulator_pipe:
            raise Exception(f'Could not locate target accumulator pipe with id {self.node.accumulator_id}')

    def find_parent_pipe(self, id: str = None) -> Optional["PipeRunner"]:
        parent: PipeRunner = self.parent
        while parent:
            parent = parent.parent
            if isinstance(parent, PipeRunner) and (True if id is None else parent.node.options.get("id") == id):
                return parent
        return None

    async def run(self, context: TaskContext) -> None:
        print(f"running pipe {self.node.container.get_name()} ...")
        self.init(context=context)
        await self.run_queue(context=context)
        if self.accumulator_pipe:
            self.accumulator_pipe.accumulate(data=self.instance.data, accessor=self.node.accumulator_accessor)
        self.destroy()
        print(f"completed pipe {self.node.container.get_name()}")

    def accumulate(self, data: DataModel, accessor: str = None):
        self.instance.accumulate(context=self.context, data=data, accessor=accessor, options=self.node.options)


class PlayBookRunner(Runner[object]):

    async def run(self, context: TaskContext) -> None:
        self.init()
        await self.run_queue(context=context)
        self.destroy()
