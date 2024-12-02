from common import DataModel
from common.abstracts import DataPipe
from common.decorators import PrxPipe


@PrxPipe("list")
class MapDataPipe(DataPipe):

    def accumulate(self, data: DataModel, accessor: str) -> None:
        pass
