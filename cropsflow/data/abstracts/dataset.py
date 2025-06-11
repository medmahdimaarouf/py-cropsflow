from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union, Dict, Optional

I = TypeVar('I')


class DataSet(Generic[I], ABC):

    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def find_one(self, query: dict[any, any]) -> Optional[Dict]:
        pass

    @abstractmethod
    def find_all(self, query: dict[any, any]) -> list[Dict]:
        pass

    @abstractmethod
    def save(self, data: Dict) -> None:
        pass

    @abstractmethod
    def delete(self, index: I) -> None:
        pass

    @abstractmethod
    def update(self, index: I, data: Dict) -> None:
        pass
