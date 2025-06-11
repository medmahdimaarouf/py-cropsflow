from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic

from cropsflow.common.decorators import InjectionScope
from cropsflow.common.utils import InjectionToken

T = TypeVar('T')


class ResolveStatus(Enum):
    NONE = 0
    PENDING = 1
    RESOLVED = 2
    ERROR = 3


class BaseInjector(Generic[T], ABC):

    def __init__(self, container: "BaseContainer", instance: T = None):
        self.container = container
        self.instance = instance
        self.resolve_status: ResolveStatus = ResolveStatus.NONE if not self.instance else ResolveStatus.RESOLVED

    @abstractmethod
    def resolve(self, token: InjectionToken = None, scope: InjectionScope = None, optional: bool = False) -> T:
        pass
