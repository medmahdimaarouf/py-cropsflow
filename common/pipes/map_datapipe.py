from common import DataModel
from common.abstracts import Pipe
from common.decorators import pipe


@pipe(selector="list")
class MapPipe(Pipe):

    def accumulate(self, data: DataModel, accessor: str) -> None:
        pass
