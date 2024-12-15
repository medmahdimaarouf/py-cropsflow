from typing import Generic, TypeVar, Optional, List
from dataclasses import dataclass, field

T = TypeVar('T')


@dataclass
class OptionMetaData(Generic[T]):
    setter_name: str = field(default_factory=str)
    name: str = field(default_factory=str)
    required: bool = field(default_factory=bool)
    default: Optional[T] = None  # Optional to indicate it's not always required
    metatype: T = None  # Generic type
    select: List[T] = None  # Optional list of generic type

    def __int__(self, setter_name: str, name: str, metatype: T, required: bool = False, select: List[T] = None,
                default: T = None):
        self.setter_name = setter_name
        self.name = name
        self.required = required
        self.default = default
        self.metatype = metatype
        self.select = select
