from common.models import DataModel
from common.abstracts import Pipe
from common.decorators import pipe


@pipe(selector="list")
class ListPipe(Pipe):

    def accumulate(self, data: DataModel, accessor: str) -> None:
        ## self.data
        pass
