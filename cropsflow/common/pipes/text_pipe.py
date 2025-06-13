"""
Pipe that processes and sets text data.
"""

from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe, option


@pipe(selector='text')
@option(key='value', meta_type=str, default=None)
class TextPipe(Pipe[str]):
    """
    Pipe that sets its data to the given text value, either from options or direct data input.
    """

    def __init__(self):
        super().__init__(data=None)

    def accumulate(
            self,
            context: TaskContext,
            options: Dict[str, Any],
            data: str = None,
            accessor: str = None
    ) -> None:
        self._data = options.get('value', data)
