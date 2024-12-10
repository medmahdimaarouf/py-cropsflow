import uuid
from inspect import isclass
from typing import Dict, Generic, TypeVar, Union

from common.decorators import ProviderMetaData, ValueProviderMetaData
from common.schemas import DecoratorMetaData
from common.utils import InjectionToken, stringify_injection_token
from .injector import Injector, NULL_INJECTOR
from ..abstracts.base_container import BaseContainer
from ..abstracts.base_injector import BaseInjector

T = TypeVar('T')


class Container(Generic[T], BaseContainer[T]):
    def __init__(self, metadata: DecoratorMetaData, instance: T = None, host: BaseContainer = None):
        self.id = str(uuid.uuid4())  # Generate a unique ID for the object
        self.injector = Injector(self, instance=instance)  # Initialize the injector
        self.metadata = metadata  # Store the metadata
        self.host = host  # Set the host container
        # Initialize the deps dictionary with Injector as the key and Container as the value
        self.deps = {}  # Instantiate Container
        # self.register_core_providers()

    def get_name(self):
        if isinstance(self.metadata, ProviderMetaData):
            return self.metadata.provide.__name__ if isclass(self.metadata.provide) else self.metadata.provide
        else:
            return self.metadata.target.__name__

    def get(self, token: InjectionToken = None) -> BaseInjector[T]:
        if token is None or token is Injector:
            return self.injector
        elif self.deps.get(token) is not None:
            return self.deps.get(token).injector
        elif self.host is not None:
            return self.host.get(token)
        else:
            return NULL_INJECTOR

    def register(self, token: InjectionToken, dep: Union[object, DecoratorMetaData, BaseContainer]) -> BaseContainer:
        if self.deps.get(token) is not None:
            raise ValueError(
                f"Token {stringify_injection_token(token)} already registered in container {self.get_name()}.")
        elif isinstance(dep, DecoratorMetaData) or isinstance(dep, ProviderMetaData):
            container = Container(metadata=dep, host=self)
            self.deps[token] = container
            return container
        elif isinstance(dep, BaseContainer):
            self.deps[token] = dep
        else:
            mutable_container: Container = Container(host=self, instance=dep)
            self.deps[token] = mutable_container

    def register_core_providers(self):
        self.register(token=Injector, dep=ValueProviderMetaData(provide=Injector, use_value=self.injector))


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
