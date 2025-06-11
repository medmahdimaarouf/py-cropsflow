from typing import TypeVar, Generic

from cropsflow.common.utils import InjectionToken
from ..injector.container import Container

T = TypeVar('T', bound=Container)


class DependencyWrap(Generic[T]):

    def __init__(self, token: InjectionToken, container: T, resolved: bool = False, inserted: bool = False,
                 bound: bool = False):
        self.token: InjectionToken = token
        self.dep: T = container
        self.resolved: bool = resolved
        self.inserted: bool = inserted
        self.bound: bool = bound
