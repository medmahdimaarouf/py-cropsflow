from typing import Any, Type, Dict

from cropsflow.common.decorators import InjectionScope, service
from cropsflow.common.services import Monitor
from cropsflow.common.utils import InjectionToken
from cropsflow.orchestrator import Orchestrator
from cropsflow.core.injector import Container, Injector
from cropsflow.core.injector.module import Module
from cropsflow.core.scanner.metadata_scanner import scanServiceMetaData


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
        self.register_core_provider(token=Orchestrator, instance=Orchestrator(self))

    def get_orchestrator(self) -> Orchestrator | None:
        injector: Injector = self.get(token=Orchestrator)
        return injector.resolve(scope=InjectionScope.DEFAULT, optional=True)

    def get_monitor(self) -> Monitor | None:
        injector: Injector = self.get(token=Monitor)
        return injector.resolve(scope=InjectionScope.DEFAULT, optional=True)

    def module(self, meta_type: Type[Any]) -> Container:
        return self.modules.get(meta_type)

    def get_task(self, meta_type: Type[Any]) -> Container:
        return self.tasks.get(meta_type)
