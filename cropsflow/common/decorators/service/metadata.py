"""
Defines metadata for a Service decorator, used to mark a class as injectable
with a specific scope in the dependency injection system.
"""

from dataclasses import dataclass, field
from typing import Type, Any

from ...schemas import DecoratorMetaData, DecoratorMetaDataType
from ..inject import InjectionScope


@dataclass
class ServiceDecoratorMetaData(DecoratorMetaData):
    """
    Metadata for classes decorated as services (injectables).

    Attributes:
        scope (InjectionScope): The scope in which the service is provided.
        type (DecoratorMetaDataType): Fixed type indicating this is an injectable.
    """
    scope: InjectionScope = field(default=InjectionScope.DEFAULT)
    type: DecoratorMetaDataType = DecoratorMetaDataType.INJECTABLE

    def __init__(self, target: Type[Any], scope: InjectionScope = InjectionScope.DEFAULT):
        self.target = target
        self.scope = scope
