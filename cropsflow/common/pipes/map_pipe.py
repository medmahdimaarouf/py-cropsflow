"""
Defines a pipe that accumulates key-value pairs into a dictionary.
"""

from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe, option


# todo: pipe key should be validated by playbook not data transformation emitter

@pipe(selector='map')
@option(key='key', default='key', required=False)
class MapPipe(Pipe[Dict[str, Any]]):
    """
    Pipe implementation that accumulates data into a dictionary
    using a string accessor as the key.
    """

    def __init__(self):
        super().__init__(data={})

    def transform(self, data: any = None, options: Dict[str, Any] = None) -> None:
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
        key: str = options.get('key', None)
        if key:
            self._data.setdefault(key, data)
        else:
            raise ValueError("MapPipe requires a non-empty string field key.")
