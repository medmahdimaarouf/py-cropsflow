from typing import Type, Any

from common.schemas import DecoratorMetaData


class TaskDecoratorMetaData(DecoratorMetaData):
    template: str

    def __init__(self, target: Type[Any], template: str):
        self.target = target
        self.type = "service"
        self.template = template
