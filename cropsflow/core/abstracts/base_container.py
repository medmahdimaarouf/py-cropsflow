import uuid
from abc import ABC, abstractmethod
from typing import Generic, Dict, TypeVar, Union

from cropsflow.common.decorators import DecoratorMetaData
from cropsflow.common.utils import InjectionToken
from .base_injector import BaseInjector

T = TypeVar('T')


class BaseContainer(Generic[T], ABC):
    id: str
    injector: "BaseInjector"
    metadata: DecoratorMetaData
    host: "BaseContainer"
    deps: Dict[InjectionToken, "BaseContainer"]
    core_providers: Dict[InjectionToken, any]

    def __init__(self, metadata: DecoratorMetaData, instance: T = None, host: "BaseContainer" = None):
        self.id = str(uuid.uuid4())  # Generate a unique ID for the object
        self.metadata = metadata  # Store the metadata
        self.host = host  # Set the host container
        self.deps = {}  # Instantiate Container
        self.core_providers = {}

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get(self, token: InjectionToken = None) -> BaseInjector[T]:
        pass

    @abstractmethod
    def register(self, token: InjectionToken,
                 dep: Union[object, DecoratorMetaData, "BaseContainer"]) -> "BaseContainer":
        pass

    @abstractmethod
    def get_task(self, token: InjectionToken) -> "Container":
        pass

    @abstractmethod
    def get_action(self, token: InjectionToken = None, selector: str = None) -> "BaseContainer":
        pass

    @abstractmethod
    def get_pipe(self, token: InjectionToken = None, selector: str = None) -> "BaseContainer":
        pass
