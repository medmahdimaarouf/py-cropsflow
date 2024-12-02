from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, Any

from common.utils import InjectionToken


class Scope(Enum):
    DEFAULT = 0
    TRANSIENT = 1
    REQUEST = 2


@dataclass
class InjectionScope:
    scope: Scope
    optional: bool
    skip_self: bool


class Scope:
    DEFAULT = 0
    TRANSIENT = 1
    REQUEST = 2


class InjectionScope:
    def __init__(self, scope: int = Scope.DEFAULT, optional: bool = False, skip_self: bool = False):
        self.scope = scope
        self.optional = optional
        self.skip_self = skip_self


class InjectMetaData:
    def __init__(self, type: str, token: Optional[InjectionToken], scope: Optional[InjectionScope], ctr: Type):
        self.type = type
        self.token = token
        self.scope = scope
        self.ctr = ctr
