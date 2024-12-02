from common.models import DataModel
from common.abstracts import DataPipe
from common.decorators import PrxPipe


@PrxPipe("list")
class ListDataPipe(DataPipe):

    def accumulate(self, data: DataModel, accessor: str) -> None:
        ## self.data
        pass
