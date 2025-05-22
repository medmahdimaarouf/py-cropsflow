from dataclasses import dataclass
from enum import Enum
from typing import Any, Type

from .decorator_metadata_type import *


class DecoratorMetaDataType(Enum):
    CLASS = "class"
    INJECTABLE = "service"
    MODULE = "module"
    FACTORY = "factory"
    DATAPIPE = "datapipe"
    ACTION = "action"
    TASK = "task"
    INJECT = "inject"


@dataclass
class DecoratorMetaData:
    target: Type[Any]
    type: DecoratorMetaDataType = "class"
