from abc import ABC, abstractmethod
from typing import Any, Dict, TypeVar, Generic, Optional

from .task_context import TaskContext

D = TypeVar('D')


class Pipe(Generic[D], ABC):
    """
    Abstract base class representing a data processing pipe.

    A Pipe is a reusable, generic component designed to process and accumulate data
    during a task's lifecycle, with support for setting and retrieving the underlying data.

    Attributes:
        data (Optional[D]): The internal data carried by the pipe.
    """

    def __init__(self, data: D = None):
        """
        Initialize the pipe with optional initial data.

        Args:
            data (D, optional): The initial data to assign to the pipe.
        """
        self.data: Optional[D] = data

    @abstractmethod
    def accumulate(
            self,
            context: TaskContext,
            options: Dict[str, Any] = {},
            data: D = None,
            accessor: str = None
    ) -> None:
        """
        Abstract method to perform accumulation logic.

        This method must be implemented by subclasses to handle specific accumulation logic.

        Args:
            context (TaskContext): The current task execution context.
            options (Dict[str, Any], optional): Additional options for accumulation.
            data (D, optional): Additional data to be considered during accumulation.
            accessor (str, optional): Optional attribute path or key used for accessing sub-data.
        """
        pass

    def set_data(self, data: D) -> None:
        """
        Set the internal data of the pipe.

        Args:
            data (D): The data to be set.
        """
        self.data = data

    def get_data(self) -> D:
        """
        Retrieve the current internal data of the pipe.

        Returns:
            D: The stored data.
        """
        return self.data
