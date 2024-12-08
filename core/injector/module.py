from typing import Type, Any, Dict

from core.injector.container import Container
from common.decorators import ModuleDecoratorMetaData, ProviderMetaData
from common.utils import InjectionToken
from core.injector.injector import Injector


class Module(Container):
    metadata: ModuleDecoratorMetaData
    imports: Dict[InjectionToken, "Module"]
    exports: Dict[InjectionToken, Container]
    is_global: bool
    exposed: bool

    def __init__(self, metadata: ModuleDecoratorMetaData, host: Container = None):
        super().__init__(metadata=metadata, host=host)
        self.imports = {}  # Instance-specific initialization
        self.exports = {}  # Instance-specific initialization
        self.is_global = False
        self.exposed = False

    def is_imports(self, module: "Module") -> bool:
        return self.imports.get(module.metadata.target) is not None

    def add_import(self, token: InjectionToken, module: "Module"):
        if self.is_imports(module):
            raise ValueError(f"Module {self.metadata.target} already has an import for module {module.metadata.token}")
        else:
            self.imports[token] = module

    def bind_provider(self, provider: ProviderMetaData):
        if self.deps.get(provider.provide, None) is not None:
            raise ValueError(f"Module {self.metadata.target} already has a provider for token {provider.provide}")
        else:
            self.deps[provider.provide] = Container(provider, self)
