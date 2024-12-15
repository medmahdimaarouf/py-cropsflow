from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Type, Any

from common.utils import InjectionToken


class InjectionScope(Enum):
    DEFAULT = 0
    TRANSIENT = 1


@dataclass
class InjectMetaData:
    scope: InjectionScope = field(default_factory=InjectionScope)
    optional: bool = field(default_factory=bool)
    skip_self: bool = field(default_factory=bool)
    token: InjectionToken = field(default_factory=str)

    def __init__(self, token: InjectionToken = None, scope: InjectionScope = InjectionScope.DEFAULT,
                 optional: bool = False,
                 skip_self: bool = False):
        self.token = token
        self.scope = scope
        self.optional = optional
        self.skip_self = skip_self
