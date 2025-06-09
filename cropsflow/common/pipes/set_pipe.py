from typing import Dict, Any, Set

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe


@pipe(selector="set")
class SetPipe(Pipe[Set]):

    def __init__(self):
        self.set_data(data=set[any]())

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: any = None, accessor: str = None) -> None:
        self.data.add(data)
