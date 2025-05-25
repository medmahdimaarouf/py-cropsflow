import inspect
from typing import Union

from cropsflow.common.decorators import DynamicModule, ProviderMetaData, ModuleDef
from cropsflow.common.utils import stringify_injection_token, InjectionToken
from cropsflow.platforms.application import Application
from ..injector.module import Module
from ..scanner.dependency_wrapper import DependencyWrap
from ..scanner.metadata_scanner import *
from ..utils import is_function
from ..utils.tokens_generator import generate_token


class DependenciesScanner:
    app: Application

    def __init__(self, app: Application):
        self.app = app

    def scan_modules(self, dep: Union[ModuleDef, Type[Any]], overrides: list[Union[ModuleDef, Type[Any]]] = []):
        for override in overrides:
            self.scan_module(module_def=override, is_global=True)
        self.scan_module(module_def=dep, is_global=True)

    def scan_module(self, module_def: ModuleDef, is_global: bool = False) -> DependencyWrap:
        if is_function(module_def):
            module_def = module_def()
        wrap: DependencyWrap[Module] = None
        if isinstance(module_def, DynamicModule):
            wrap = self.register_module(module_metadata=scanModuleMetaData(module_def.module), dynamic=True, is_global=is_global or module_def.is_global)
            for provider in module_def.providers if module_def.providers is not None else []:
                wrap.dep.register(token=provider.provide, dep=provider)
        else:
            wrap = self.register_module(module_metadata=scanModuleMetaData(module_def), dynamic=False, is_global=is_global)
        if wrap.inserted:
            module_metadata: ModuleDecoratorMetaData = wrap.dep.metadata
            for import_def in module_metadata.imports:
                if import_def == module_metadata.target:
                    print(f"Skipping self-import for module {module_metadata.target.__name__}")
                    continue
                import_wrapper = self.scan_module(import_def)
                wrap.dep.add_import(token=import_wrapper.token, module=import_wrapper.dep)
        return wrap

    def scan_edges(self):
        for module in self.app.modules.values():
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
                    self.register_task(metadata=scanTaskMetaData(dec), module=module)
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

    def bind_edges(self):
        for module in self.app.modules.values():
            if not module.exposed:
                self._expose_module(module=module)

    def _expose_module(self, module: Module):
        if len(module.imports.values()):
            for imported_module in module.imports.values():
                if not imported_module.exposed:
                    self._expose_module(imported_module)
                for token, exposed_dep in imported_module.exports.items():
                    module.register(token=token, dep=exposed_dep)

        if len(module.metadata.exports):
            for token in module.metadata.exports:
                if module.imports.get(token) is not None:
                    exported_module = module.imports.get(token)
                    for [token, dep] in exported_module.deps.items():
                        module.exports.setdefault(token, dep)
                        if module.is_global:
                            self.app.register(token, dep)
                elif module.deps.get(token) is not None:
                    module.exports.setdefault(token, module.deps.get(token))
                    if module.is_global:
                        self.app.register(token, module.deps.get(token))
                else:
                    raise Exception(
                        f'Could not export {stringify_injection_token(token)} from {module.get_name()} : dependency not found.')

        module.exposed = True

    ################################################################

    def register_module(self, module_metadata: ModuleDecoratorMetaData, dynamic: bool = False,
                        is_global: bool = False) -> DependencyWrap:
        token = module_metadata.target if not dynamic else generate_token(module_metadata)
        module = self.app.modules.get(module_metadata.target)
        exists = module is not None
        if dynamic or not exists:
            module = self.app.modules[token] = Module(metadata=module_metadata, host=self.app)
            module.is_global = is_global
            if is_global:
                if self.app.global_modules.get(token) is None:
                    self.app.global_modules[token] = module
                else:
                    raise Exception(f'Duplicated global module {module.metadata.target.__name__}')

        return DependencyWrap(token=token, container=module, inserted=not exists)

    def get_modules(self, dynamic: bool = None) -> List[Module]:
        if dynamic is None:
            return list(self.app.modules.values())
        else:
            return [module for token, module in self.app.modules.items() if
                    token != module.metadata.target == dynamic]

    def register_task(self, metadata: TaskDecoratorMetaData, module: Module):
        task = module.register_task(metadata=metadata)
        self.app.tasks[metadata.target] = task

    def get_task(self, token: InjectionToken) -> Any:
        return self.app.tasks.get(token)


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
