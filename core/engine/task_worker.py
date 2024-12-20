import uuid
from abc import abstractmethod, ABC
from dataclasses import field, dataclass
from typing import Generic, TypeVar, List, Dict, Any

from ..injector import TaskPlaybookItem, Injector, TaskPlaybook, Task

from common.abstracts import Action, Pipe, Init
from common.decorators import InjectionScope

T = TypeVar('T')


class WorkerTreeNode(Generic[T], ABC):
    playbook_item: TaskPlaybookItem
    nodes: List["WorkerTreeNode"]

    def __int__(self, playbook_item: TaskPlaybookItem, parent: "WorkerTreeNode" = None):
        self.playbook_item = playbook_item
        self.nodes = []

    @abstractmethod
    def run(self):
        pass

    def instantiate(self) -> T:
        return self.injector.resolve(scope=InjectionScope.TRANSIENT, optional=False)

    @abstractmethod
    def add_node(self, playbook_item: TaskPlaybookItem):
        pass


class ActionWorkerNode(WorkerTreeNode[Action]):
    def __init__(self, action: Action):
        super().__init__(action)

    async def run(self):
        instance: Action = self.instantiate()
        if isinstance(instance, Init):
            instance.init()
        print("Running ActionWorkerNode ")
        await instance.run(context=None)


class PipeWorkerNode(WorkerTreeNode[Pipe]):
    def __init__(self, pipe: Pipe):
        super().__init__(pipe)

    async def run(self):
        instance: Pipe = self.instantiate()
        if isinstance(instance, Init):
            instance.init()
        print("Running ActionWorkerNode ")
        await instance.accumulate()


class TaskWorker:
    task: Task

    def __init__(self, task: Task):
        self.task = task

    async def run(self):
        playbook: TaskPlaybook = self.task.template.playbook
