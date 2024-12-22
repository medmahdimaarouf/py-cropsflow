from dataclasses import dataclass, field
from typing import Type, Any

from cropsflow.common.schemas.docorator_metadata import DecoratorMetaData


@dataclass()
class ActionDecoratorMetaData(DecoratorMetaData):
    selector: str = field(default_factory=dict)

    def __int__(self, target: Type[Any], selector: str):
        self.type = "action"
        self.target = target
        self.selector = selector
