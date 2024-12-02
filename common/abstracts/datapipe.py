from abc import ABC, abstractmethod

from common.models import DataModel


class DataPipe(ABC):
    data: DataModel

    @abstractmethod
    def accumulate(self, data: DataModel, accessor: str) -> None:
        pass
