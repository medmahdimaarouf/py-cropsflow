from abc import ABC, abstractmethod
from typing import TypeVar, Generic

B = TypeVar('B')


class Builder(Generic[B], ABC):
    @abstractmethod
    async def build(self) -> B:
        pass
