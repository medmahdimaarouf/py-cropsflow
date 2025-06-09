from abc import ABC, abstractmethod
from typing import Any, Dict, TypeVar, Generic, Optional

from .task_context import TaskContext

D = TypeVar('D')


class Pipe(Generic[D], ABC):
    data: Optional[D] = None

    def __init__(self):
        self.data = None

    @abstractmethod
    def accumulate(self, context: TaskContext, options: Dict[str, Any] = {}, data: D = None, accessor: str = None) -> None:
        pass

    def set_data(self, data: D) -> None:
        self.data = data
