import inspect
from typing import Union

from common.decorators import DynamicModule, ProviderMetaData, ModuleDef
from common.utils import stringify_injection_token
from .metadata_scanner import *
from ..injector.module import Module
from ..inspector import Inspector, DependencyWrap
from ..utils import is_function
from ..application import Application


class DependencyScanner:
    inspector: Inspector

    def __init__(self, app: Application):
        self.inspector = Inspector(app)

    def scan(self, dep: Union[ModuleDef, Type[Any]]):
        self.scan_module(dep)
        self.scan_dependencies()
        self.bind_dependencies()

    def scan_module(self, module_def: ModuleDef) -> DependencyWrap:
        if is_function(module_def):
            module_def = module_def()
        wrap: DependencyWrap[Module] = None
        if isinstance(module_def, DynamicModule):
            wrap = self.inspector.register_module(scanModuleMetaData(module_def.module), dynamic=True,
                                                  is_global=module_def.is_global)
            for provider in module_def.providers if module_def.providers is not None else []:
                wrap.dep.register_provider(provider)
        else:
            wrap = self.inspector.register_module(scanModuleMetaData(module_def))
        if wrap.inserted:
            module_metadata: ModuleDecoratorMetaData = wrap.dep.metadata
            for import_def in module_metadata.imports:
                if import_def == module_metadata.target:
                    print(f"Skipping self-import for module {module_metadata.target.__name__}")
                    continue
                import_wrapper = self.scan_module(import_def)
                wrap.dep.add_import(token=import_wrapper.token, module=import_wrapper.dep)
        return wrap

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
                    module.register_action(metadata=scanActionMetaData(dec))
                elif isDecorated(dec, PIPE_WATERMARK):
                    module.register_pipe(metadata=scanDataPipeMetaData(dec))
                elif isDecorated(dec, INJECTABLE_WATERMARK):
                    raise ValueError(
                        f'Declaration {dec.__name__} of the @Module {module.metadata.target.__name__} is a Service')
                else:
                    raise ValueError(
                        f'Unknown declaration {dec.__name__} in @Module {module.metadata.target.__name__}')

    def bind_dependencies(self):
        if len(self.inspector.app.modules):
            self._expose_module(next(iter(self.inspector.app.modules.values())))

    def _expose_module(self, module: Module):
        if len(module.imports.values()):
            for imported_module in module.imports.values():
                if not imported_module.exposed:
                    self._expose_module(imported_module)
                for token, exposed_dep in imported_module.exports.items():
                    module.register(token=token, dep=exposed_dep)

        if len(module.metadata.exports):
            for token in module.metadata.exports:
                if module.deps.get(token) is not None:
                    module.exports.setdefault(token, module.deps.get(token))
                    if module.is_global:
                        self.container.register(token, module.deps.get(token))
                else:
                    raise Exception(
                        f'Could not export {stringify_injection_token(token)} from {module.get_name()} : dependency not found.')

        module.exposed = True


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
