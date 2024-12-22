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
    instance: T = None
    container: "BaseContainer"
    resolve_status: ResolveStatus = ResolveStatus.NONE

    @abstractmethod
    def resolve(self, token: InjectionToken = None, scope: InjectionScope = None, optional: bool = False) -> T:
        pass
