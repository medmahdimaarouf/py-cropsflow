from dataclasses import dataclass, field
from typing import Type, Any

from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass()
class DataPipeDecoratorMetaData(DecoratorMetaData):
    selector: str = field(default_factory=str)
    type = DecoratorMetaDataType.DATAPIPE
