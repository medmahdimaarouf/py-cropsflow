from abc import ABC, abstractmethod
from typing import Any, Dict

from common.decorators import OptionMetaData
from common.models import DataModel
from ..constants import OPTION_DECORATOR_KEY


class Pipe(ABC):
    data: DataModel

    def option(self, name: str, value: Any):
        """Assign values to properties of the instance using tracked metadata."""
        options: Dict[str, OptionMetaData] = getattr(self.__class__, OPTION_DECORATOR_KEY, {})
        option: OptionMetaData = options.get(name.strip(), None)
        if option is not None:
            setattr(self, option.setter_name, value)
        else:
            raise Exception(f"The @option '{name}' is not found in {self.__class__.__name__}")

    def options(self, options: Dict[str, Any]):
        for name, value in options.items():
            self.option(name, value)
    @abstractmethod
    def accumulate(self, data: DataModel, accessor: str) -> None:
        pass
