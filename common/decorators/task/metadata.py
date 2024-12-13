from typing import Type, Any

from common.schemas import DecoratorMetaData


class TaskDecoratorMetaData(DecoratorMetaData):
    template: str

    def __init__(self, target: Type[Any], template: str):
        self.type = "service"
        self.target = target
        self.template = template
