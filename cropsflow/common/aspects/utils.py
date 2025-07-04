import builtins
from inspect import ismethod, isfunction, isbuiltin
from types import MethodType
from typing import Callable, Union, Type, Optional, Any


def get_function_bound(func: Union[MethodType, Callable]) -> Type[any]:
    if ismethod(func) and hasattr(func, '__self__'):
        return func.__self__
    elif isbuiltin(func):
        return builtins
    elif isfunction(func):
        if len(func.__qualname__.split('.')) > 1:
            return getattr(__import__(func.__module__), func.__qualname__.split('.').pop(0))
        else:
            return __import__(func.__module__)
    else:
        return None


def get_wrapped_function(target: Callable) -> Optional[Callable]:
    """Helper to get the current wrapped function (if any)."""
    bound = get_function_bound(target)
    if bound is None:
        raise ValueError(f'Unable to apply aspect on target {str(target)}')
    return getattr(bound, target.__name__, None)


def update_wrapper(bound: Any, target: Callable, wrapper: Callable) -> None:
    """Updates the bound method with the new wrapper."""
    setattr(bound, target.__name__, wrapper)
