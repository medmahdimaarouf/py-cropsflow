from typing import Dict, Any, List

from common.decorators import ModuleDecoratorMetaData, TaskDecoratorMetaData, ActionDecoratorMetaData, \
    DataPipeDecoratorMetaData, ServiceDecoratorMetaData
from common.utils import InjectionToken
from .dependency_wrapper import DependencyWrap
from .tokens_generator import _generate_token
from ..injector.module import Module
from ..injector.container import Container


class Inspector:
    modules: Dict[InjectionToken, Module] = {}
    tasks: Dict[InjectionToken, Any] = {}
    services: Dict[InjectionToken, Any] = {}
    groups: Dict[InjectionToken, Any] = {}
    global_modules: List[Module] = []
    global_tasks: Dict[InjectionToken, Any] = []
    container: Container

    def __init__(self, container: Container):
        self.container = container

    def register_module(self, module_metadata: ModuleDecoratorMetaData, dynamic: bool = False,
                        is_global: bool = False) -> DependencyWrap:
        token = module_metadata.target if not dynamic else _generate_token(module_metadata)
        module = self.modules.get(module_metadata.target)
        exists = module is not None
        if dynamic or not exists:
            module = self.modules[token] = Module(metadata=module_metadata, host=self.container)
            module.is_global = is_global
            if is_global:
                if self.global_modules.get(token) is None:
                    self.global_modules[token] = module
                else:
                    raise Exception(f'Duplicated global module {module.metadata.target.__name__}')

        return DependencyWrap(token=token, container=module, inserted=not exists)

    def get_modules(self, dynamic: bool = None) -> List[Module]:
        if dynamic is None:
            return list(self.modules.values())
        else:
            return [module for token, module in self.modules.items() if token != module.metadata.target == dynamic]

    def register_task(self, metadata: TaskDecoratorMetaData, module: Module = None):
        task = Container(metadata=metadata, host=module)
        if module is not None:
            if module.deps.get(metadata.target) is None:
                module.deps[metadata.target] = task
            else:
                raise Exception(
                    f'Task {metadata.target.__name__} already exists in @Module {module.metadata.target.__name__}')
        self.tasks[metadata.target] = task

    def task(self, token: InjectionToken) -> Any:
        return self.tasks.get(token)

    def register_action(self, metadata: ActionDecoratorMetaData, module: Module):
        if module is not None:
            if module.deps.get(metadata.target) is None:
                module.deps[metadata.target] = Container(metadata=metadata, host=module)
            else:
                raise Exception(
                    f'Action {metadata.target.__name__} already exists in @Module {module.metadata.target.__name__}')

    def register_pipe(self, metadata: DataPipeDecoratorMetaData, module: Module):
        if module is not None:
            if module.deps.get(metadata.target) is None:
                module.deps[metadata.target] = Container(metadata=metadata, host=module)
            else:
                raise Exception(
                    f'Pipe {metadata.target.__name__} already exists in @Module {module.metadata.target.__name__}')
