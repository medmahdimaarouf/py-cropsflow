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
from copy import deepcopy
from typing import Dict, Any, TypeVar, Generic, Optional

from .action import Action
from .task_context import TaskContext

C = TypeVar('C', bound=TaskContext)
D = TypeVar('D')


class DataAction(Generic[C, D], Action[C], ABC):
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

    def __init__(self, data: D = None):
        """
        Initialize the pipe with optional initial data.

        Args:
            data (D, optional): The initial data to assign to the pipe.
        """
        self._data: Optional[D] = data

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
    def get_data(self) -> D:
        """
        Retrieve the current internal data of the dataAction.

        Returns:
            D: The stored data.
        """
        return deepcopy(self._data)
