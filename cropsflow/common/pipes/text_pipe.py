from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe, option


@pipe(selector='text')
@option(key='value', meta_type=str, default=None)
class TextPipe(Pipe):

    def __init__(self):
        super().__init__(data=None)

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: str = None, accessor: str = None) -> None:
        self.set_data(data=options.get(__key='value', default=data))
