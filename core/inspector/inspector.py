from typing import Dict, Any, List

from common.decorators import ModuleDecoratorMetaData, TaskDecoratorMetaData
from common.utils import InjectionToken
from .dependency_wrapper import DependencyWrap
from .tokens_generator import _generate_token
from ..application import Application
from ..injector.module import Module


class Inspector:
    app: Application

    def __init__(self, container: Application):
        self.app = container

    def register_module(self, module_metadata: ModuleDecoratorMetaData, dynamic: bool = False,
                        is_global: bool = False) -> DependencyWrap:
        token = module_metadata.target if not dynamic else _generate_token(module_metadata)
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
