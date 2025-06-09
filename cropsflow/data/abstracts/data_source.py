from abc import ABC, abstractmethod
from typing import Generic, Dict, TypeVar, Union

from .dataset import DataSet

D = TypeVar('D', bound=DataSet)


class DataSource(Generic[D], ABC):
    connected: bool = False

    @abstractmethod
    def connect(self, **args) -> None:
        pass

    @abstractmethod
    def disconnect(self, **args) -> None:
        pass

    @abstractmethod
    def get_dataset(self, name: str) -> Union[D, None]:
        pass

    @abstractmethod
    def get_datasets(self) -> Dict[str, D]:
        pass

    @abstractmethod
    def create_dataset(self, name: str) -> D:
        pass

    @abstractmethod
    def delete_dataset(self, name: str) -> bool:
        pass
