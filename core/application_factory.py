from typing import Type, Any

from core.injector import load_dependencies
from core.injector.container import Container
from core.injector.resolve_status import ResolveStatus
from core.inspector import Inspector
from core.scanner.dependency_scanner import DependencyScanner
from common.decorators import InjectionScope
from common.abstracts import Init


class ApplicationFactory:
    inspector: Inspector = Inspector()
    scanner: DependencyScanner = DependencyScanner(inspector)
    container: Container

    def __init__(self):
        self.container = Container()
        self.inspector = Inspector()
        self.scanner = DependencyScanner(self.inspector)

    def init(self, t: Type[Any]):
        try:
            print("Initializing ...")
            self.scanner.scan(t)
            print('Modules initializing...')
            self._initialize_modules()
            print('Building tasks ...')
        except Exception as e:
            print(str(e))

    def _initialize_modules(self):
        load_dependencies(self.inspector)
        for module in self.inspector.modules.values():
            instance: Init = module.get().resolve()
            if issubclass(type(instance), Init):
                instance.init()
