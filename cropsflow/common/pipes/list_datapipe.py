from ..abstracts import Pipe
from ..decorators import pipe
from ..models import DataModel


@pipe(selector="list")
class ListPipe(Pipe):

    def accumulate(self, data: DataModel, accessor: str) -> None:
        pass
