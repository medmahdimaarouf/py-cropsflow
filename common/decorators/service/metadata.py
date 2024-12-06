from common.schemas import DecoratorMetaData
from ..inject import InjectionMetaData


class ServiceDecoratorMetaData(DecoratorMetaData):
    scope: InjectionMetaData

    def __init__(self, scope: InjectionMetaData = None):
        self.type = "service"
        self.scope = scope
