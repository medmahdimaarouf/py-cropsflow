"""
This module defines the TaskContext class, which encapsulates the execution context of a task.

TaskContext manages hierarchical relationships between tasks through an optional parent context,
provides a logger instance for recording task-related events, and holds arbitrary data relevant
to the task's execution. This design facilitates structured task management and logging in complex
systems where tasks may be nested or require shared contextual information.

Attributes:
    parent (Optional[TaskContext]): Reference to the parent task context, if any.
    logger (Optional[Logger]): Logger instance for logging within the task's scope.
    data (Any): Arbitrary data associated with the task, allowing flexible usage.
"""

from typing import Optional, Any
from .logger import Logger


class TaskContext:
    """
    Represents the execution context of a task, holding references to its parent context,
    logger, and any associated data.

    Attributes:
        parent (Optional[TaskContext]): An optional parent context for hierarchical task management.
        logger (Optional[Logger]): Logger instance for tracking task logs.
        data (Any): A flexible field to hold any data relevant to the task.
    """

    def __init__(
            self,
            parent: Optional['TaskContext'] = None,
            logger: Optional[Logger] = None
    ):
        """
        Initialize a TaskContext instance.

        Args:
            parent (Optional[TaskContext]): Optional parent task context.
            logger (Optional[Logger]): Optional logger to use within the task context.
        """
        self.parent: Optional['TaskContext'] = parent
        self.data: Any = None
        self.logger: Optional[Logger] = logger
