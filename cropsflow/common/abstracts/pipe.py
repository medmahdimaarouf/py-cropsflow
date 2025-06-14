"""
This module defines the abstract base class `Pipe` for data processing within a task execution framework.

A `Pipe` serves as a generic and reusable component designed to accumulate and manage data throughout
the lifecycle of a task. It provides a standardized interface for processing data via the abstract
`accumulate` method, which must be implemented by subclasses to define specific data aggregation logic.

The pipe can hold an internal data state, which can be set and retrieved via the `set_data` and `get_data`
methods, respectively. This design supports flexible data manipulation patterns in complex workflows,
allowing subclasses to extend and customize how data is accumulated and accessed in different contexts.

Key concepts:
- Generic typing for flexible data types.
- Integration with `TaskContext` for task-specific execution state.
- Optional accessor support for nested or specific data retrieval.

This abstraction is useful in systems that require modular, composable data processing pipelines,
such as workflow engines, ETL processes, or reactive data streams.
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, TypeVar, Generic, Optional

from .task_context import TaskContext

D = TypeVar('D')


class Pipe(Generic[D], ABC):
    """
    Abstract base class representing a data processing pipe.

    A Pipe is a reusable, generic component designed to process and accumulate data
    during a task's lifecycle, with support for setting and retrieving the underlying data.

    Attributes:
        _data (Optional[D]): The internal data carried by the pipe.
    """

    def __init__(self, data: D = None):
        """
        Initialize the pipe with optional initial data.

        Args:
            data (D, optional): The initial data to assign to the pipe.
        """
        self._data: Optional[D] = data

    @abstractmethod
    def transform(self, data: any = None, options: Dict[str, Any] = None) -> None:
        """
        Abstract method to perform accumulation logic.

        This method must be implemented by subclasses to handle specific accumulation logic.

        Args:
            context (TaskContext): The current task execution context.
            options (Dict[str, Any], optional): Additional options for accumulation.
            data (D, optional): Additional data to be considered during accumulation.
            accessor (str, optional): Optional attribute path or key used for accessing sub-data.
        """

    def get_data(self) -> D:
        """
        Retrieve the current internal data of the pipe.

        Returns:
            D: The stored data.
        """
        return deepcopy(self._data)
