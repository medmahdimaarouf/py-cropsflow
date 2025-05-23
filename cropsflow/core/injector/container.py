from inspect import isclass
from typing import Generic, TypeVar, Union

from cropsflow.common.decorators import ProviderMetaData, ValueProviderMetaData, DataPipeDecoratorMetaData, \
    ActionDecoratorMetaData, InjectionScope
from ...common.decorators import TaskDecoratorMetaData
from cropsflow.common.schemas import DecoratorMetaData
from cropsflow.common.utils import InjectionToken, stringify_injection_token
from .injector import Injector, NULL_INJECTOR
from ..abstracts.container import BaseContainer
from ..abstracts.injector import BaseInjector

T = TypeVar('T')


class Container(Generic[T], BaseContainer[T]):
    def __init__(self, metadata: DecoratorMetaData, instance: T = None, host: BaseContainer = None):
        super().__init__(metadata=metadata, instance=instance, host=host)
        self.injector = Injector(self, instance=instance)  # Initialize the injector
        self.register_core_provider(token=Injector, instance=self.injector)

    def get_name(self):
        if isinstance(self.metadata, ProviderMetaData):
            return self.metadata.provide.__name__ if isclass(self.metadata.provide) else self.metadata.provide
        else:
            return self.metadata.target.__name__

    def get(self, token: InjectionToken = None) -> BaseInjector[T] | NULL_INJECTOR:
        if token is None:
            return self.injector
        elif token in self.core_providers:
            return Injector(container=self, instance=self.core_providers.get(token))
        elif token in self.deps:
            return self.deps.get(token).injector
        elif self.host is not None:
            return self.host.get(token)
        else:
            return NULL_INJECTOR

    def resolve(self, scope: InjectionScope = None, optional: bool = False):
        return self.injector.resolve(scope=scope, optional=optional)

    def register(self, token: InjectionToken, dep: Union[object, DecoratorMetaData, BaseContainer]) -> BaseContainer:
        if token in self.deps or token in self.core_providers:
            raise ValueError(f"Token {stringify_injection_token(token)} already registered in {self.get_name()}.")
        elif isinstance(dep, DecoratorMetaData) or isinstance(dep, ProviderMetaData):
            container = Container(metadata=dep, host=self)
            self.deps[token] = container
            return container
        elif isinstance(dep, BaseContainer):
            self.deps[token] = dep
        else:
            mutable_container: Container = Container(host=self, instance=dep)
            self.deps[token] = mutable_container

    def get_task(self, token: InjectionToken) -> "Container":
        for t, dep in self.deps.items():
            if isinstance(dep.metadata, TaskDecoratorMetaData) and t == token:
                return dep
        return None if self.host is None else self.host.get_task(token=token)

    def get_action(self, token: InjectionToken = None, selector: str = None) -> "Container":
        for t, dep in self.deps.items():
            if not isinstance(dep.metadata, ActionDecoratorMetaData): continue
            metadata: ActionDecoratorMetaData = dep.metadata
            if t == token or selector == metadata.selector:
                return dep
        return None if self.host is None else self.host.get_action(token=token, selector=selector)

    def get_pipe(self, token: InjectionToken = None, selector: str = None) -> "Container":
        for t, dep in self.deps.items():
            if not isinstance(dep.metadata, DataPipeDecoratorMetaData): continue
            metadata: ActionDecoratorMetaData = dep.metadata
            if t == token or selector == metadata.selector:
                return dep
        return None if self.host is None else self.host.get_pipe(token=token, selector=selector)

    def register_core_provider(self, token: InjectionToken, instance: any):
        self.core_providers.setdefault(token, instance)


'''
        injector: Injector[T] = self.injector if token is None else None
        if token is not None:
            if self.deps.get(token) is not None:
                injector = self.deps.get(token)
            elif self.host is not None:
                injector = self.host.get(token)
        if injector is None and token is None and self.metadata is None:
            raise Exception(f'Null injector found for {stringify_injection_token(token)} in {self.get_name()}')
'''
