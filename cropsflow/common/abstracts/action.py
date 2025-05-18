import asyncio
from abc import ABC, abstractmethod
from asyncio import Task
from typing import Callable, Dict, Any

from .task_context import TaskContext


class Action(ABC):
    nextCallBack: Callable[[TaskContext], Any] = None

    def __init__(self):
        self.nextCallBack = None
        self.task = None
        self.data = None

    @abstractmethod
    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        pass

    async def start(self, context: TaskContext) -> Task:
        if self.task is not None and self.task.cancelled():
            raise 'Action is already running'
        else:
            try:
                self.task: Task = asyncio.create_task[TaskContext](self.run(context))
                return self.task.uncancel()
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
        self.nextCallBack = callback

    def complete(self, context: TaskContext = None):
        self.stop()

    def set_data(self, data: any) -> None:
        self.data = data

    def get_data(self) -> any:
        return self.data

    def jump(self):
        pass
