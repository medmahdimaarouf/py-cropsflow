from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe, option


@pipe(selector='decimal')
@option(key='value', meta_type=float, default=None)
class DecimalPipe(Pipe[float]):

    def __init__(self):
        self.set_data(data=None)

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: float = None, accessor: str = None) -> None:
        self.set_data(data=options.get(__key='value', default=data))
