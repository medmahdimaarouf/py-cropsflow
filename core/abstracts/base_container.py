from abc import ABC, abstractmethod
from typing import Generic, Dict, TypeVar, Union

from common.decorators import DecoratorMetaData
from common.utils import InjectionToken
from .base_injector import BaseInjector

T = TypeVar('T')


class BaseContainer(Generic[T], ABC):
    id: str
    injector: "BaseInjector"
    metadata: DecoratorMetaData
    host: "BaseContainer" = None
    deps: Dict[InjectionToken, "BaseContainer"] = {}
    name: str

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
