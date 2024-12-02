import json
from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional, Any

# Define a type variable
T = TypeVar('T')
R = TypeVar('R')


class DataModel(Generic[T], ABC):
    def __init__(self, value: T):
        self.value = value

    def __str__(self) -> str:
        return json.dumps(self.value)

    @abstractmethod
    def serialize(self) -> Optional[R]:
        """Abstract method to serialize the data model."""
        pass
