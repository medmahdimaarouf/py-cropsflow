from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, Generic

from .task_context import TaskContext

C = TypeVar('C', bound=TaskContext)


class Action(Generic[C], ABC):

    @abstractmethod
    async def run(self, context: C, options: Dict[str, Any] = {}) -> TaskContext:
        pass

    async def next(self, context: TaskContext = None) -> None:
        if self.next_callback is not None:
            return await self.next_callback(context)
        else:
            return context
