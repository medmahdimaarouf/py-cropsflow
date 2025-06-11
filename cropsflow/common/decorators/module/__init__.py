from .metdata import *

from ...constants import *


def module(
        declarations: List[Type[Any]] = [],
        imports: List[ModuleDef] = [],
        providers: List[ProviderDef] = [],
        exports: List[InjectionToken] = []) -> Callable:
    """
    This Action decorator
    Parameters:
    selector (str): The selector of the action.
    """

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if MODULE_WATERMARK not in watermarks:
            watermarks.append(MODULE_WATERMARK)
        else:
            raise Exception("Duplicated Module decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)
        setattr(cls, MODULE_DECORATOR_DECLARATIONS_KEY, [_ for _ in declarations if _ is not None])
        setattr(cls, MODULE_DECORATOR_IMPORTS_KEY, [_ for _ in imports if _ is not None])
        setattr(cls, MODULE_DECORATOR_PROVIDERS_KEY, [_ for _ in providers if _ is not None])
        setattr(cls, MODULE_DECORATOR_EXPORTS_KEY, [_ for _ in exports if _ is not None])
        return cls

    return decorator
