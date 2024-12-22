from dataclasses import dataclass, field
from typing import Type, Any

from ...schemas import DecoratorMetaData


@dataclass()
class TaskDecoratorMetaData(DecoratorMetaData):
    template: str = field(default_factory=str)

    def __init__(self, target: Type[Any], template: str):
        self.type = "service"
        self.target = target
        self.template = template
