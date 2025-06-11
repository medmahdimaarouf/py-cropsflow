from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, Generic

from .task_context import TaskContext

C = TypeVar('C', bound=TaskContext)


class Action(Generic[C], ABC):
    """
    Abstract base class for all actions within a task execution framework.

    This class defines a standard interface for actions that operate on a `TaskContext`
    and produce a modified or new `TaskContext` as a result. It also optionally supports
    transitioning to the next step via a callback.

    Type Parameters:
        C (TaskContext): A subclass of TaskContext that defines the specific context type
                         this action operates on.

    Methods:
        run(context: C, options: Dict[str, Any]) -> TaskContext:
            Abstract method that must be implemented by subclasses to define the action's behavior.

        next(context: TaskContext) -> None:
            Optional method that triggers the next callback, if defined, with the given context.
    """

    @abstractmethod
    async def run(self, context: C, options: Dict[str, Any] = {}) -> TaskContext:
        """
        Execute the action using the provided context and options.

        Args:
            context (C): The execution context for the action.
            options (Dict[str, Any], optional): Additional parameters for the action.

        Returns:
            TaskContext: The updated or new task context after execution.
        """
        pass

    async def next(self, context: TaskContext = None) -> None:
        """
        Execute the next callback, if one is defined, passing along the context.

        Args:
            context (TaskContext, optional): The context to pass to the callback. Defaults to None.

        Returns:
            None
        """
        callback = getattr(self, 'next_callback', None)
        if callback is not None:
            return await callback(context)
        return context
