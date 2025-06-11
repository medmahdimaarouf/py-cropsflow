from typing import Callable

from ...constants import *
from .metadata import *
from ...utils import InjectionToken


def declare(token: InjectionToken, dependency: Type[any], export: bool = False) -> Callable:
    """
    This Action decorator
    Parameters:
    selector (str): The selector of the action.
    """

    def decorator(cls):
        watermarks = getattr(cls, DECORATOR_WATERMARKS, [])
        if ACTION_WATERMARK not in watermarks:
            watermarks.append(DECLARATIONS_WATERMARK)
        else:
            raise Exception("Duplicated Action decorator")
        setattr(cls, DECORATOR_WATERMARKS, watermarks)
        declarations = getattr(cls, DECLARATIONS_ANNOTATION_KEY, [])
        declarations.append(DeclarationDecoratorMetaData(token=token, dependency=dependency, export=export))
        setattr(cls, DECLARATIONS_ANNOTATION_KEY, [_ for _ in declarations if _ is not None])
        return cls

    return decorator
