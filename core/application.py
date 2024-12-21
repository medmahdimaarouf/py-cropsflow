from typing import Any, Type, Dict, List

from common.decorators import InjectionScope, service
from common.utils import InjectionToken
from .injector.container import Container
from .injector.module import Module
from .scanner.metadata_scanner import scanServiceMetaData


@service(scope=InjectionScope.DEFAULT)
class Application(Container):
    modules: Dict[InjectionToken, Module] = {}
    tasks: Dict[InjectionToken, Any] = {}
    groups: Dict[InjectionToken, Any] = {}
    global_modules: List[Module] = []

    def __init__(self):
        super().__init__(metadata=scanServiceMetaData(Application), instance=self, host=None)

    def group(self, path: str):
        return self.groups.get(path)

    def module(self, meta_type: Type[Any]) -> Container:
        return self.modules.get(meta_type)

    def task(self, meta_type: Type[Any]) -> Container:
        return self.tasks.get(meta_type)
