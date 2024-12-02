import asyncio
from abc import ABC, abstractmethod
from asyncio import Task
from typing import Callable

from common.decorators import Option
from .logger import Logger
from .task_context import TaskContext


class Action(ABC):
    label: str = ''
    required: bool = False

    def __init__(self):
        self.nextCallBack = None
        self.task = None

    @Option(label='name', required=False)
    def set_name(self, label: str = 'label'):
        self.label = label

    @Option(label='required', required=False)
    def set_required(self, required: bool = False):
        self.required = required

    @abstractmethod
    async def run(self, context: TaskContext, logger: Logger = None) -> TaskContext:
        pass

    async def start(self, context: TaskContext) -> Task:
        if self.task is not None and self.task.cancelled():
            raise 'Action is already running'
        else:
            try:
                self.task: Task = asyncio.create_task[TaskContext](self.run(context))
                return self.task;
            except asyncio.CancelledError:
                pass

    def stop(self):
        if self.task is None:
            raise Exception("Action is not running to stop")
        elif self.task.cancelled():
            raise Exception("Action is already stopped")
        self.task.stop()

    async def next(self, context: TaskContext = None) -> TaskContext:
        if self.nextCallBack is not None:
            return self.nextCallBack(context)
        else:
            return context

    def setNextCallBack(self, callback: Callable):
        self.nextCallBack = callback;
