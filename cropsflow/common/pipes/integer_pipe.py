"""
Provides the IntegerPipe class, which extracts and sets an integer value
from options or fallback data within a task context.
"""

from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..abstracts.pipe import D
from ..decorators import pipe, option


@pipe(selector='integer')
@option(key='value', meta_type=int, default=None)
class IntegerPipe(Pipe[int]):
    """
    Pipe implementation that processes an integer value.

    Attributes:
        data (int): The extracted or fallback integer value.
    """

    def __init__(self):
        super().__init__(data=None)

    def transform(self, data: any = None, options: Dict[str, Any] = None) -> None:
        """
        Accumulates an integer value from options or falls back to provided data.

        Args:
            context (TaskContext): The task execution context.
            options (Dict[str, Any]): Options including a 'value' key for input.
            data (int, optional): Fallback data if 'value' is not in options.
            accessor (str, optional): Not used in this implementation.
        """
        self._data = options.get('value', data)
