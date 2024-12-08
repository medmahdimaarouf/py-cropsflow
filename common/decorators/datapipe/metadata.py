from typing import Type, Any

from common.schemas.docorator_metadata import DecoratorMetaData


class DataPipeDecoratorMetaData(DecoratorMetaData):
    selector: str
    type = "datapipe"

    def __int__(self, target: Type[Any], selector: str):
        self.target = target
        self.selector = selector
