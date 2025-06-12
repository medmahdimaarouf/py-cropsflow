"""
This module defines the DeclarationDecoratorMetaData dataclass, which represents
metadata for a declaration decorator within the framework.

Attributes:
    type (DecoratorMetaDataType): The type of decorator, fixed to ACTION.
    token (InjectionToken): The injection token associated with the declaration.
    dependency (Type[Any]): The type of the dependency being declared.
    export (bool): Flag indicating if the dependency should be exported.
"""

from dataclasses import dataclass, field
from typing import Type, Any, Optional

from ...utils import InjectionToken
from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass
class DeclarationDecoratorMetaData(DecoratorMetaData):
    """
    Metadata class for declaration decorators.

    Attributes:
        type (DecoratorMetaDataType): The decorator type, fixed to ACTION.
        token (Optional[InjectionToken]): The injection token for the declared dependency.
        dependency (Optional[Type[Any]]): The class/type of the dependency.
        export (bool): Whether this declaration should be exported.
    """

    type: DecoratorMetaDataType = field(init=False, default=DecoratorMetaDataType.ACTION)
    token: Optional[InjectionToken] = field(default=None)
    dependency: Optional[Type[Any]] = field(default=None)
    export: bool = field(default=False)
