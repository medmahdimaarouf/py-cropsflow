from common.schemas import DecoratorMetaData
from ..inject import InjectionScope


class ServiceDecoratorMetaData(DecoratorMetaData):
    scope: InjectionScope

    def __init__(self, scope: InjectionScope = None):
        self.type = "service"
        self.scope = scope
