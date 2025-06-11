from typing import Dict

from .container import Container
from cropsflow.common.decorators import ModuleDecoratorMetaData, ProviderMetaData, TaskDecoratorMetaData, \
    ActionDecoratorMetaData, \
    DataPipeDecoratorMetaData
from cropsflow.common.utils import InjectionToken
from .task import Task


class Module(Container):

    def __init__(self, metadata: ModuleDecoratorMetaData, host: Container = None):
        super().__init__(metadata=metadata, host=host)
        self.imports: Dict[InjectionToken, "Module"] = {}  # Instance-specific initialization
        self.exports: Dict[InjectionToken, Container] = {}  # Instance-specific initialization
        self.is_global: bool = False
        self.exposed: bool = False

    def has_import(self, module: "Module") -> bool:
        return self.imports.get(module.metadata.target) is not None

    def add_import(self, token: InjectionToken, module: "Module"):
        if self.has_import(module):
            raise ValueError(f"Module {self.metadata.target} already has an import for module {module.metadata.token}")
        else:
            self.imports[token] = module

    def register_task(self, metadata: TaskDecoratorMetaData) -> Task:
        if not self.deps.get(metadata.target, None):
            task = Task(metadata=metadata, host=self)
            self.deps[metadata.target] = task
            return task
        else:
            raise Exception(f'Task {metadata.target.__name__} already exists in @Module {self.get_name()}')

    def register_action(self, metadata: ActionDecoratorMetaData) -> Container:
        if not self.deps.get(metadata.target):
            action = Container(metadata=metadata, host=self)
            self.deps[metadata.target] = action
            return action
        else:
            raise Exception(
                f'Action {metadata.target.__name__} already exists in @Module {self.get_name()}')

    def register_pipe(self, metadata: DataPipeDecoratorMetaData):
        if self.deps.get(metadata.target) is None:
            self.deps[metadata.target] = Container(metadata=metadata, host=self)
        else:
            raise Exception(
                f'Pipe {metadata.target.__name__} already exists in @Module {self.get_name()}')
