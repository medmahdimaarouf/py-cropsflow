from abc import ABC, abstractmethod
from typing import Any, Dict, TypeVar, Generic

from ..models import DataModel
from .task_context import TaskContext

D = TypeVar('D', bound=DataModel)


class Pipe(Generic[D], ABC):
    data: D

    @abstractmethod
    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: D = None, accessor: str = None) -> None:
        pass

    def set_data(self, data: D) -> None:
        self.data = data
