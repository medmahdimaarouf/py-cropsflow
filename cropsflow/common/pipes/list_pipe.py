"""
Defines a pipe that accumulates values into a list within the task context.
"""

from typing import List, Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe


@pipe(selector="list")
class ListPipe(Pipe[List[Any]]):
    """
    Pipe implementation that collects values into a list.
    """

    def __init__(self):
        super().__init__(data=[])

    def accumulate(
            self,
            context: TaskContext,
            options: Dict[str, Any],
            data: Any = None,
            accessor: str = None
    ) -> None:
        """
        Appends data to the internal list.

        Args:
            context (TaskContext): Task execution context.
            options (Dict[str, Any]): Unused in this implementation.
            data (Any): The value to append.
            accessor (str, optional): Unused in this implementation.
        """
        self.get_data().append(data)
