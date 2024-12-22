from abc import ABC, abstractmethod
from typing import Any, Dict

from ..models import DataModel


class Pipe(ABC):
    data: DataModel

    @abstractmethod
    def accumulate(self, data: DataModel, accessor: str = None, options: Dict[str, Any] = {}) -> None:
        pass
