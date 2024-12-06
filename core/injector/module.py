from typing import Type, Any, Dict

from core.injector.container import Container
from common.decorators import ModuleDecoratorMetaData, ProviderMetaData
from common.utils import InjectionToken
from core.injector.injector import Injector


class Module(Container):
    metadata: ModuleDecoratorMetaData
    imports: Dict[InjectionToken, "Module"] = {}
    exports: Dict[InjectionToken, Container] = {}
    is_global: bool = False

    def __int__(self, metadata: ModuleDecoratorMetaData):
        self.metadata = metadata

    def add_import(self, module: "Module"):
        if self.imports.get(module.metadata.target):
            raise ValueError(f"Module {self.metadata.target} already has an import for module {module.metadata.token}")
        else:
            self.imports[module.id] = module

    def bind_provider(self, provider: ProviderMetaData):
        if self.deps.get(provider.provide) is not None:
            raise ValueError(f"Module {self.metadata.target} already has a provider for token {provider.provide}")
        else:
            self.deps[provider.provide] = Container(provider, self)
