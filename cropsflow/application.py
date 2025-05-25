from typing import Any, Type, Dict, List

from cropsflow.common.decorators import InjectionScope, service
from cropsflow.common.services import Monitor
from cropsflow.common.utils import InjectionToken
from cropsflow.core.engine import Engine
from cropsflow.core.injector import Container, Injector, NULL_INJECTOR
from cropsflow.core.injector.module import Module
from cropsflow.core.scanner.metadata_scanner import scanServiceMetaData
from cropsflow.events import EventEmitter


@service(scope=InjectionScope.DEFAULT)
class Application(Container):
    modules: Dict[InjectionToken, Module] = {}
    tasks: Dict[InjectionToken, Any] = {}
    groups: Dict[InjectionToken, Any] = {}
    global_modules: Dict[InjectionToken, Module] = {}
    args: list[str] = []

    def __init__(self, args: list[str] = []):
        super().__init__(metadata=scanServiceMetaData(Application), instance=self, host=None)
        self.args = args
        self.register_core_provider(token=Engine, instance=Engine(self))

    def get_engine(self) -> Engine | None:
        injector: Injector = self.get(token=Engine)
        return injector.resolve(scope=InjectionScope.DEFAULT, optional=True)

    def get_monitor(self) -> Monitor | None:
        injector: Injector = self.get(token=Monitor)
        return injector.resolve(scope=InjectionScope.DEFAULT, optional=True)

    def module(self, meta_type: Type[Any]) -> Container:
        return self.modules.get(meta_type)

    def get_task(self, meta_type: Type[Any]) -> Container:
        return self.tasks.get(meta_type)
