import inspect
from typing import Type, Any, Dict, ForwardRef, List, Union

from .metadata_scanner import *
from ..injector.container import Container
from ..injector.module import Module
from ..inspector import Inspector, DependencyWrap
from ..utils import is_function
from common.decorators import DynamicModule, ProviderMetaData, ModuleDef, ServiceDecoratorMetaData, DecoratorMetaData
from common.utils import InjectionToken


class DependencyScanner:
    inspector: Inspector
    container: Container

    def __init__(self, container: Container):
        self.container = container
        self.inspector = Inspector()

    def scan(self, dep: Union[ModuleDef, Type[Any]]):
        self.scan_module(dep)
        self.scan_dependencies()
        self.bind_dependencies()

    async def scan_module(self, module_def: ModuleDef) -> Module:
        if is_function(module_def) or isinstance(module_def, ForwardRef[Any]):
            module_def = await module_def()
        wrap: DependencyWrap[Module] = None
        if isinstance(module_def, DynamicModule):
            wrap = self.inspector.register_module(scanModuleMetaData(module_def.module), dynamic=True,
                                                  is_global=module_def.is_global)
            for provider in module_def.providers if module_def.providers is not None else []:
                wrap.dep.bind_provider(provider)
        else:
            wrap = self.inspector.register_module(scanModuleMetaData(module_def))

        if not wrap.inserted:
            module_metadata: ModuleDecoratorMetaData = wrap.dep.metadata
            for import_def in module_metadata.imports:
                wrap.dep.add_import(self.scan_module(import_def))

        return wrap.dep

    def scan_dependencies(self):
        for module in self.inspector.get_modules():
            metadata: ModuleDecoratorMetaData = module.metadata
            for index, provider in enumerate(metadata.providers):
                if provider is None:
                    raise ValueError(
                        f'None provider in @Module {module.metadata.target.__name__} at position {index}')
                elif isinstance(provider, ProviderMetaData):
                    module.register(provider.provide, provider)
                elif inspect.isclass(provider) and isDecorated(provider, INJECTABLE_WATERMARK):
                    module.register(provider, scanServiceMetaData(provider))
                else:
                    raise TypeError(
                        f'Expected Provider or Service for providers {provider.__name__} in @Module {module.metadata.target.__name__}')

            for index, dec in enumerate(metadata.declarations):
                if dec is None:
                    raise ValueError(
                        f'None declaration in @Module {module.metadata.target.__name__} at position {index}')
                elif not inspect.isclass(dec):
                    raise TypeError(
                        f'Expected class for declaration {dec.__name__} in @Module {module.metadata.target.__name__}')
                elif isDecorated(dec, TASK_WATERMARK):
                    self.inspector.register_task(metadata=scanTaskMetaData(dec), module=module)
                elif isDecorated(dec, ACTION_WATERMARK):
                    self.inspector.register_action(metadata=scanActionMetaData(dec), module=module)
                elif isDecorated(dec, PIPE_WATERMARK):
                    self.inspector.register_pipe(metadata=scanDataPipeMetaData(dec), module=module)
                elif isDecorated(dec, INJECTABLE_WATERMARK):
                    raise ValueError(
                        f'Declaration {dec.__name__} of the @Module {module.metadata.target.__name__} is a Service')
                else:
                    raise ValueError(
                        f'Unknown declaration {dec.__name__} in @Module {module.metadata.target.__name__}')

    def bind_dependencies(self):
        if len(self.inspector.modules):
            self._expose_module()

    def _expose_module(self, module: Module = None):
        module = module if module is not None else next(iter(self.inspector.modules.values()))
        if len(module.imports):
            for imported_module in module.imports.values():
                self._expose_module(imported_module)
                for token, exposed_dep in module.exports.items():
                    if module.exports.get(token) is None:
                        module.exports[token] = exposed_dep
                    else:
                        raise f'Dependency {token} clashes with {module.exports.get(token)} in import {imported_module.metadata.target.__name__}'
        if len(module.exports) and module.is_global:
            for token, dep in module.exports.items():
                self.container.register(token, dep)


'''
    def _scan_module_declaration(self, module: Module):
        for index, dec in enumerate(module.metadata.declarations):

            if dec is None:
                raise ValueError(
                    f'None declaration in @Module {module.metadata.target.__name__} at position {index}')
            elif not inspect.isclass(dec):
                raise TypeError(
                    f'Expected class for declaration {dec.__name__} in @Module {module.metadata.target.__name__}')
            elif isDecorated(dec, ACTION_WATERMARK):
                metadata = scanActionMetaData(dec)
            elif isDecorated(dec, PIPE_WATERMARK):
                metadata = scanDataPipeMetaData(dec)
            elif isDecorated(dec, TASK_WATERMARK):
                metadata = scanTaskMetaData(dec)
            elif isDecorated(dec, INJECTABLE_WATERMARK):
                raise ValueError(
                    f'Declaration {dec.__name__} of the @Module {module.metadata.target.__name__} is a Service')
            else:
                raise ValueError(
                    f'Unknown declaration {dec.__name__} in @Module {module.metadata.target.__name__}')
            module.register(metadata.target, metadata)

    def _scan_task(self, metadata: TaskDecoratorMetaData, module: Module) -> Container:
        return Container(metadata, module)

    def _scan_provider(self, metadata: ProviderMetaData, host: Container):
        host.register(metadata.provide, metadata)

'''
