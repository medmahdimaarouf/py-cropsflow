from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, Any

from common.utils import InjectionToken


class InjectionScope(Enum):
    DEFAULT = 0
    TRANSIENT = 1
    REQUEST = 2


@dataclass
class InjectMetaData:
    scope: InjectionScope
    optional: bool
    skip_self: bool
    token: InjectionToken

    def __init__(self, token: InjectionToken = None, scope: InjectionScope = InjectionScope.DEFAULT,
                 optional: bool = False,
                 skip_self: bool = False):
        self.token = token
        self.scope = scope
        self.optional = optional
        self.skip_self = skip_self
