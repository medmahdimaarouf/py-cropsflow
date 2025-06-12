"""
Defines the DecimalPipe class, a data pipe used to handle floating-point values
within a task context. It extracts and sets a decimal value for downstream actions.
"""

from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe, option


@pipe(selector='decimal')
@option(key='value', meta_type=float, default=None)
class DecimalPipe(Pipe[float]):
    """
    Pipe implementation that provides a float value from options or input data.

    Attributes:
        data (float): The processed float data to be passed along the pipeline.
    """

    def __init__(self):
        super().__init__(data=None)

    def accumulate(
            self,
            context: TaskContext,
            options: Dict[str, Any],
            data: float = None,
            accessor: str = None
    ) -> None:
        """
        Accumulates a float value from options or falls back to provided data.

        Args:
            context (TaskContext): The current execution context.
            options (Dict[str, Any]): Options including a 'value' key for decimal input.
            data (float, optional): Fallback data if 'value' is not in options.
            accessor (str, optional): Unused in this implementation.
        """
        self.set_data(data=options.get('value', data))
