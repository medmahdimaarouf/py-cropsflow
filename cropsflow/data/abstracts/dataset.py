from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union

from cropsflow.common.abstracts.data_model import DataModel

I = TypeVar('I')


class DataSet(Generic[I], ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def get(self, index: I = None) -> Union[DataModel, None]:
        pass

    @abstractmethod
    def find(self, query: dict[any, any]) -> list[DataModel]:
        pass

    @abstractmethod
    def save(self, data: DataModel) -> I:
        pass

    @abstractmethod
    def delete(self, index: I) -> Union[DataModel, None]:
        pass

    @abstractmethod
    def update(self, index: I, data: DataModel) -> Union[DataModel, None]:
        pass
