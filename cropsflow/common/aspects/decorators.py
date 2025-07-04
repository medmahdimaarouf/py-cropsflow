import functools
from typing import Callable, Any, Type, TypeVar, Union

from .utils import get_function_bound, update_wrapper, get_wrapped_function

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


def before(target: Callable) -> Callable[[F], F]:
    """Decorator for before advice (supports multiple aspects)."""

    def decorator(fn: F) -> F:
        fn_ref = get_wrapped_function(target)
        if fn_ref is None:
            raise ValueError(f'Target function not found: {target.__name__}')

        @functools.wraps(fn_ref)
        def wrapper(*args, **kwargs):
            fn(*args, **kwargs)  # Execute the advice first
            return fn_ref(*args, **kwargs)  # Then call the original/wrapped function

        update_wrapper(get_function_bound(target), target, wrapper)
        return fn

    return decorator


def after(target: Callable) -> Callable[[F], F]:
    """Decorator for after advice (supports multiple aspects)."""

    def decorator(fn: F) -> F:
        fn_ref = get_wrapped_function(target)
        if fn_ref is None:
            raise ValueError(f'Target function not found: {target.__name__}')

        @functools.wraps(fn_ref)
        def wrapper(*args, **kwargs):
            return_value = fn_ref(*args, **kwargs)  # Call the original/wrapped function
            fn(*args, **kwargs)  # Execute the advice afterward
            return return_value

        update_wrapper(get_function_bound(target), target, wrapper)
        return fn

    return decorator


def result(target: Callable) -> Callable[[F], F]:
    """Decorator for after advice (supports multiple aspects)."""

    def decorator(fn: F) -> F:
        fn_ref = get_wrapped_function(target)
        if fn_ref is None:
            raise ValueError(f'Target function not found: {target.__name__}')

        @functools.wraps(fn_ref)
        def wrapper(*args, **kwargs):
            return_value = fn_ref(*args, **kwargs)
            return fn(return_value, *args, *kwargs)

        update_wrapper(get_function_bound(target), target, wrapper)
        return fn

    return decorator


def catch(target: Union[Type[Any], Callable, Any], *params: Any) -> Callable[[F], F]:
    """Decorator for exception handling advice (supports multiple aspects)."""

    def decorator(fn: F) -> F:
        fn_ref = get_wrapped_function(target)
        if fn_ref is None:
            raise ValueError(f'Target function not found: {target.__name__}')

        @functools.wraps(fn_ref)
        def wrapper(*args, **kwargs):
            try:
                return fn_ref(*args, **kwargs)
            except Exception as e:  # Fixed: `any` is not a valid exception catch
                fn(e, *params)  # Execute the advice on exception
                raise  # Re-raise the exception

        update_wrapper(get_function_bound(target), target, wrapper)
        return fn

    return decorator
