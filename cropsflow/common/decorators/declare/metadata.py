from dataclasses import dataclass, field
from typing import Type

from ...utils import InjectionToken
from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass()
class DeclarationDecoratorMetaData(DecoratorMetaData):
    type = DecoratorMetaDataType.ACTION
    token: InjectionToken = field(default=None)
    dependency: Type[any] = field(default=None)
    export: bool = field(default=False)
