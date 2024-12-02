from .option_metadata import ActionOptionMetaData
from typing import Dict

from common.schemas.docorator_metadata import DecoratorMetaData


class ActionDecoratorMetaData(DecoratorMetaData):
    selector: str
    options: Dict[str, ActionOptionMetaData]

    def __int__(self, selector: str, options: Dict[str, ActionOptionMetaData] = {}):
        self.type = "action"
