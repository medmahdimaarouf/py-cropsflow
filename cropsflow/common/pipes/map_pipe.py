"""
Defines a pipe that accumulates key-value pairs into a dictionary.
"""

from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe


@pipe(selector='map')
class MapPipe(Pipe[Dict[str, Any]]):
    """
    Pipe implementation that accumulates data into a dictionary
    using a string accessor as the key.
    """

    def __init__(self):
        super().__init__(data={})

    def accumulate(
            self,
            context: TaskContext,
            data: Any,
            accessor: str,
            options: Dict[str, Any]
    ) -> None:
        """
        Stores data under the specified accessor key in the internal dictionary.

        Args:
            context (TaskContext): The task execution context.
            data (Any): The value to store.
            accessor (str): The key under which the data will be stored.
            options (Dict[str, Any]): Additional pipe options (unused).

        Raises:
            Exception: If the accessor is None or an empty string.
        """
        if accessor:
            self.get_data().setdefault(accessor, data)
        else:
            raise ValueError("MapPipe requires a non-empty string accessor.")
