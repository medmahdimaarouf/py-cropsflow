import inspect
from typing import Any, Type, Dict

from cropsflow.common.abstracts import Init

from cropsflow.common.decorators import InjectionScope, service, ModuleDef
from cropsflow.common.utils import InjectionToken
from .injector import Container
from .injector.module import Module
from .scanner.metadata_scanner import scanServiceMetaData


@service(scope=InjectionScope.DEFAULT)
class Application(Container):
    def __init__(self, args: list[str] = []):
        super().__init__(metadata=scanServiceMetaData(Application), instance=self, host=None)
        self.args = args
        self.modules: Dict[InjectionToken, Module] = {}
        self.tasks: Dict[InjectionToken, Any] = {}
        self.global_modules: Dict[InjectionToken, Module] = {}
        from .scanner.dependency_scanner import DependenciesScanner
        self.scanner: DependenciesScanner = DependenciesScanner(app=self)
        self.register_core_provider(token=Application, instance=self)

    def get_orchestrator(self) -> 'Orchestrator':
        from cropsflow.orchestrator.orchestrator import Orchestrator
        return self.get(token=Orchestrator).resolve(scope=InjectionScope.DEFAULT, optional=True)

    def get_monitor(self):
        from cropsflow.monitoring import Monitor
        return self.get(token=Monitor).resolve(scope=InjectionScope.DEFAULT, optional=True)

    def get_data_sources(self):
        from cropsflow.data import DataSourcesRegister
        return self.get(token=DataSourcesRegister).resolve(scope=InjectionScope.DEFAULT, optional=True)

    def get_module(self, meta_type: Type[Any]) -> Container:
        return self.modules.get(meta_type)

    def get_task(self, token: Type[Any]) -> Container:
        return self.tasks.get(token)

    async def initialize_modules(self) -> None:
        for module in self.modules.values():
            instance: Init = module.get().resolve()
            if issubclass(type(instance), Init):
                try:
                    deps = module.injector.resolve_class_method_deps(module.metadata.target, instance.init)
                    await instance.init(**deps)
                    print('initialized module : ', module.get_name())
                except Exception as e:
                    print(inspect.getfile(module.metadata.target))
                    print(f"Error initializing module {module.metadata.target.__name__} : {str(e)}", file=sys.stderr)
                    # print_traceback()
                    raise e

    def resolve_dependencies(self) -> None:
        for module in self.modules.values():
            for dep in module.deps.values():
                dep.injector.resolve(scope=InjectionScope.DEFAULT)
                dep.injector.resolve(scope=InjectionScope.DEFAULT)

    async def bootstrap(self, module: ModuleDef, overrides: list[any] = None):
        self.scanner.scan_modules(dep=module, overrides=overrides or [])
        self.scanner.scan_edges()
        self.scanner.bind_edges()
        self.resolve_dependencies()
        await self.initialize_modules()
