from dataclasses import dataclass, field
from typing import Type, Any

from ...schemas import DecoratorMetaData
from ..inject import InjectionScope


@dataclass()
class ServiceDecoratorMetaData(DecoratorMetaData):
    scope: InjectionScope = field(default_factory=InjectionScope)

    def __init__(self, target: Type[Any], scope: InjectionScope = None):
        self.target = target
        self.type = "service"
        self.scope = scope
