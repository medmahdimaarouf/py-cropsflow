from ..abstracts import Pipe
from ..decorators import pipe
from ..models import DataModel


@pipe(selector="set")
class DataSetPipe(Pipe):

    def accumulate(self, data: DataModel) -> None:
        pass
