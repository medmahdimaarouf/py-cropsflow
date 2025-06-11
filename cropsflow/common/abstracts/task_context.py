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
