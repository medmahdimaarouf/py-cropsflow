from typing import Dict, Any, Set

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe


@pipe(selector="set")
class SetPipe(Pipe[Set]):

    def __init__(self):
        super().__init__(data=set[any]())

    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: any = None,
                   accessor: str = None) -> None:
        self.get_data().add(data)
