from typing import Any, Type, Dict

from cropsflow.common.decorators import InjectionScope, service
from cropsflow.common.utils import InjectionToken
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
        self.register_core_provider(token=Application, instance=self)
        self.args = args

    def get_orchestrator(self) -> 'Orchestrator':
        from cropsflow.orchestrator.orchestrator import Orchestrator
        return self.get(token=Orchestrator).resolve[Orchestrator](scope=InjectionScope.DEFAULT, optional=True)

    def get_monitor(self):
        from cropsflow.monitoring import Monitor
        return self.get(token=Monitor).resolve[Monitor](scope=InjectionScope.DEFAULT, optional=True)

    def get_data_sources(self):
        from cropsflow.data import DataSourcesRegister
        return self.get(token=DataSourcesRegister).resolve[DataSourcesRegister](scope=InjectionScope.DEFAULT, optional=True)

    def module(self, meta_type: Type[Any]) -> Container:
        return self.modules.get(meta_type)

    def get_task(self, meta_type: Type[Any]) -> Container:
        return self.tasks.get(meta_type)
