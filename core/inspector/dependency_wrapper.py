from typing import TypeVar, Generic

from common.utils import InjectionToken
from ..injector.container import Container

T = TypeVar('T', bound=Container)


class DependencyWrap(Generic[T]):
    dep: T
    token: InjectionToken
    resolved: bool
    inserted: bool
    bound: bool

    def __init__(self, token: InjectionToken, container: T, resolved: bool = False, inserted: bool = False,
                 bound: bool = False):
        self.token = token
        self.dep = container
        self.resolved = resolved
        self.inserted = inserted
        self.bound = bound
