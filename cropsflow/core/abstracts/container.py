import uuid
from abc import ABC, abstractmethod
from typing import Generic, Dict, TypeVar, Union

from cropsflow.common.decorators import DecoratorMetaData
from cropsflow.common.utils import InjectionToken
from .injector import BaseInjector

T = TypeVar('T')


class BaseContainer(Generic[T], ABC):

    def __init__(self, metadata: DecoratorMetaData, instance: T = None, host: "BaseContainer" = None):
        self.id: str = str(uuid.uuid4())  # Generate a unique ID for the object
        self.metadata: DecoratorMetaData = metadata  # Store the metadata
        self.host: BaseContainer = host  # Set the host container
        self.deps: Dict[InjectionToken, BaseContainer] = {}  # Instantiate Container
        self.core_providers: Dict[InjectionToken, any] = {}
        self.injector: BaseInjector = None

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
