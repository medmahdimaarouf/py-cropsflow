from typing import Any, Type, Dict, List

from cropsflow.common.decorators import InjectionScope, service
from cropsflow.common.services import Monitor
from cropsflow.common.utils import InjectionToken
from .engine import Engine
from .injector import Container, Injector, NULL_INJECTOR
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
        self.engine = Engine(self)
        self.register_core_provider(token=Engine, instance=self.engine)
        self.register_core_provider(token=Monitor, instance=Monitor())

    def get_engine(self):
        return self.engine

    def get_monitor(self) -> Monitor | None:
        injector: Injector = self.get(token=Monitor)
        return None if injector is NULL_INJECTOR else injector.resolve(scope=InjectionScope.DEFAULT, optional=True)

    def module(self, meta_type: Type[Any]) -> Container:
        return self.modules.get(meta_type)

    def get_task(self, meta_type: Type[Any]) -> Container:
        return self.tasks.get(meta_type)
