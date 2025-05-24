from dataclasses import dataclass, field

from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass()
class ActionDecoratorMetaData(DecoratorMetaData):
    type = DecoratorMetaDataType.ACTION
    selector: str = field(default_factory=dict)
    auto_next: bool = field(default_factory=bool)
