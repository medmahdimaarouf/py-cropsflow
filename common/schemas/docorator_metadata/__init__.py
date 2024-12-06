from dataclasses import dataclass
from typing import Any, Type

from .decorator_metadata_type import *


@dataclass
class DecoratorMetaData:
    target: Type[Any]
    type: DecoratorMetaDataType = "class"


