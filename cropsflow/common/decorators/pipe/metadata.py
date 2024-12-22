from dataclasses import dataclass, field
from typing import Type, Any

from cropsflow.common.schemas.docorator_metadata import DecoratorMetaData


@dataclass()
class DataPipeDecoratorMetaData(DecoratorMetaData):
    selector: str = field(default_factory=str)

    def __int__(self, target: Type[Any], selector: str):
        self.type = "datapipe"
        self.target = target
        self.selector = selector
