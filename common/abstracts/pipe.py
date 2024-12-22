from abc import ABC, abstractmethod
from typing import Any, Dict

from common.decorators import Option
from common.models import DataModel
from ..constants import OPTION_DECORATOR_KEY


class Pipe(ABC):
    data: DataModel

    @abstractmethod
    def accumulate(self, data: DataModel, accessor: str = None, options: Dict[str, Any] = {}) -> None:
        pass
