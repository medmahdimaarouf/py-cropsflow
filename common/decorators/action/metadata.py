from .option_metadata import ActionOptionMetaData
from typing import Dict, Type, Any

from common.schemas.docorator_metadata import DecoratorMetaData


class ActionDecoratorMetaData(DecoratorMetaData):
    selector: str
    options: Dict[str, ActionOptionMetaData]

    def __int__(self, target: Type[Any], selector: str, options: Dict[str, ActionOptionMetaData] = {}):
        self.type = "action"
        self.target = target
        self.selector = selector
