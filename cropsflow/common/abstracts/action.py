"""
action.py

Defines the abstract base class `Action` used in the task execution framework.

This class serves as a contract for creating asynchronous actions that operate
on a given `TaskContext`, potentially modify it, and optionally trigger a next
step in the execution chain.

Classes:
    Action: Abstract base class for task actions, requiring an async `run` method.

Type Parameters:
    C (TaskContext): A subclass of TaskContext that the action will operate on.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, Generic

from .task_context import TaskContext

C = TypeVar('C', bound=TaskContext)


class Action(Generic[C], ABC):
    """
    Abstract base class for all actions within a task execution framework.

    This class defines a standard interface for actions that operate on a `TaskContext`
    and optionally support transitioning to the next step via a callback.

    Methods:
        run(context: C, options: Dict[str, Any]) -> TaskContext:
            Must be implemented by subclasses to perform the core action logic.

        next(context: TaskContext) -> None:
            Triggers the next callback if one is defined.
    """

    @abstractmethod
    async def run(self, context: C, options: Dict[str, Any]) -> TaskContext:
        """
        Execute the action using the provided context and options.

        Args:
            context (C): The execution context for the action.
            options (Dict[str, Any], optional): Additional parameters for the action.

        Returns:
            TaskContext: The updated or new task context after execution.
        """

    async def next(self, context: TaskContext = None) -> TaskContext:
        """
        Execute the next callback, if one is defined, passing along the context.

        Args:
            context (TaskContext, optional): The context to pass to the callback.

        Returns:
            TaskContext: The same context, after optional next callback.
        """
        callback = getattr(self, 'next_callback', None)
        if callback is not None:
            return await callback(context)
        return context
