"""
This module defines the ActionDecoratorMetaData dataclass which encapsulates metadata for
an Action decorator within the framework.

Attributes:
    type (DecoratorMetaDataType): The decorator type, fixed to ACTION.
    selector (str, optional): The selector used to identify the action.
    auto_next (bool): Flag indicating if the action automatically proceeds to the next step.
"""

from dataclasses import dataclass, field
from typing import Optional

from ...schemas import DecoratorMetaData, DecoratorMetaDataType


@dataclass
class ActionDecoratorMetaData(DecoratorMetaData):
    """
    Metadata class representing information related to an Action decorator.

    Attributes:
        type (DecoratorMetaDataType): The type of decorator, fixed to ACTION.
        selector (Optional[str]): The selector string used to identify the action.
        auto_next (bool): Whether to automatically proceed to the next action.
    """

    type: DecoratorMetaDataType = field(init=False, default=DecoratorMetaDataType.ACTION)
    selector: Optional[str] = field(default=None)
    auto_next: bool = field(default=False)
