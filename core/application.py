import uuid
from typing import Dict, Any, Type
from common.utils import InjectionToken
from core.injector.container import Container
from core.injector.injector import Injector
from core.injector.module import Module
from common.decorators import InjectionScope, Service


@Service(scope=InjectionScope.DEFAULT)
class Application:

    def __init__(self):
        pass#self.container.register(Application, self)

    def group(self, path: str):
        pass

    def groups(self, path: str):
        pass

    def module(self, meta_type: Type[Any]):
        pass

    def get(self, token: InjectionToken) -> Injector:
        if token is not None:
            return self.container.get(token)
        else:
            raise f'Could not find dependency with token: {token}'
