from typing import Any, Type

from common.decorators import InjectionScope, service
from common.utils import InjectionToken
from core.injector.container import Container
from core.injector.injector import Injector
from .scanner.metadata_scanner import scanServiceMetaData


@service(scope=InjectionScope.DEFAULT)
class Application:
    container: Container

    def __init__(self):
        self.container = Container(metadata=scanServiceMetaData(Application), instance=self, host=None)

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
