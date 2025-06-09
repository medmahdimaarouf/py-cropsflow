from typing import Dict, Any

from ..abstracts import Pipe, TaskContext
from ..decorators import pipe


@pipe(selector='map')
class MapPipe(Pipe[Dict]):

    def __init__(self):
        self.set_data(data=dict[str, any]())

    def accumulate(self, context: TaskContext, data: any, accessor: str, options: Dict[str, Any] = {}, ) -> None:

        if accessor is not None and len(accessor) > 0:
            self.data.setdefault(accessor, data)
        else:
            raise Exception('Map pipe accessor is None expected not empty str ')
