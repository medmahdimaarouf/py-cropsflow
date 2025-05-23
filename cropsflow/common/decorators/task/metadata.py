from dataclasses import dataclass, field
from typing import Type, Any

from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass()
class TaskDecoratorMetaData(DecoratorMetaData):
    template: str = field(default_factory=str)
    type = DecoratorMetaDataType.TASK
