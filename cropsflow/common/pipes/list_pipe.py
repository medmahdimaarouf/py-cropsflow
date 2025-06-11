from typing import List, Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe


@pipe(selector="list")
class ListPipe(Pipe[List]):

    def __init__(self):
        super().__init__(data=list[any]())

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: any = None,
                   accessor: str = None) -> None:
        self.get_data().append(data)
