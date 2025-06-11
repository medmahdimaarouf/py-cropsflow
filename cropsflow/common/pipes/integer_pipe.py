from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe, option


@pipe(selector='integer')
@option(key='value', meta_type=int, default=None)
class IntegerPipe(Pipe[int]):

    def __init__(self):
        super().__init__(data=None)

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: int = None, accessor: str = None) -> None:
        self.set_data(data=options.get(__key='value', default=data))
