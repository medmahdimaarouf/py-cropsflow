from abc import abstractmethod, ABC
from typing import Generic, TypeVar

from ..injector import Task, TaskPlaybook, Injector

from common.abstracts import Action, Pipe, Init
from common.decorators import InjectionScope

T = TypeVar('T')


class WorkerNode(Generic[T], ABC):
    important: bool
    injector: Injector[T]

    def __int__(self, injector: T, important: bool = True, parent: "WorkerNode" = None):
        self.injector = injector
        self.important = important

    @abstractmethod
    def run(self):
        pass

    def instantiate(self) -> T:
        return self.injector.resolve(scope=InjectionScope.TRANSIENT, optional=False)


class ActionWorkerNode(WorkerNode[Action]):
    def __init__(self, action: Action):
        super().__init__(action)

    async def run(self):
        instance: Action = self.instantiate()
        if isinstance(instance, Init):
            instance.init()
        print("Running ActionWorkerNode ")
        await instance.run(context=None)


class PipeWorkerNode(WorkerNode[Pipe]):
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

