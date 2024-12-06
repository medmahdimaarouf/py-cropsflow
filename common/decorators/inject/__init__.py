from typing import Dict, Union
from common.constants import INJECT_FN_DEPENDENCY_KEY
from .metadata import *

# Constants to simulate the Injection Keys

FnArgInjectionIndex = Union[str, int]


def inject(index: FnArgInjectionIndex, token: InjectionToken = None, scope: InjectionScope = InjectionScope.DEFAULT,
           optional: bool = False,
           skip_self: bool = False):
    """
    Inject decorator for properties, methods, and constructor parameters.
    """

    def decorator(func):
        method_dependencies: Dict[FnArgInjectionIndex, InjectMetaData] = getattr(func, INJECT_FN_DEPENDENCY_KEY, {})
        method_dependencies[index] = InjectMetaData(
            token=token,
            scope=scope,
            optional=optional,
            skip_self=skip_self
        )
        setattr(func, INJECT_FN_DEPENDENCY_KEY, method_dependencies)
        return func

    return decorator
