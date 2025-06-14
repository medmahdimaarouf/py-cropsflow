"""
Defines a pipe that accumulates unique items into a set.
"""

from typing import Dict, Any, Set

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe


@pipe(selector="set")
class SetPipe(Pipe[Set[Any]]):
    """
    Pipe implementation that collects unique data values into a set.
    """

    def __init__(self):
        super().__init__(data=set())

    def transform(self, data: any = None, options: Dict[str, Any] = None) -> None:
        """
        Adds a unique data value to the set.

        Args:
            context (TaskContext): The task execution context.
            options (Dict[str, Any]): Pipe options (unused).
            data (Any): The data to add to the set.
            accessor (str): Optional accessor (unused).
        """
        self._data.add(data)
