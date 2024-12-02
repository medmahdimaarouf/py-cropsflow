from typing import Optional

from .metadata import *

# Constants to simulate the Injection Keys
INJECT_CONSTRUCTOR_DEPENDENCY_KEY = "__inject_constructor_dependencies__"
INJECT_PROPERTY_DEPENDENCY_KEY = "__inject_property_dependencies__"
INJECT_METHOD_DEPENDENCY_KEY = "__inject_method_dependencies__"


def inject(token: Optional[InjectionToken] = None, scope: Optional[InjectionScope] = None):
    """
    Inject decorator for properties, methods, and constructor parameters.
    """

    def decorator(target: object, key: Optional[str] = None, index: Optional[int] = None):
        # Handle method parameter injection
        if key and index is not None:
            param_types = target.__annotations__.get(key, None)
            method_dependencies = getattr(target, INJECT_METHOD_DEPENDENCY_KEY, {})
            method_dependencies[index] = InjectMetaData(
                type="inject",
                token=token or param_types,
                scope=scope,
                ctr=target.__class__
            )
            setattr(target, INJECT_METHOD_DEPENDENCY_KEY, method_dependencies)
        elif key:
            # Handle property injection
            property_dependencies = getattr(target, INJECT_PROPERTY_DEPENDENCY_KEY, {})
            property_dependencies[key] = InjectMetaData(
                type="inject",
                token=token or target.__annotations__.get(key),
                scope=scope,
                ctr=target.__class__
            )
            setattr(target, INJECT_PROPERTY_DEPENDENCY_KEY, property_dependencies)
        else:
            # Handle constructor parameter injection
            if isinstance(target, type):
                param_types = getattr(target, "__annotations__", {})
                constructor_dependencies = getattr(target, INJECT_CONSTRUCTOR_DEPENDENCY_KEY, {})
                constructor_dependencies[index] = InjectMetaData(
                    type="inject",
                    token=token or param_types.get(index),
                    scope=scope,
                    ctr=target
                )
                setattr(target, INJECT_CONSTRUCTOR_DEPENDENCY_KEY, constructor_dependencies)

        return target

    return decorator
