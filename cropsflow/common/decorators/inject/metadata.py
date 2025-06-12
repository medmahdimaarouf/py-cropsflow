"""
This module defines the InjectMetaData dataclass and the InjectionScope enum,
used to describe dependency injection metadata including scope, optionality,
and token information.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ...utils import InjectionToken


class InjectionScope(Enum):
    """
    Enum representing the scope of an injection.

    Attributes:
        DEFAULT: Default singleton scope.
        TRANSIENT: Transient scope, creates a new instance on each injection.
    """
    DEFAULT = 0
    TRANSIENT = 1


@dataclass
class InjectMetaData:
    """
    Metadata for dependency injection configuration.

    Attributes:
        token (Optional[InjectionToken]): The injection token identifying the dependency.
        scope (InjectionScope): The lifecycle scope of the injection.
        optional (bool): Whether the dependency is optional.
        skip_self (bool): Whether to skip self when resolving dependency.
    """

    token: Optional[InjectionToken] = field(default=None)
    scope: InjectionScope = field(default=InjectionScope.DEFAULT)
    optional: bool = field(default=False)
    skip_self: bool = field(default=False)
