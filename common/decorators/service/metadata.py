from typing import Type, Any

from common.schemas import DecoratorMetaData
from ..inject import InjectionScope


class ServiceDecoratorMetaData(DecoratorMetaData):
    scope: InjectionScope

    def __init__(self, target: Type[Any], scope: InjectionScope = None):
        self.target = target
        self.type = "service"
        self.scope = scope
