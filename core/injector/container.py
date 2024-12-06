import uuid
from abc import abstractmethod, ABC
from inspect import isclass
from typing import Any, Dict, Generic, TypeVar
from common.utils import InjectionToken, stringify_injection_token
from common.schemas import DecoratorMetaData
from common.decorators import ProviderMetaData
from .injector import Injector, NULL_INJECTOR
from .resolve_status import ResolveStatus

T = TypeVar('T')


class Container(Generic[T]):
    id: str
    injector: Injector
    metadata: DecoratorMetaData
    host: "Container" = None
    instances: Dict[InjectionToken, Any] = {}
    deps: Dict[InjectionToken, "Container"] = {}
    name: str

    def __init__(self, metadata: DecoratorMetaData = None, host: "Container" = None):
        self.id = str(uuid.uuid4())
        self.metadata = metadata
        self.host = host
        self.injector = Injector(self)

    def isHostedBy(self, host: "Container") -> bool:
        return self.host == host

    def get_name(self):
        if self.metadata is None:
            return "ROOT"
        if isinstance(self.metadata, ProviderMetaData):
            return self.metadata.provide.__name__ if isclass(self.metadata.provide) else self.metadata.provide
        else:
            return self.metadata.target.__name__

    def get(self, token: InjectionToken = None, optional: bool = False) -> Injector[T]:
        if token is None:
            if self.metadata is None:
                raise Exception(f'Null injector found for {stringify_injection_token(token)}')
            else:
                return self.injector
        elif self.deps.get(token) is not None:
            return self.deps.get(token)
        elif self.host is not None:
            return self.host.get(token)
        elif not optional:
            raise Exception(f'Null injector found for {stringify_injection_token(token)} in {self.get_name()}')
        else:
            return NULL_INJECTOR

    def register(self, token: InjectionToken, metadata: DecoratorMetaData) -> "Container":
        if self.deps.get(token) is not None:
            raise ValueError(f"Token {token} already registered.")
        else:
            container = Container(metadata, self)
            self.deps[token] = container
            return container

    def add(self, token: InjectionToken, dep: "Container"):
        if self.deps.get(token) is not None:
            raise ValueError(
                f"Token {stringify_injection_token(token)} already registered in container {self.get_name()}.")
        else:
            self.deps[token] = dep


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
